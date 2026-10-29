package com.example.agent

import android.content.Context
import android.content.Intent
import com.example.R
import com.example.data.SecureStore
import com.example.data.SkillsStore
import com.example.model.ActionResponse
import com.example.model.ActionType
import com.example.model.EditJob
import com.example.model.JobStatus
import com.example.model.ObservationResult
import com.example.model.SkillRecord
import com.example.model.StepLog
import com.example.network.GeminiClient
import com.example.service.MiraAccessibilityService
import com.example.service.OverlayService
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import kotlinx.coroutines.suspendCancellableCoroutine
import kotlin.coroutines.resume

object AgentRunner {

    private val _currentJob = MutableStateFlow<EditJob?>(null)
    val currentJob: StateFlow<EditJob?> = _currentJob.asStateFlow()

    private val _logs = MutableStateFlow<List<StepLog>>(emptyList())
    val logs: StateFlow<List<StepLog>> = _logs.asStateFlow()

    private val _isPaused = MutableStateFlow(false)
    val isPaused: StateFlow<Boolean> = _isPaused.asStateFlow()

    private val _safetyPrompt = MutableStateFlow<String?>(null)
    val safetyPrompt: StateFlow<String?> = _safetyPrompt.asStateFlow()

    private var executionJob: Job? = null
    private var permissionContinuation: (suspend (Boolean) -> Unit)? = null

    fun startJob(context: Context, job: EditJob) {
        stopJob(context)

        _currentJob.value = job.copy(status = JobStatus.RUNNING)
        _logs.value = emptyList()
        _isPaused.value = false
        _safetyPrompt.value = null

        val overlayIntent = Intent(context, OverlayService::class.java).apply {
            action = OverlayService.ACTION_START_OVERLAY
        }
        context.startService(overlayIntent)

        OverlayService.onStopClicked = {
            stopJob(context)
        }
        OverlayService.onPauseResumeClicked = {
            togglePause(context)
        }
        OverlayService.onSafetyApproved = { approved ->
            permissionContinuation?.let { cb ->
                CoroutineScope(Dispatchers.Default).launch {
                    cb(approved)
                }
            }
        }

        executionJob = CoroutineScope(Dispatchers.Default).launch {
            runAgentLoop(context.applicationContext, job)
        }
    }

    fun stopJob(context: Context) {
        executionJob?.cancel()
        executionJob = null
        val job = _currentJob.value
        if (job != null && job.status == JobStatus.RUNNING) {
            val updated = job.copy(status = JobStatus.STOPPED)
            _currentJob.value = updated
            SecureStore(context).saveRecentJob(updated)
        }
        _isPaused.value = false
        _safetyPrompt.value = null

        val overlayIntent = Intent(context, OverlayService::class.java).apply {
            action = OverlayService.ACTION_STOP_OVERLAY
        }
        context.startService(overlayIntent)
    }

    fun togglePause(context: Context) {
        val next = !_isPaused.value
        _isPaused.value = next
        updateOverlay(context, if (next) "MIRA رکی ہوئی ہے (وقفہ)" else "MIRA دوبارہ جاری ہے", next)
    }

    fun respondSafetyPermission(approved: Boolean) {
        _safetyPrompt.value = null
        OverlayService.onSafetyApproved?.invoke(approved)
    }

    fun clearLogs() {
        _logs.value = emptyList()
    }

    private suspend fun runAgentLoop(context: Context, initialJob: EditJob) {
        val secureStore = SecureStore(context)
        val skillsStore = SkillsStore(context)
        val apiKey = secureStore.getApiKey()

        if (apiKey.isBlank()) {
            addLog(1, "API Key موجود نہیں ہے", "API Key missing", "ناکامی", false)
            finishJob(context, initialJob.copy(status = JobStatus.FAILED))
            return
        }

        val systemPrompt = try {
            context.resources.openRawResource(R.raw.system_prompt).bufferedReader().use { it.readText() }
        } catch (_: Exception) {
            "You are MIRA, an autonomous CapCut video editing agent on Android."
        }

        val geminiClient = GeminiClient(systemPrompt)
        val capcutPkg = secureStore.capcutPackage
        val stepDelayMs = secureStore.stepDelayMs
        val maxSteps = secureStore.maxSteps
        val maxRetries = secureStore.maxRetries

        var stepNumber = 0
        var totalApiCalls = 0
        var consecutiveFailures = 0
        var lastActionSummary = ""
        var sameActionCount = 0

        val service = MiraAccessibilityService.instance
        if (service == null) {
            addLog(1, "رسائی سروس (Accessibility) فعال نہیں ہے", "AccessibilityService null", "ناکامی", false)
            finishJob(context, initialJob.copy(status = JobStatus.FAILED))
            return
        }

        if (!service.isAllowedForeground()) {
            updateOverlay(context, "CapCut کھولا جا رہا ہے...")
            service.openApp(capcutPkg)
            delay(3000L)
        }

        while (stepNumber < maxSteps && CoroutineScope(Dispatchers.Default).isActive) {
            while (_isPaused.value) {
                delay(500L)
            }

            stepNumber++

            sendOverlayCommand(context, OverlayService.ACTION_HIDE_TEMP)
            delay(150L)

            val needScreenshot = (stepNumber == 1) || (consecutiveFailures > 0) || (stepNumber % 4 == 0)
            val observation = service.observe(includeScreenshot = needScreenshot)

            sendOverlayCommand(context, OverlayService.ACTION_SHOW_TEMP)

            if (!service.isAllowedForeground()) {
                addLog(
                    stepNumber = stepNumber,
                    thoughtUrdu = "ہم CapCut سے باہر ہیں۔ حفاظت کے لیے عمل روکا گیا۔",
                    screenSummary = "Outside CapCut: ${observation.packageName}",
                    actionName = "SAFETY_HALT",
                    isSuccess = false,
                    apiCalls = totalApiCalls
                )
                updateOverlay(context, "ہم CapCut سے باہر ہیں!")
                delay(2000L)
                service.openApp(capcutPkg)
                delay(2500L)
                continue
            }

            updateOverlay(context, "MIRA سوچ رہی ہے...")

            val (decision, callsUsed) = geminiClient.decideNextAction(
                apiKey = apiKey,
                modelName = secureStore.modelName,
                job = _currentJob.value ?: initialJob,
                currentObservation = observation,
                history = _logs.value,
                sendScreenshot = needScreenshot,
                onWaitingRateLimit = { waitingMsg ->
                    updateOverlay(context, waitingMsg)
                }
            )
            totalApiCalls += callsUsed

            _currentJob.value = _currentJob.value?.copy(
                progress = decision.progressPercent.coerceIn(0, 100),
                apiCallsCount = totalApiCalls
            )

            updateOverlay(context, decision.thoughtUrdu.ifBlank { "MIRA ایکشن لے رہی ہے..." })

            val currentActionKey = "${decision.action}_${decision.x}_${decision.y}_${decision.targetNodeIndex}"
            if (currentActionKey == lastActionSummary) {
                sameActionCount++
                if (sameActionCount >= 3) {
                    addLog(
                        stepNumber = stepNumber,
                        thoughtUrdu = "ایک ہی عمل 3 بار دہرایا گیا ہے۔ آپ کی رائے درکار ہے۔",
                        screenSummary = "Loop detected: $currentActionKey",
                        actionName = "LOOP_DETECTED",
                        isSuccess = false,
                        apiCalls = totalApiCalls
                    )
                    pauseForUser(context, "ایک ہی اسکرین پر بار بار کوشش ناکام رہی۔ کیا آپ ہاتھ سے اگلا مرحلہ مکمل کریں گے؟")
                    sameActionCount = 0
                    continue
                }
            } else {
                sameActionCount = 1
                lastActionSummary = currentActionKey
            }

            val isSensitiveAction = decision.action == ActionType.REQUEST_PERMISSION ||
                    (secureStore.askBeforeExport && decision.expectedResult.contains("export", ignoreCase = true)) ||
                    decision.thoughtUrdu.contains("محفوظ") ||
                    decision.thoughtUrdu.contains("ایکسپورٹ")

            if (isSensitiveAction) {
                _currentJob.value = _currentJob.value?.copy(status = JobStatus.WAITING_PERMISSION)
                val promptText = "MIRA ویڈیو کو ایکسپورٹ یا محفوظ کرنا چاہتی ہے۔ کیا آپ اجازت دیتے ہیں؟"
                _safetyPrompt.value = promptText

                val permissionApproved = requestUserPermissionSuspend(context, promptText)
                _safetyPrompt.value = null

                if (!permissionApproved) {
                    addLog(
                        stepNumber = stepNumber,
                        thoughtUrdu = "صارف نے ایکسپورٹ کی اجازت نہیں دی۔",
                        screenSummary = "User declined permission",
                        actionName = "PERMISSION_DENIED",
                        isSuccess = false,
                        apiCalls = totalApiCalls
                    )
                    _currentJob.value = _currentJob.value?.copy(status = JobStatus.STOPPED)
                    finishJob(context, _currentJob.value ?: initialJob)
                    return
                }
                _currentJob.value = _currentJob.value?.copy(status = JobStatus.RUNNING)
            }

            if (decision.action == ActionType.DONE) {
                addLog(
                    stepNumber = stepNumber,
                    thoughtUrdu = decision.thoughtUrdu.ifBlank { "الحمدللہ! ویڈیو ایڈیٹنگ مکمل ہو گئی۔" },
                    screenSummary = decision.screenSummary,
                    actionName = "DONE",
                    isSuccess = true,
                    apiCalls = totalApiCalls
                )
                finishJob(context, (_currentJob.value ?: initialJob).copy(status = JobStatus.COMPLETED, progress = 100))
                return
            }

            if (decision.action == ActionType.FAIL) {
                addLog(
                    stepNumber = stepNumber,
                    thoughtUrdu = decision.thoughtUrdu.ifBlank { "ایڈیٹنگ مکمل نہیں ہو سکی۔" },
                    screenSummary = decision.screenSummary,
                    actionName = "FAIL",
                    isSuccess = false,
                    apiCalls = totalApiCalls
                )
                finishJob(context, (_currentJob.value ?: initialJob).copy(status = JobStatus.FAILED))
                return
            }

            if (decision.action == ActionType.ASK_USER) {
                pauseForUser(context, decision.thoughtUrdu)
                continue
            }

            val executionSuccess = executeAction(service, decision, observation)

            addLog(
                stepNumber = stepNumber,
                thoughtUrdu = decision.thoughtUrdu,
                screenSummary = decision.screenSummary,
                actionName = "${decision.action} (${decision.expectedResult.take(30)})",
                isSuccess = executionSuccess,
                apiCalls = totalApiCalls
            )

            if (executionSuccess && decision.targetNodeIndex != null && decision.targetNodeIndex in observation.nodes.indices) {
                val node = observation.nodes[decision.targetNodeIndex]
                val label = node.text.ifBlank { node.contentDescription }
                if (label.isNotBlank()) {
                    val capcutVer = try {
                        context.packageManager.getPackageInfo(capcutPkg, 0).versionName ?: "unknown"
                    } catch (_: Exception) { "unknown" }

                    val metrics = context.resources.displayMetrics
                    skillsStore.saveSkill(
                        SkillRecord(
                            capcutVersion = capcutVer,
                            label = label,
                            viewId = node.viewIdResourceName,
                            relativeX = node.bounds.centerX().toFloat() / metrics.widthPixels,
                            relativeY = node.bounds.centerY().toFloat() / metrics.heightPixels
                        )
                    )
                }
            }

            delay(stepDelayMs)

            val postObservation = service.observe(includeScreenshot = false)
            val screenChanged = postObservation.treeJson != observation.treeJson
            if (!screenChanged && decision.action != ActionType.WAIT) {
                consecutiveFailures++
                if (consecutiveFailures >= maxRetries) {
                    pauseForUser(context, "مسلسل $maxRetries کوششوں کے باوجود اسکرین میں تبدیلی نہیں ہوئی۔ آپ کی رہنمائی درکار ہے۔")
                    consecutiveFailures = 0
                }
            } else {
                consecutiveFailures = 0
            }
        }

        finishJob(context, (_currentJob.value ?: initialJob).copy(status = JobStatus.COMPLETED))
    }

    private suspend fun executeAction(
        service: MiraAccessibilityService,
        action: ActionResponse,
        observation: ObservationResult
    ): Boolean {
        return try {
            when (action.action) {
                ActionType.TAP -> {
                    if (action.targetNodeIndex != null && action.targetNodeIndex in observation.nodes.indices) {
                        val node = observation.nodes[action.targetNodeIndex]
                        service.tap(node.bounds.centerX().toFloat(), node.bounds.centerY().toFloat())
                    } else if (action.x != null && action.y != null) {
                        val realX = action.x * observation.scaleFactorX
                        val realY = action.y * observation.scaleFactorY
                        service.tap(realX, realY)
                    } else {
                        false
                    }
                }
                ActionType.LONG_PRESS -> {
                    val realX = (action.x ?: 500f) * observation.scaleFactorX
                    val realY = (action.y ?: 500f) * observation.scaleFactorY
                    service.longPress(realX, realY, action.durationMs ?: 600L)
                }
                ActionType.SWIPE, ActionType.DRAG -> {
                    val x1 = (action.x ?: 300f) * observation.scaleFactorX
                    val y1 = (action.y ?: 500f) * observation.scaleFactorY
                    val x2 = (action.x2 ?: 700f) * observation.scaleFactorX
                    val y2 = (action.y2 ?: 500f) * observation.scaleFactorY
                    service.swipe(x1, y1, x2, y2, action.durationMs ?: 350L)
                }
                ActionType.PINCH -> {
                    val cx = (action.x ?: 500f) * observation.scaleFactorX
                    val cy = (action.y ?: 500f) * observation.scaleFactorY
                    service.pinch(cx, cy, zoomIn = true, durationMs = action.durationMs ?: 350L)
                }
                ActionType.SCROLL -> {
                    val scrollDown = (action.y2 ?: 0f) < (action.y ?: 1f)
                    service.scroll(scrollDown)
                }
                ActionType.TYPE_TEXT -> {
                    service.typeText(action.text ?: "")
                }
                ActionType.BACK -> {
                    service.pressBack()
                }
                ActionType.HOME -> {
                    service.pressHome()
                }
                ActionType.OPEN_APP -> {
                    service.openApp(action.text ?: "com.lemon.lvoverseas")
                }
                ActionType.WAIT -> {
                    delay(action.durationMs ?: 1200L)
                    true
                }
                else -> true
            }
        } catch (_: Exception) {
            false
        }
    }

    private suspend fun requestUserPermissionSuspend(context: Context, prompt: String): Boolean =
        suspendCancellableCoroutine { cont ->
            permissionContinuation = { approved ->
                permissionContinuation = null
                if (cont.isActive) cont.resume(approved)
            }
            val intent = Intent(context, OverlayService::class.java).apply {
                action = OverlayService.ACTION_SHOW_SAFETY_DIALOG
                putExtra(OverlayService.EXTRA_PERMISSION_PROMPT, prompt)
            }
            context.startService(intent)
        }

    private fun pauseForUser(context: Context, urduMessage: String) {
        _isPaused.value = true
        _currentJob.value = _currentJob.value?.copy(status = JobStatus.WAITING_USER)
        updateOverlay(context, urduMessage, isPaused = true)
    }

    private fun updateOverlay(context: Context, statusUrdu: String, isPaused: Boolean = false) {
        val intent = Intent(context, OverlayService::class.java).apply {
            action = OverlayService.ACTION_UPDATE_STATUS
            putExtra(OverlayService.EXTRA_STATUS_URDU, statusUrdu)
            putExtra(OverlayService.EXTRA_IS_PAUSED, isPaused)
        }
        context.startService(intent)
    }

    private fun sendOverlayCommand(context: Context, action: String) {
        val intent = Intent(context, OverlayService::class.java).apply {
            this.action = action
        }
        context.startService(intent)
    }

    private fun addLog(
        stepNumber: Int,
        thoughtUrdu: String,
        screenSummary: String,
        actionName: String,
        isSuccess: Boolean,
        apiCalls: Int = 0
    ) {
        val step = StepLog(
            stepNumber = stepNumber,
            thoughtUrdu = thoughtUrdu,
            screenSummary = screenSummary,
            actionName = actionName,
            resultUrdu = if (isSuccess) "کامیاب" else "دوبارہ کوشش",
            isSuccess = isSuccess,
            apiCalls = apiCalls
        )
        val current = _logs.value.toMutableList()
        current.add(step)
        _logs.value = current
    }

    private fun finishJob(context: Context, job: EditJob) {
        _currentJob.value = job
        SecureStore(context).saveRecentJob(job)
        updateOverlay(
            context,
            when (job.status) {
                JobStatus.COMPLETED -> "ایڈیٹنگ مکمل ہو گئی!"
                JobStatus.FAILED -> "ٹاسک ناکام ہو گیا"
                JobStatus.STOPPED -> "ٹاسک روک دیا گیا"
                else -> "MIRA بند ہے"
            }
        )
    }
}
