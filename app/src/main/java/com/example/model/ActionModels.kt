package com.example.model

import android.graphics.Bitmap
import android.graphics.Rect

enum class JobStatus {
    IDLE,
    RUNNING,
    PAUSED,
    WAITING_PERMISSION,
    WAITING_USER,
    COMPLETED,
    FAILED,
    STOPPED
}

enum class ActionType {
    TAP,
    LONG_PRESS,
    SWIPE,
    DRAG,
    PINCH,
    TYPE_TEXT,
    BACK,
    HOME,
    OPEN_APP,
    WAIT,
    SCROLL,
    REQUEST_PERMISSION,
    ASK_USER,
    DONE,
    FAIL;

    companion object {
        fun fromString(value: String): ActionType {
            return entries.firstOrNull { it.name.equals(value.trim(), ignoreCase = true) } ?: WAIT
        }
    }
}

data class ActionResponse(
    val thoughtUrdu: String = "",
    val screenSummary: String = "",
    val action: ActionType = ActionType.WAIT,
    val x: Float? = null,
    val y: Float? = null,
    val x2: Float? = null,
    val y2: Float? = null,
    val durationMs: Long? = null,
    val text: String? = null,
    val targetNodeIndex: Int? = null,
    val expectedResult: String = "",
    val progressPercent: Int = 0
)

data class UiNode(
    val index: Int,
    val className: String,
    val text: String,
    val contentDescription: String,
    val viewIdResourceName: String,
    val bounds: Rect,
    val clickable: Boolean,
    val scrollable: Boolean,
    val editable: Boolean,
    val enabled: Boolean
)

data class ObservationResult(
    val treeJson: String,
    val nodes: List<UiNode>,
    val screenshot: Bitmap?,
    val screenshotBase64: String?,
    val scaleFactorX: Float = 1.0f,
    val scaleFactorY: Float = 1.0f,
    val packageName: String = "",
    val windowTitle: String = ""
)

data class StepLog(
    val stepNumber: Int,
    val timestamp: Long = System.currentTimeMillis(),
    val thoughtUrdu: String,
    val screenSummary: String,
    val actionName: String,
    val resultUrdu: String,
    val isSuccess: Boolean = true,
    val apiCalls: Int = 0
)

data class EditJob(
    val id: String = java.util.UUID.randomUUID().toString(),
    val videoUri: String? = null,
    val videoNote: String = "",
    val cutTimings: String = "",
    val style: String = "MIRA خود فیصلہ کرے",
    val instructions: String = "",
    val status: JobStatus = JobStatus.IDLE,
    val progress: Int = 0,
    val createdAt: Long = System.currentTimeMillis(),
    val apiCallsCount: Int = 0
)

data class SkillRecord(
    val capcutVersion: String,
    val label: String,
    val viewId: String? = null,
    val relativeX: Float = 0.5f,
    val relativeY: Float = 0.5f
)
