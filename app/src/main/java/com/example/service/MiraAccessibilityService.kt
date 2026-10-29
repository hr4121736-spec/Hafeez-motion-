package com.example.service

import android.accessibilityservice.AccessibilityService
import android.accessibilityservice.GestureDescription
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.ColorSpace
import android.graphics.Path
import android.graphics.Rect
import android.hardware.HardwareBuffer
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.util.Base64
import android.view.Display
import android.view.accessibility.AccessibilityEvent
import android.view.accessibility.AccessibilityNodeInfo
import com.example.model.ObservationResult
import com.example.model.UiNode
import kotlinx.coroutines.suspendCancellableCoroutine
import org.json.JSONArray
import org.json.JSONObject
import java.io.ByteArrayOutputStream
import java.util.concurrent.Executor
import kotlin.coroutines.resume

class MiraAccessibilityService : AccessibilityService() {

    companion object {
        @Volatile
        var instance: MiraAccessibilityService? = null
            private set

        fun isServiceRunning(): Boolean = instance != null
    }

    private val mainHandler = Handler(Looper.getMainLooper())
    private val mainExecutor = Executor { command -> mainHandler.post(command) }
    private var lastForegroundPackage: String = ""

    override fun onServiceConnected() {
        super.onServiceConnected()
        instance = this
    }

    override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        event?.packageName?.toString()?.let {
            if (it.isNotBlank()) {
                lastForegroundPackage = it
            }
        }
    }

    override fun onInterrupt() {}

    override fun onDestroy() {
        super.onDestroy()
        if (instance == this) {
            instance = null
        }
    }

    fun getCurrentPackageName(): String {
        val root = rootInActiveWindow
        val pkg = root?.packageName?.toString() ?: lastForegroundPackage
        root?.recycle()
        return pkg
    }

    fun isAllowedForeground(): Boolean {
        val pkg = getCurrentPackageName()
        return pkg.contains("lemon") ||
                pkg.contains("capcut") ||
                pkg.contains("mira") ||
                pkg.contains("example")
    }

    suspend fun observe(includeScreenshot: Boolean = true): ObservationResult {
        val nodes = mutableListOf<UiNode>()
        val root = rootInActiveWindow
        val currentPkg = root?.packageName?.toString() ?: lastForegroundPackage
        val windowTitle = root?.text?.toString() ?: ""

        if (root != null) {
            flattenTree(root, nodes)
            root.recycle()
        }

        val treeJson = buildTreeJson(nodes)

        var screenshot: Bitmap? = null
        var base64Jpeg: String? = null
        var scaleX = 1.0f
        var scaleY = 1.0f

        if (includeScreenshot) {
            val rawBmp = captureScreenshot()
            if (rawBmp != null) {
                val origW = rawBmp.width
                val origH = rawBmp.height
                val maxDim = 1080
                val longSide = maxOf(origW, origH)

                val scaledBmp = if (longSide > maxDim) {
                    val scale = maxDim.toFloat() / longSide
                    val targetW = (origW * scale).toInt().coerceAtLeast(1)
                    val targetH = (origH * scale).toInt().coerceAtLeast(1)
                    scaleX = origW.toFloat() / targetW
                    scaleY = origH.toFloat() / targetH
                    Bitmap.createScaledBitmap(rawBmp, targetW, targetH, true).also {
                        if (it != rawBmp) rawBmp.recycle()
                    }
                } else {
                    scaleX = 1.0f
                    scaleY = 1.0f
                    rawBmp
                }

                val stream = ByteArrayOutputStream()
                scaledBmp.compress(Bitmap.CompressFormat.JPEG, 70, stream)
                val bytes = stream.toByteArray()
                base64Jpeg = Base64.encodeToString(bytes, Base64.NO_WRAP)
                screenshot = scaledBmp
            }
        }

        return ObservationResult(
            treeJson = treeJson,
            nodes = nodes,
            screenshot = screenshot,
            screenshotBase64 = base64Jpeg,
            scaleFactorX = scaleX,
            scaleFactorY = scaleY,
            packageName = currentPkg,
            windowTitle = windowTitle
        )
    }

    private suspend fun captureScreenshot(): Bitmap? = suspendCancellableCoroutine { cont ->
        try {
            takeScreenshot(
                Display.DEFAULT_DISPLAY,
                mainExecutor,
                object : TakeScreenshotCallback {
                    override fun onSuccess(result: ScreenshotResult) {
                        val hardwareBuffer = result.hardwareBuffer
                        val colorSpace = result.colorSpace ?: ColorSpace.get(ColorSpace.Named.SRGB)
                        val bmp = Bitmap.wrapHardwareBuffer(hardwareBuffer, colorSpace)
                        hardwareBuffer.close()

                        val softwareBmp = bmp?.copy(Bitmap.Config.ARGB_8888, false)
                        bmp?.recycle()
                        if (cont.isActive) {
                            cont.resume(softwareBmp)
                        }
                    }

                    override fun onFailure(errorCode: Int) {
                        if (cont.isActive) {
                            cont.resume(null)
                        }
                    }
                }
            )
        } catch (_: Exception) {
            if (cont.isActive) {
                cont.resume(null)
            }
        }
    }

    private fun flattenTree(node: AccessibilityNodeInfo, list: MutableList<UiNode>) {
        val bounds = Rect()
        node.getBoundsInScreen(bounds)

        val text = node.text?.toString() ?: ""
        val desc = node.contentDescription?.toString() ?: ""
        val viewId = node.viewIdResourceName ?: ""
        val className = node.className?.toString() ?: ""

        val isUseful = text.isNotBlank() ||
                desc.isNotBlank() ||
                viewId.isNotBlank() ||
                node.isClickable ||
                node.isEditable ||
                node.isScrollable

        if (isUseful) {
            list.add(
                UiNode(
                    index = list.size,
                    className = className,
                    text = text.take(60),
                    contentDescription = desc.take(60),
                    viewIdResourceName = viewId,
                    bounds = bounds,
                    clickable = node.isClickable,
                    scrollable = node.isScrollable,
                    editable = node.isEditable,
                    enabled = node.isEnabled
                )
            )
        }

        for (i in 0 until node.childCount) {
            val child = node.getChild(i) ?: continue
            flattenTree(child, list)
            child.recycle()
        }
    }

    private fun buildTreeJson(nodes: List<UiNode>): String {
        val array = JSONArray()
        for (node in nodes.take(40)) {
            val obj = JSONObject().apply {
                put("idx", node.index)
                if (node.text.isNotBlank()) put("text", node.text)
                if (node.contentDescription.isNotBlank()) put("desc", node.contentDescription)
                if (node.viewIdResourceName.isNotBlank()) put("id", node.viewIdResourceName.substringAfterLast('/'))
                put("x", node.bounds.centerX())
                put("y", node.bounds.centerY())
                if (node.clickable) put("click", true)
                if (node.editable) put("edit", true)
                if (node.scrollable) put("scroll", true)
            }
            array.put(obj)
        }
        return array.toString()
    }

    suspend fun tap(x: Float, y: Float): Boolean {
        val path = Path().apply { moveTo(x, y) }
        val stroke = GestureDescription.StrokeDescription(path, 0L, 50L)
        val gesture = GestureDescription.Builder().addStroke(stroke).build()
        return dispatchGestureSuspending(gesture)
    }

    suspend fun longPress(x: Float, y: Float, durationMs: Long = 600L): Boolean {
        val path = Path().apply { moveTo(x, y) }
        val stroke = GestureDescription.StrokeDescription(path, 0L, durationMs.coerceIn(400L, 2000L))
        val gesture = GestureDescription.Builder().addStroke(stroke).build()
        return dispatchGestureSuspending(gesture)
    }

    suspend fun swipe(x1: Float, y1: Float, x2: Float, y2: Float, durationMs: Long = 300L): Boolean {
        val path = Path().apply {
            moveTo(x1, y1)
            lineTo(x2, y2)
        }
        val stroke = GestureDescription.StrokeDescription(path, 0L, durationMs.coerceIn(100L, 1500L))
        val gesture = GestureDescription.Builder().addStroke(stroke).build()
        return dispatchGestureSuspending(gesture)
    }

    suspend fun drag(x1: Float, y1: Float, x2: Float, y2: Float, durationMs: Long = 800L): Boolean {
        return swipe(x1, y1, x2, y2, durationMs)
    }

    suspend fun pinch(centerX: Float, centerY: Float, zoomIn: Boolean = true, durationMs: Long = 350L): Boolean {
        val offset = 180f
        val path1 = Path()
        val path2 = Path()

        if (zoomIn) {
            path1.moveTo(centerX - 40f, centerY)
            path1.lineTo(centerX - offset, centerY)
            path2.moveTo(centerX + 40f, centerY)
            path2.lineTo(centerX + offset, centerY)
        } else {
            path1.moveTo(centerX - offset, centerY)
            path1.lineTo(centerX - 40f, centerY)
            path2.moveTo(centerX + offset, centerY)
            path2.lineTo(centerX + offset, centerY)
        }

        val stroke1 = GestureDescription.StrokeDescription(path1, 0L, durationMs)
        val stroke2 = GestureDescription.StrokeDescription(path2, 0L, durationMs)
        val gesture = GestureDescription.Builder().addStroke(stroke1).addStroke(stroke2).build()
        return dispatchGestureSuspending(gesture)
    }

    suspend fun scroll(down: Boolean = true): Boolean {
        val metrics = resources.displayMetrics
        val centerX = metrics.widthPixels / 2f
        val startY = if (down) metrics.heightPixels * 0.7f else metrics.heightPixels * 0.3f
        val endY = if (down) metrics.heightPixels * 0.3f else metrics.heightPixels * 0.7f
        return swipe(centerX, startY, centerX, endY, 300L)
    }

    fun typeText(text: String): Boolean {
        val root = rootInActiveWindow ?: return false
        val focused = root.findFocus(AccessibilityNodeInfo.FOCUS_INPUT)
        val target = focused ?: findFirstEditable(root)
        root.recycle()

        if (target != null) {
            val arguments = Bundle().apply {
                putCharSequence(AccessibilityNodeInfo.ACTION_ARGUMENT_SET_TEXT_CHARSEQUENCE, text)
            }
            val success = target.performAction(AccessibilityNodeInfo.ACTION_SET_TEXT, arguments)
            target.recycle()
            return success
        }
        return false
    }

    private fun findFirstEditable(node: AccessibilityNodeInfo): AccessibilityNodeInfo? {
        if (node.isEditable) return node
        for (i in 0 until node.childCount) {
            val child = node.getChild(i) ?: continue
            val found = findFirstEditable(child)
            if (found != null) return found
            child.recycle()
        }
        return null
    }

    fun pressBack(): Boolean = performGlobalAction(GLOBAL_ACTION_BACK)

    fun pressHome(): Boolean = performGlobalAction(GLOBAL_ACTION_HOME)

    fun openApp(packageName: String): Boolean {
        return try {
            val launchIntent = packageManager.getLaunchIntentForPackage(packageName)
            if (launchIntent != null) {
                launchIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                startActivity(launchIntent)
                true
            } else {
                false
            }
        } catch (_: Exception) {
            false
        }
    }

    private suspend fun dispatchGestureSuspending(gesture: GestureDescription): Boolean =
        suspendCancellableCoroutine { cont ->
            try {
                val dispatched = dispatchGesture(
                    gesture,
                    object : GestureResultCallback() {
                        override fun onCompleted(gestureDescription: GestureDescription?) {
                            if (cont.isActive) cont.resume(true)
                        }

                        override fun onCancelled(gestureDescription: GestureDescription?) {
                            if (cont.isActive) cont.resume(false)
                        }
                    },
                    mainHandler
                )
                if (!dispatched && cont.isActive) {
                    cont.resume(false)
                }
            } catch (_: Exception) {
                if (cont.isActive) {
                    cont.resume(false)
                }
            }
        }
}
