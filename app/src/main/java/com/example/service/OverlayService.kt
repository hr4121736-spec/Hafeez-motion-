package com.example.service

import android.annotation.SuppressLint
import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Context
import android.content.Intent
import android.graphics.Color
import android.graphics.PixelFormat
import android.graphics.drawable.GradientDrawable
import android.os.Build
import android.os.IBinder
import android.provider.Settings
import android.view.Gravity
import android.view.MotionEvent
import android.view.View
import android.view.WindowManager
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView
import androidx.core.app.NotificationCompat
import com.example.MainActivity
import com.example.R
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

class OverlayService : Service() {

    companion object {
        const val ACTION_START_OVERLAY = "com.example.mira.ACTION_START_OVERLAY"
        const val ACTION_STOP_OVERLAY = "com.example.mira.ACTION_STOP_OVERLAY"
        const val ACTION_UPDATE_STATUS = "com.example.mira.ACTION_UPDATE_STATUS"
        const val ACTION_HIDE_TEMP = "com.example.mira.ACTION_HIDE_TEMP"
        const val ACTION_SHOW_TEMP = "com.example.mira.ACTION_SHOW_TEMP"
        const val ACTION_SHOW_SAFETY_DIALOG = "com.example.mira.ACTION_SHOW_SAFETY_DIALOG"

        const val EXTRA_STATUS_URDU = "extra_status_urdu"
        const val EXTRA_IS_PAUSED = "extra_is_paused"
        const val EXTRA_PERMISSION_PROMPT = "extra_permission_prompt"

        @Volatile
        var isOverlayRunning = false
            private set

        @Volatile
        var onStopClicked: (() -> Unit)? = null

        @Volatile
        var onPauseResumeClicked: (() -> Unit)? = null

        @Volatile
        var onSafetyApproved: ((Boolean) -> Unit)? = null

        fun canDrawOverlays(context: Context): Boolean {
            return Settings.canDrawOverlays(context)
        }
    }

    private var windowManager: WindowManager? = null
    private var bubbleView: View? = null
    private var safetyDialogView: View? = null
    private var bubbleParams: WindowManager.LayoutParams? = null

    private var statusTextView: TextView? = null
    private var pauseResumeButton: Button? = null
    private var isPausedState: Boolean = false

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onCreate() {
        super.onCreate()
        windowManager = getSystemService(Context.WINDOW_SERVICE) as WindowManager
        createNotificationChannel()
        val notification = buildForegroundNotification("MIRA AI فعال ہے")
        startForeground(1001, notification)
        isOverlayRunning = true
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val action = intent?.action ?: return START_STICKY

        when (action) {
            ACTION_START_OVERLAY -> {
                if (bubbleView == null) {
                    createFloatingBubble()
                }
            }
            ACTION_STOP_OVERLAY -> {
                removeFloatingBubble()
                removeSafetyDialog()
                stopForeground(STOP_FOREGROUND_REMOVE)
                stopSelf()
            }
            ACTION_UPDATE_STATUS -> {
                val status = intent.getStringExtra(EXTRA_STATUS_URDU) ?: "MIRA کام کر رہی ہے..."
                isPausedState = intent.getBooleanExtra(EXTRA_IS_PAUSED, false)
                statusTextView?.text = status
                pauseResumeButton?.text = if (isPausedState) "جاری رکھیں" else "وقفہ"
                updateNotification(status)
            }
            ACTION_HIDE_TEMP -> {
                bubbleView?.visibility = View.GONE
                safetyDialogView?.visibility = View.GONE
            }
            ACTION_SHOW_TEMP -> {
                bubbleView?.visibility = View.VISIBLE
            }
            ACTION_SHOW_SAFETY_DIALOG -> {
                val prompt = intent.getStringExtra(EXTRA_PERMISSION_PROMPT) ?: "کیا آپ ایکسپورٹ / محفوظ کرنے کی اجازت دیتے ہیں؟"
                showSafetyPromptDialog(prompt)
            }
        }

        return START_STICKY
    }

    @SuppressLint("ClickableViewAccessibility")
    private fun createFloatingBubble() {
        if (!Settings.canDrawOverlays(this)) return

        val layoutType = WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
        bubbleParams = WindowManager.LayoutParams(
            WindowManager.LayoutParams.WRAP_CONTENT,
            WindowManager.LayoutParams.WRAP_CONTENT,
            layoutType,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or
                    WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.TOP or Gravity.START
            x = 40
            y = 200
        }

        val container = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            setPadding(24, 16, 24, 16)
            background = GradientDrawable().apply {
                setColor(Color.parseColor("#EE0F172A"))
                cornerRadius = 40f
                setStroke(3, Color.parseColor("#06B6D4"))
            }
        }

        statusTextView = TextView(this).apply {
            text = "MIRA کام کر رہی ہے..."
            setTextColor(Color.WHITE)
            textSize = 13f
            maxWidth = 420
            setPadding(0, 0, 16, 0)
        }

        pauseResumeButton = Button(this).apply {
            text = "وقفہ"
            textSize = 11f
            setTextColor(Color.WHITE)
            background = GradientDrawable().apply {
                setColor(Color.parseColor("#334155"))
                cornerRadius = 24f
            }
            setOnClickListener {
                isPausedState = !isPausedState
                text = if (isPausedState) "جاری رکھیں" else "وقفہ"
                onPauseResumeClicked?.invoke()
            }
        }

        val stopButton = Button(this).apply {
            text = "روکیں"
            textSize = 11f
            setTextColor(Color.WHITE)
            background = GradientDrawable().apply {
                setColor(Color.parseColor("#E11D48"))
                cornerRadius = 24f
            }
            setOnClickListener {
                onStopClicked?.invoke()
            }
        }

        container.addView(statusTextView)
        container.addView(pauseResumeButton)
        container.addView(View(this).apply {
            layoutParams = LinearLayout.LayoutParams(12, 1)
        })
        container.addView(stopButton)

        container.setOnTouchListener(object : View.OnTouchListener {
            private var initialX = 0
            private var initialY = 0
            private var initialTouchX = 0f
            private var initialTouchY = 0f
            private var isMoving = false

            override fun onTouch(v: View, event: MotionEvent): Boolean {
                when (event.action) {
                    MotionEvent.ACTION_DOWN -> {
                        initialX = bubbleParams?.x ?: 0
                        initialY = bubbleParams?.y ?: 0
                        initialTouchX = event.rawX
                        initialTouchY = event.rawY
                        isMoving = false
                        return false
                    }
                    MotionEvent.ACTION_MOVE -> {
                        val dx = event.rawX - initialTouchX
                        val dy = event.rawY - initialTouchY
                        if (Math.abs(dx) > 10 || Math.abs(dy) > 10) {
                            isMoving = true
                            bubbleParams?.x = initialX + dx.toInt()
                            bubbleParams?.y = initialY + dy.toInt()
                            windowManager?.updateViewLayout(bubbleView, bubbleParams)
                            return true
                        }
                    }
                    MotionEvent.ACTION_UP -> {
                        return isMoving
                    }
                }
                return false
            }
        })

        bubbleView = container
        try {
            windowManager?.addView(bubbleView, bubbleParams)
        } catch (_: Exception) {}
    }

    private fun showSafetyPromptDialog(prompt: String) {
        removeSafetyDialog()
        val layoutType = WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
        val dialogParams = WindowManager.LayoutParams(
            WindowManager.LayoutParams.MATCH_PARENT,
            WindowManager.LayoutParams.WRAP_CONTENT,
            layoutType,
            WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.CENTER
        }

        val dialog = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER
            setPadding(40, 36, 40, 36)
            background = GradientDrawable().apply {
                setColor(Color.parseColor("#FA0F172A"))
                cornerRadius = 32f
                setStroke(4, Color.parseColor("#F59E0B"))
            }
        }

        val promptView = TextView(this).apply {
            text = prompt
            setTextColor(Color.WHITE)
            textSize = 16f
            gravity = Gravity.CENTER
            setPadding(0, 0, 0, 24)
        }

        val buttonRow = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER
        }

        val approveBtn = Button(this).apply {
            text = "ہاں، آگے بڑھیں"
            setTextColor(Color.WHITE)
            background = GradientDrawable().apply {
                setColor(Color.parseColor("#10B981"))
                cornerRadius = 24f
            }
            setOnClickListener {
                removeSafetyDialog()
                onSafetyApproved?.invoke(true)
            }
        }

        val cancelBtn = Button(this).apply {
            text = "منسوخ کریں"
            setTextColor(Color.WHITE)
            background = GradientDrawable().apply {
                setColor(Color.parseColor("#E11D48"))
                cornerRadius = 24f
            }
            setOnClickListener {
                removeSafetyDialog()
                onSafetyApproved?.invoke(false)
            }
        }

        buttonRow.addView(approveBtn)
        buttonRow.addView(View(this).apply {
            layoutParams = LinearLayout.LayoutParams(24, 1)
        })
        buttonRow.addView(cancelBtn)

        dialog.addView(promptView)
        dialog.addView(buttonRow)

        safetyDialogView = dialog
        try {
            windowManager?.addView(safetyDialogView, dialogParams)
        } catch (_: Exception) {}
    }

    private fun removeFloatingBubble() {
        if (bubbleView != null) {
            try {
                windowManager?.removeView(bubbleView)
            } catch (_: Exception) {}
            bubbleView = null
        }
    }

    private fun removeSafetyDialog() {
        if (safetyDialogView != null) {
            try {
                windowManager?.removeView(safetyDialogView)
            } catch (_: Exception) {}
            safetyDialogView = null
        }
    }

    private fun createNotificationChannel() {
        val channel = NotificationChannel(
            "mira_agent_channel",
            "MIRA AI Agent Service",
            NotificationManager.IMPORTANCE_LOW
        ).apply {
            description = "MIRA video editing autonomous agent loop"
        }
        val nm = getSystemService(NotificationManager::class.java)
        nm.createNotificationChannel(channel)
    }

    private fun buildForegroundNotification(statusText: String): Notification {
        val openIntent = Intent(this, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_SINGLE_TOP
        }
        val pendingIntent = PendingIntent.getActivity(
            this,
            0,
            openIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        return NotificationCompat.Builder(this, "mira_agent_channel")
            .setContentTitle("MIRA AI ایڈیٹنگ جاری ہے")
            .setContentText(statusText)
            .setSmallIcon(R.mipmap.ic_launcher)
            .setOngoing(true)
            .setContentIntent(pendingIntent)
            .build()
    }

    private fun updateNotification(statusText: String) {
        val nm = getSystemService(NotificationManager::class.java)
        nm.notify(1001, buildForegroundNotification(statusText))
    }

    override fun onDestroy() {
        super.onDestroy()
        removeFloatingBubble()
        removeSafetyDialog()
        isOverlayRunning = false
    }
}
