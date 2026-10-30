#!/usr/bin/env python3
"""
patch_openrouter.py
-------------------
Applies the OpenRouter patch to MIRA AI Android project.
Overwrites all changed files with their complete new content and removes deprecated GeminiClient.kt.

Usage:
    python3 patch_openrouter.py
"""

import os
from pathlib import Path

FILES = {}

# 1. .env.example
FILES[".env.example"] = """# OPENROUTER_API_KEY: Required for OpenRouter AI API calls.
# AI Studio injects this or you paste it in MIRA AI Settings.
# OPENROUTER_API_KEY=sk-or-v1-your-key-here
"""

# 2. metadata.json
FILES["metadata.json"] = """{
  "name": "MIRA AI",
  "description": "Urdu-speaking autonomous AI video editing agent for CapCut with Accessibility Service, floating overlay, and OpenRouter reasoning.",
  "requestFramePermissions": [],
  "majorCapabilities": ["MAJOR_CAPABILITY_SERVER_SIDE_GEMINI_API"]
}
"""

# 3. README.md
FILES["README.md"] = """# MIRA AI - Personal Autonomous Video Editing Agent for CapCut 🎬🤖

**MIRA AI** is an intelligent, free, native Android assistant that operates the **CapCut** app on your Android phone just like a human editor. It looks at the screen using an Accessibility Service, reasons about the next editing action using **OpenRouter** (defaulting to free models like `google/gemma-3-27b-it:free`), and performs taps, cuts, splits, speed curves (Velocity/Rampage), and transitions autonomously.

The entire user interface and interaction is in **Urdu (RTL)**, while the underlying Kotlin engine is engineered for rock-solid reliability, safety, and privacy.

---

## 🌟 Key Highlights & Architecture

- **Powered by OpenRouter**: Connects to `https://openrouter.ai/api/v1/chat/completions` supporting top free & premium models (default: `google/gemma-3-27b-it:free`).
- **Android Native**: Built with **Kotlin**, **Jetpack Compose (Material 3)**, and **Coroutines**.
- **Eyes & Hands**: Uses `MiraAccessibilityService` (`minSdk 30`) with `canTakeScreenshot` and `dispatchGesture`.
- **Dual Observation Strategy**: Analyzes the fast Android UI accessibility node tree first; falls back to downscaled 1080p JPEG screenshots when inspecting custom canvas elements like CapCut's timeline.
- **Robust JSON Action Protocol**: Does not rely on rigid JSON schemas that break on free models; cleans markdown fences, extracts outermost `{...}`, and automatically retries with strict reminders.
- **Detailed Error Logging**: For any non-200 response, logs both the HTTP status code and the first 300 characters of the response body into the Live Log. Includes exponential backoff for 429 rate limits and 5xx server issues.
- **Floating Overlay Bubble**: `SYSTEM_ALERT_WINDOW` floating widget showing current steps in Urdu with an instant **"روکیں" (STOP)** emergency button and pause/resume.
- **Strict Safety Gate**: Requires explicit Urdu approval before saving, exporting, or making changes outside the project.
- **Local Learning Memory**: Caches successful UI coordinates and button identifiers in a local JSON skills store to save API quota.

---

## 🔒 Privacy Notice (رازداری کا نوٹس)

> **اردو:** ویڈیو ایڈیٹنگ کے دوران اسکرین شاٹس اور UI معلومات صرف OpenRouter اور آپ کے منتخب کردہ AI ماڈل پرووائیڈر کو محفوظ طریقے سے بھیجی جاتی ہیں۔ آپ کی OpenRouter API کی آپ کے فون کے محفوظ Android Keystore میں محفوظ رہتی ہے اور کسی دیگر سرور پر شیئر نہیں کی جاتی۔

- **API Key Storage**: Stored locally in `EncryptedSharedPreferences` backed by the **Android Keystore (AES-256 GCM)**. Never logged, never transmitted anywhere except directly to OpenRouter.
- **Data Transmission**: Screenshots and UI trees are sent exclusively to OpenRouter's endpoint with HTTPS encryption.

---

## 🚀 How to Build and Download the APK for Free (GitHub Actions)

You do not need Android Studio installed on your computer. You can build the APK directly on GitHub using the included workflow:

### Step 1: Push or Upload Project to GitHub
1. Create a new GitHub repository (public or private).
2. Push this folder to your repository, or upload the files directly via GitHub's web interface.

### Step 2: Run GitHub Actions Workflow
1. Go to your repository on GitHub.
2. Click on the **Actions** tab.
3. Select **"Build MIRA AI APK"** from the left sidebar.
4. Click **Run workflow** -> Select `main` branch -> Click **Run workflow**.

### Step 3: Download and Install APK
1. When the workflow finishes (typically ~2-3 minutes with green checkmark), click on the completed run.
2. Scroll to the bottom to find **Artifacts**.
3. Download **`MIRA-AI-debug-apk`**.
4. Unzip the downloaded file to get `app-debug.apk` and transfer/open it on your Android phone to install.

---

## 📲 First-Run Setup & Onboarding Wizard (Urdu)

When you first launch **MIRA AI**, complete the 5 simple setup steps:

1. **OpenRouter API Key**:
   - Go to [openrouter.ai/keys](https://openrouter.ai/keys) and create an API key (`sk-or-v1-...`).
   - Paste it in MIRA AI Settings. You can tap **"API کی ٹیسٹ کریں"** to verify connection via `GET https://openrouter.ai/api/v1/auth/key`.
2. **Notifications**: Allow notification access so MIRA can run in the foreground.
3. **Display Over Other Apps (Overlay)**: Enable permission to show the floating control bubble over CapCut.
4. **Accessibility Service**:
   - Turn ON **"MIRA AI"** in Accessibility settings.
   - **Note for Android 13+ Users**: If the switch is greyed out ("Restricted setting"):
     - Go to phone **Settings** > **Apps** > **MIRA AI**.
     - Tap the **3-dots menu** at the top right.
     - Tap **"Allow restricted settings"** and verify with fingerprint/PIN.
     - Return to Accessibility and turn on the switch!
5. **Open CapCut**: Ensure CapCut is installed and has been opened at least once.

---

## 🤖 Recommended OpenRouter Models

In Settings, you can configure any model on OpenRouter:
- `google/gemma-3-27b-it:free` (Default: fast, free, excellent reasoning)
- `meta-llama/llama-3.3-70b-instruct:free` (High reasoning capacity)
- `deepseek/deepseek-r1:free` (Deep reasoning)
- Any paid vision-capable model (e.g., `google/gemini-2.0-flash-001`, `anthropic/claude-3.5-sonnet`)

---

## 🧪 10-Second Test Checklist (Run on Your Phone)

Use this quick verification procedure with a 10-second test video:

1. [ ] **Verify Status**: Launch MIRA AI. Ensure the Home card says **"MIRA تیار ہے"** with green indicators.
2. [ ] **Test API Key**: Go to Settings, enter your key, tap **"API کی ٹیسٹ کریں"**, confirm green success.
3. [ ] **Start New Edit**: Tap **"نیا ایڈٹ شروع کریں"**.
4. [ ] **Step 1**: Pick your 10-second video from the Gallery and enter a title.
5. [ ] **Step 2**: Enter cut timing: `2.5, 5.0, 7.5`.
6. [ ] **Step 3**: Select style: **وائلوسیٹی (Velocity)** or **ریمپیج (Rampage)**.
7. [ ] **Step 4**: Enter note: *"Fast cuts with smooth zoom"*.
8. [ ] **Step 5**: Tap **"شروع کریں"**.
9. [ ] **Observe Floating Bubble**: Notice CapCut opens automatically and the floating bubble displays Urdu progress.
10. [ ] **Test Stop Button**: Tap the red **"روکیں"** button at any point to verify immediate cancellation.
11. [ ] **Check Live Logs**: Re-open MIRA AI and switch to the **"لائیو لاگ"** tab to see every action and API response snippet.
"""

# 4. strings.xml
FILES["app/src/main/res/values/strings.xml"] = """<resources>
    <string name="app_name">MIRA AI</string>
    <string name="accessibility_service_description">میرا اے آئی (MIRA AI) خودکار ویڈیو ایڈیٹنگ کے لیے CapCut میں اسکرین پڑھ کر اشارے اور کٹس انجام دیتی ہے۔</string>

    <string name="nav_home">مرکزی صفحہ</string>
    <string name="nav_new_edit">نیا ایڈٹ</string>
    <string name="nav_logs">لائیو لاگ</string>
    <string name="nav_settings">ترتیبات</string>

    <string name="status_ready">MIRA تیار ہے</string>
    <string name="status_off">MIRA بند ہے</string>
    <string name="status_ready_desc">تمام اجازتیں اور API کی فعال ہیں۔ آپ نیا ایڈیٹنگ ٹاسک شروع کر سکتے ہیں۔</string>
    <string name="status_off_desc">کچھ اہم اجازتیں یا ترتیبات باقی ہیں۔ نیچے دیے گئے بٹن سے سیٹ اپ مکمل کریں۔</string>
    <string name="permission_accessibility">رسائی سروس (Accessibility Service)</string>
    <string name="permission_overlay">اسکرین اوورلے (Display Over Other Apps)</string>
    <string name="permission_api_key">اوپن راؤٹر کی (OpenRouter API Key)</string>
    <string name="permission_notification">اطلاعات (Notifications)</string>
    <string name="btn_fix">سیٹ کریں</string>
    <string name="btn_start_new_edit">نیا ایڈٹ شروع کریں</string>
    <string name="recent_jobs_title">حالیہ ایڈیٹنگ ٹاسکس</string>
    <string name="no_recent_jobs">ابھی تک کوئی ٹاسک نہیں چلایا گیا</string>

    <string name="step_1_title">1. آج کون سی ویڈیو بنانی ہے؟</string>
    <string name="step_1_pick_video">گیلری سے ویڈیو منتخب کریں</string>
    <string name="step_1_note_hint">ویڈیو کا خیال یا تھیم لکھیں (مثلاً موٹر بائیک ڈرائیو یا ایونٹ کلپ)...</string>
    <string name="step_2_title">2. کٹ کس سیکنڈ پر لگانے ہیں؟</string>
    <string name="step_2_hint">کٹ سیکنڈز لکھیں، مثلاً: 2.5, 5.0, 7.8 (اختیاری)</string>
    <string name="step_3_title">3. کون سا اسٹائل؟</string>
    <string name="step_4_title">4. کوئی خاص ہدایت؟</string>
    <string name="step_4_hint">مثلاً: فلٹر، موسیقی، سلو مو، آٹو کیپشن یا ٹیکسٹ وغیرہ...</string>
    <string name="step_5_title">5. ایڈیٹنگ پلان کا جائزہ</string>
    <string name="btn_start_job">شروع کریں</string>
    <string name="btn_next">اگلا مرحلہ</string>
    <string name="btn_prev">پچھلا مرحلہ</string>

    <string name="style_auto">MIRA خود فیصلہ کرے</string>
    <string name="style_rampage">ریمپیج (Rampage)</string>
    <string name="style_velocity">وائلوسیٹی (Velocity)</string>
    <string name="style_slomo">اسموتھ سلو مو (Smooth Slow-Mo)</string>
    <string name="style_cinematic">سنیماٹک (Cinematic)</string>

    <string name="settings_title">ترتیبات اور ماڈل</string>
    <string name="setting_api_key_label">OpenRouter API Key</string>
    <string name="setting_api_key_hint">OpenRouter سے حاصل کردہ کی یہاں پیسٹ کریں (sk-or-v1-...)</string>
    <string name="setting_model_label">ماڈل کا نام (OpenRouter Model)</string>
    <string name="setting_delay_label">ہر ایکشن میں وقفہ (ملی سیکنڈ)</string>
    <string name="setting_max_steps_label">زیادہ سے زیادہ مراحل (Max Steps)</string>
    <string name="setting_max_retries_label">زیادہ سے زیادہ کوششیں (Retries)</string>
    <string name="setting_ask_export_label">ایکسپورٹ سے پہلے مجھ سے اجازت لیں</string>
    <string name="setting_proactive_label">خود سے بہتری تجویز کریں</string>
    <string name="setting_capcut_pkg_label">CapCut پیکیج منتخب کریں</string>
    <string name="btn_test_api_key">API کی ٹیسٹ کریں</string>
    <string name="btn_reset_memory">سیکھی ہوئی میموری صاف کریں</string>
    <string name="api_test_success">ماشاءاللہ! API کی بالکل درست ہے اور OpenRouter سے رابطہ ہو گیا ہے۔</string>
    <string name="api_test_failed">OpenRouter API کی کی تصدیق ناکام ہو گئی۔ براہ کرم کی درستگی چیک کریں۔</string>
    <string name="privacy_note_title">رازداری کا نوٹس (Privacy Note)</string>
    <string name="privacy_note_desc">ویڈیو ایڈیٹنگ کے دوران اسکرین شاٹس اور UI معلومات OpenRouter اور آپ کے منتخب کردہ AI ماڈل پرووائیڈر کو محفوظ طریقے سے بھیجی جاتی ہیں۔ آپ کی کی صرف آپ کے آلے میں محفوظ رہتی ہے۔</string>

    <string name="logs_title">لائیو لاگ اور ایکشن ہسٹری</string>
    <string name="btn_share_logs">لاگ شیئر / محفوظ کریں</string>
    <string name="btn_clear_logs">لاگ صاف کریں</string>
    <string name="no_logs_yet">کوئی ایکشن لاگ موجود نہیں</string>

    <string name="overlay_stop">روکیں</string>
    <string name="overlay_pause">وقفہ</string>
    <string name="overlay_resume">جاری رکھیں</string>
    <string name="overlay_waiting">MIRA انتظار کر رہی ہے...</string>
    <string name="overlay_working">MIRA کام کر رہی ہے...</string>
    <string name="overlay_permission_needed">اجازت درکار ہے: کیا MIRA ایکسپورٹ / محفوظ کرے؟</string>
    <string name="btn_confirm_yes">ہاں، اجازت دیں</string>
    <string name="btn_confirm_no">نہیں، منسوخ کریں</string>

    <string name="onboarding_title">MIRA AI سیٹ اپ ویژرڈ</string>
    <string name="onboarding_step1">1. OpenRouter API کی شامل کریں (openrouter.ai سے حاصل کریں)</string>
    <string name="onboarding_step2">2. اطلاعات (Notifications) کی اجازت دیں</string>
    <string name="onboarding_step3">3. دیگر ایپس پر ظاہر ہونے کی اجازت (Overlay)</string>
    <string name="onboarding_step4">4. رسائی سروس (Accessibility Service) آن کریں</string>
    <string name="onboarding_step4_help">اگر آپ کا فون Android 13+ ہے اور سوئچ گرے ہے: فون کی Settings > Apps > MIRA AI > تین نقطوں (Three dots) پر ٹیپ کریں اور "Allow restricted settings" آن کریں۔</string>
    <string name="onboarding_step5">5. CapCut کھولیں اور واپس آئیں</string>
    <string name="btn_open_settings">سیٹنگز کھولیں</string>
    <string name="btn_open_capcut">CapCut کھولیں</string>
    <string name="btn_complete_setup">سیٹ اپ مکمل ہوا</string>
</resources>
"""

# 5. OpenRouterClient.kt
FILES["app/src/main/java/com/example/network/OpenRouterClient.kt"] = """package com.example.network

import com.example.model.ActionResponse
import com.example.model.ActionType
import com.example.model.EditJob
import com.example.model.ObservationResult
import com.example.model.StepLog
import kotlinx.coroutines.delay
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONArray
import org.json.JSONObject
import java.io.IOException
import java.util.concurrent.TimeUnit

class OpenRouterClient(
    private val defaultSystemPrompt: String
) {
    private val client = OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(60, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        .build()

    private val jsonMediaType = "application/json; charset=utf-8".toMediaType()

    companion object {
        private const val CHAT_COMPLETIONS_URL = "https://openrouter.ai/api/v1/chat/completions"
        private const val AUTH_KEY_URL = "https://openrouter.ai/api/v1/auth/key"
        private const val HTTP_REFERER = "https://github.com/mira-ai"
        private const val X_TITLE = "MIRA AI"
    }

    suspend fun decideNextAction(
        apiKey: String,
        modelName: String,
        job: EditJob,
        currentObservation: ObservationResult,
        history: List<StepLog>,
        sendScreenshot: Boolean,
        onWaitingRateLimit: (String) -> Unit = {},
        onHttpError: (Int, String) -> Unit = { _, _ -> }
    ): Pair<ActionResponse, Int> {
        var apiCallsMade = 0
        var attempt = 0
        val maxRetries = 3
        var backoffMs = 2000L

        val userPromptText = buildUserPromptText(job, currentObservation, history)

        while (attempt < maxRetries) {
            attempt++
            apiCallsMade++

            val requestBodyString = buildOpenRouterRequestBody(
                modelName = modelName,
                userPromptText = userPromptText,
                screenshotBase64 = if (sendScreenshot) currentObservation.screenshotBase64 else null
            )

            val request = Request.Builder()
                .url(CHAT_COMPLETIONS_URL)
                .addHeader("Authorization", "Bearer ${apiKey.trim()}")
                .addHeader("HTTP-Referer", HTTP_REFERER)
                .addHeader("X-Title", X_TITLE)
                .post(requestBodyString.toRequestBody(jsonMediaType))
                .build()

            try {
                client.newCall(request).execute().use { response ->
                    val code = response.code
                    val bodyString = response.body?.string() ?: ""

                    if (code != 200) {
                        val snippet = bodyString.take(300)
                        onHttpError(code, snippet)

                        if (code == 429 || code in 500..599) {
                            onWaitingRateLimit("MIRA انتظار کر رہی ہے... (اوپن راؤٹر بزی ہے، کوڈ $code)")
                            delay(backoffMs)
                            backoffMs = (backoffMs * 2).coerceAtMost(16000L)
                            return@use
                        }

                        if (attempt >= maxRetries) {
                            return Pair(
                                ActionResponse(
                                    thoughtUrdu = "اوپن راؤٹر سرور نے خرابی دی: کوڈ $code",
                                    screenSummary = "HTTP $code: $snippet",
                                    action = ActionType.FAIL
                                ),
                                apiCallsMade
                            )
                        }
                        delay(1000L)
                        return@use
                    }

                    val rawContent = extractContentFromResponse(bodyString)
                    val parsedAction = parseActionJson(rawContent)

                    if (parsedAction != null) {
                        return Pair(parsedAction, apiCallsMade)
                    }

                    // Retry once with a stricter reminder if parsing fails
                    if (rawContent != null && attempt < maxRetries) {
                        apiCallsMade++
                        val retryResponse = executeStricterJsonRetry(apiKey, modelName, rawContent)
                        if (retryResponse != null) {
                            return Pair(retryResponse, apiCallsMade)
                        }
                    }

                    if (attempt < maxRetries) {
                        delay(1000L)
                    }
                }
            } catch (e: IOException) {
                onHttpError(0, "Network error: ${e.message?.take(300)}")
                if (attempt >= maxRetries) {
                    return Pair(
                        ActionResponse(
                            thoughtUrdu = "انٹرنیٹ کنکشن میں مسئلہ ہے",
                            screenSummary = "Network error: ${e.message}",
                            action = ActionType.WAIT
                        ),
                        apiCallsMade
                    )
                }
                delay(backoffMs)
            }
        }

        return Pair(
            ActionResponse(
                thoughtUrdu = "کارروائی کا فیصلہ نہیں ہو سکا، براہ کرم مدد کریں۔",
                screenSummary = "Failed to parse action from OpenRouter after retries",
                action = ActionType.ASK_USER
            ),
            apiCallsMade
        )
    }

    suspend fun testApiKey(apiKey: String): Pair<Boolean, String> {
        val trimmed = apiKey.trim()
        if (trimmed.isBlank()) {
            return Pair(false, "API Key خالی ہے")
        }

        val request = Request.Builder()
            .url(AUTH_KEY_URL)
            .addHeader("Authorization", "Bearer $trimmed")
            .addHeader("HTTP-Referer", HTTP_REFERER)
            .addHeader("X-Title", X_TITLE)
            .get()
            .build()

        return try {
            client.newCall(request).execute().use { response ->
                val code = response.code
                val bodyString = response.body?.string() ?: ""

                if (response.isSuccessful) {
                    val labelInfo = try {
                        val root = JSONObject(bodyString)
                        val data = root.optJSONObject("data")
                        val label = data?.optString("label")
                        if (!label.isNullOrBlank()) " ($label)" else ""
                    } catch (_: Exception) { "" }

                    Pair(true, "ماشاءاللہ! API کی درست ہے اور OpenRouter سے رابطہ ہو گیا ہے۔$labelInfo")
                } else {
                    val errorSnippet = bodyString.take(300)
                    Pair(false, "خرابی: HTTP $code - $errorSnippet")
                }
            }
        } catch (e: Exception) {
            Pair(false, "رابطہ ناکام: ${e.message?.take(300)}")
        }
    }

    private fun buildUserPromptText(
        job: EditJob,
        observation: ObservationResult,
        history: List<StepLog>
    ): String {
        val promptBuilder = StringBuilder()
        promptBuilder.appendLine("=== CURRENT VIDEO EDITING JOB ===")
        promptBuilder.appendLine("Theme / Note: ${job.videoNote}")
        promptBuilder.appendLine("Cut Timings (seconds): ${job.cutTimings.ifBlank { "None specified" }}")
        promptBuilder.appendLine("Target Style: ${job.style}")
        promptBuilder.appendLine("Special Instructions: ${job.instructions.ifBlank { "None" }}")
        promptBuilder.appendLine("Foreground Package: ${observation.packageName}")
        promptBuilder.appendLine()

        promptBuilder.appendLine("=== RECENT STEPS HISTORY (Last 8) ===")
        if (history.isEmpty()) {
            promptBuilder.appendLine("Job just started. No previous actions taken.")
        } else {
            for (step in history.takeLast(8)) {
                promptBuilder.appendLine("Step ${step.stepNumber}: Action=${step.actionName}, Result=${step.resultUrdu}, Summary=${step.screenSummary}")
            }
        }
        promptBuilder.appendLine()

        promptBuilder.appendLine("=== CURRENT SCREEN UI TREE (JSON) ===")
        promptBuilder.appendLine(observation.treeJson)
        promptBuilder.appendLine()
        promptBuilder.appendLine("Inspect the UI tree and screenshot (if provided). Output the single next JSON action object.")
        promptBuilder.appendLine("IMPORTANT: Respond with ONLY the single raw JSON object. Do not wrap in markdown or backticks, do not include any explanatory text.")
        return promptBuilder.toString()
    }

    private fun buildOpenRouterRequestBody(
        modelName: String,
        userPromptText: String,
        screenshotBase64: String?
    ): String {
        val root = JSONObject()
        root.put("model", modelName.trim().ifBlank { "google/gemma-3-27b-it:free" })

        val messages = JSONArray()

        val systemMessage = JSONObject().apply {
            put("role", "system")
            put("content", defaultSystemPrompt)
        }
        messages.put(systemMessage)

        val userMessage = JSONObject().apply {
            put("role", "user")
            if (!screenshotBase64.isNullOrBlank()) {
                val contents = JSONArray()
                contents.put(JSONObject().apply {
                    put("type", "text")
                    put("text", userPromptText)
                })
                contents.put(JSONObject().apply {
                    put("type", "image_url")
                    put("image_url", JSONObject().apply {
                        put("url", "data:image/jpeg;base64,$screenshotBase64")
                    })
                })
                put("content", contents)
            } else {
                put("content", userPromptText)
            }
        }
        messages.put(userMessage)

        root.put("messages", messages)
        root.put("temperature", 0.2)

        return root.toString()
    }

    private suspend fun executeStricterJsonRetry(
        apiKey: String,
        modelName: String,
        previousMalformedContent: String
    ): ActionResponse? {
        val root = JSONObject()
        root.put("model", modelName.trim().ifBlank { "google/gemma-3-27b-it:free" })

        val messages = JSONArray()
        messages.put(JSONObject().apply {
            put("role", "system")
            put("content", defaultSystemPrompt)
        })
        messages.put(JSONObject().apply {
            put("role", "assistant")
            put("content", previousMalformedContent.take(500))
        })
        messages.put(JSONObject().apply {
            put("role", "user")
            put("content", "CRITICAL ERROR: Your previous response was not valid JSON. You MUST output ONLY the raw JSON object starting with { and ending with }. No code fences, no commentary.")
        })
        root.put("messages", messages)
        root.put("temperature", 0.1)

        val request = Request.Builder()
            .url(CHAT_COMPLETIONS_URL)
            .addHeader("Authorization", "Bearer ${apiKey.trim()}")
            .addHeader("HTTP-Referer", HTTP_REFERER)
            .addHeader("X-Title", X_TITLE)
            .post(root.toString().toRequestBody(jsonMediaType))
            .build()

        return try {
            client.newCall(request).execute().use { response ->
                if (!response.isSuccessful) return null
                val body = response.body?.string() ?: return null
                val content = extractContentFromResponse(body) ?: return null
                parseActionJson(content)
            }
        } catch (_: Exception) {
            null
        }
    }

    private fun extractContentFromResponse(responseBody: String): String? {
        return try {
            val root = JSONObject(responseBody)
            val choices = root.optJSONArray("choices") ?: return null
            if (choices.length() == 0) return null
            val message = choices.getJSONObject(0).optJSONObject("message") ?: return null
            message.optString("content", null)
        } catch (_: Exception) {
            null
        }
    }

    private fun parseActionJson(rawText: String?): ActionResponse? {
        if (rawText.isNullOrBlank()) return null
        return try {
            val jsonObject = extractFirstJsonObject(rawText) ?: return null

            val thoughtUrdu = jsonObject.optString("thought_urdu", "MIRA اگلا قدم اٹھا رہی ہے...")
            val screenSummary = jsonObject.optString("screen_summary", "CapCut screen active")
            val actionStr = jsonObject.optString("action", "wait")
            val actionType = ActionType.fromString(actionStr)

            val x = if (jsonObject.has("x") && !jsonObject.isNull("x")) jsonObject.optDouble("x").toFloat() else null
            val y = if (jsonObject.has("y") && !jsonObject.isNull("y")) jsonObject.optDouble("y").toFloat() else null
            val x2 = if (jsonObject.has("x2") && !jsonObject.isNull("x2")) jsonObject.optDouble("x2").toFloat() else null
            val y2 = if (jsonObject.has("y2") && !jsonObject.isNull("y2")) jsonObject.optDouble("y2").toFloat() else null
            val durationMs = if (jsonObject.has("duration_ms") && !jsonObject.isNull("duration_ms")) jsonObject.optLong("duration_ms") else null
            val txt = if (jsonObject.has("text") && !jsonObject.isNull("text")) jsonObject.optString("text") else null
            val targetNodeIdx = if (jsonObject.has("target_node_index") && !jsonObject.isNull("target_node_index")) jsonObject.optInt("target_node_index") else null
            val expected = jsonObject.optString("expected_result", "")
            val progress = jsonObject.optInt("progress_percent", 0).coerceIn(0, 100)

            ActionResponse(
                thoughtUrdu = thoughtUrdu,
                screenSummary = screenSummary,
                action = actionType,
                x = x,
                y = y,
                x2 = x2,
                y2 = y2,
                durationMs = durationMs,
                text = txt,
                targetNodeIndex = targetNodeIdx,
                expectedResult = expected,
                progressPercent = progress
            )
        } catch (_: Exception) {
            null
        }
    }

    private fun extractFirstJsonObject(rawText: String): JSONObject? {
        var clean = rawText.trim()

        if (clean.contains("```")) {
            val startIndex = clean.indexOf("```")
            val nextLine = clean.indexOf('\\n', startIndex)
            if (nextLine != -1) {
                val afterFence = clean.substring(nextLine + 1)
                val endIndex = afterFence.lastIndexOf("```")
                clean = if (endIndex != -1) {
                    afterFence.substring(0, endIndex).trim()
                } else {
                    afterFence.trim()
                }
            }
        }

        try {
            return JSONObject(clean)
        } catch (_: Exception) {}

        val start = clean.indexOf('{')
        val end = clean.lastIndexOf('}')
        if (start != -1 && end != -1 && end > start) {
            val candidate = clean.substring(start, end + 1)
            try {
                return JSONObject(candidate)
            } catch (_: Exception) {}
        }

        return null
    }
}
"""

# 6. SecureStore.kt
FILES["app/src/main/java/com/example/data/SecureStore.kt"] = """package com.example.data

import android.content.Context
import android.content.SharedPreferences
import android.content.pm.PackageManager
import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import android.util.Base64
import com.example.model.EditJob
import com.example.model.JobStatus
import org.json.JSONArray
import org.json.JSONObject
import java.security.KeyStore
import javax.crypto.Cipher
import javax.crypto.KeyGenerator
import javax.crypto.SecretKey
import javax.crypto.spec.GCMParameterSpec

class SecureStore(private val context: Context) {

    private val prefs: SharedPreferences = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)

    companion object {
        private const val PREFS_NAME = "mira_secure_prefs"
        private const val KEY_ALIAS = "mira_gemini_key_alias"
        private const val ANDROID_KEYSTORE = "AndroidKeyStore"
        private const val AES_GCM_NO_PADDING = "AES/GCM/NoPadding"
        private const val GCM_IV_LENGTH = 12
        private const val GCM_TAG_LENGTH = 128

        private const val PREF_ENCRYPTED_API_KEY = "encrypted_api_key"
        private const val PREF_IV = "api_key_iv"
        private const val PREF_MODEL_NAME = "model_name"
        private const val PREF_STEP_DELAY = "step_delay_ms"
        private const val PREF_MAX_STEPS = "max_steps"
        private const val PREF_MAX_RETRIES = "max_retries"
        private const val PREF_ASK_EXPORT = "ask_permission_before_export"
        private const val PREF_PROACTIVE = "proactive_improvements"
        private const val PREF_CAPCUT_PKG = "selected_capcut_package"
        private const val PREF_RECENT_JOBS = "recent_jobs_json"
        private const val PREF_ONBOARDING_DONE = "onboarding_completed"

        val KNOWN_CAPCUT_PACKAGES = listOf(
            "com.lemon.lvoverseas",
            "com.lemon.lvoverseas.lite",
            "com.capcut.videoeditor",
            "com.lemon.kinevideo"
        )
    }

    init {
        ensureKeyStoreKey()
    }

    private fun ensureKeyStoreKey() {
        try {
            val keyStore = KeyStore.getInstance(ANDROID_KEYSTORE).apply { load(null) }
            if (!keyStore.containsAlias(KEY_ALIAS)) {
                val keyGenerator = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, ANDROID_KEYSTORE)
                val keyGenParameterSpec = KeyGenParameterSpec.Builder(
                    KEY_ALIAS,
                    KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT
                )
                    .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
                    .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
                    .setKeySize(256)
                    .build()
                keyGenerator.init(keyGenParameterSpec)
                keyGenerator.generateKey()
            }
        } catch (_: Exception) {}
    }

    private fun getSecretKey(): SecretKey? {
        return try {
            val keyStore = KeyStore.getInstance(ANDROID_KEYSTORE).apply { load(null) }
            (keyStore.getEntry(KEY_ALIAS, null) as? KeyStore.SecretKeyEntry)?.secretKey
        } catch (_: Exception) {
            null
        }
    }

    fun saveApiKey(rawKey: String) {
        if (rawKey.isBlank()) {
            prefs.edit().remove(PREF_ENCRYPTED_API_KEY).remove(PREF_IV).apply()
            return
        }
        try {
            val key = getSecretKey() ?: return
            val cipher = Cipher.getInstance(AES_GCM_NO_PADDING)
            cipher.init(Cipher.ENCRYPT_MODE, key)
            val iv = cipher.iv
            val encryptedBytes = cipher.doFinal(rawKey.trim().toByteArray(Charsets.UTF_8))

            val ivBase64 = Base64.encodeToString(iv, Base64.NO_WRAP)
            val encryptedBase64 = Base64.encodeToString(encryptedBytes, Base64.NO_WRAP)

            prefs.edit()
                .putString(PREF_ENCRYPTED_API_KEY, encryptedBase64)
                .putString(PREF_IV, ivBase64)
                .apply()
        } catch (_: Exception) {}
    }

    fun getApiKey(): String {
        val encryptedBase64 = prefs.getString(PREF_ENCRYPTED_API_KEY, null) ?: return ""
        val ivBase64 = prefs.getString(PREF_IV, null) ?: return ""
        return try {
            val key = getSecretKey() ?: return ""
            val iv = Base64.decode(ivBase64, Base64.NO_WRAP)
            val encryptedBytes = Base64.decode(encryptedBase64, Base64.NO_WRAP)

            val cipher = Cipher.getInstance(AES_GCM_NO_PADDING)
            val spec = GCMParameterSpec(GCM_TAG_LENGTH, iv)
            cipher.init(Cipher.DECRYPT_MODE, key, spec)
            val decryptedBytes = cipher.doFinal(encryptedBytes)
            String(decryptedBytes, Charsets.UTF_8)
        } catch (_: Exception) {
            ""
        }
    }

    fun getMaskedApiKey(): String {
        val key = getApiKey()
        if (key.length <= 8) return if (key.isNotEmpty()) "••••••••" else ""
        return "${key.take(4)}••••••••${key.takeLast(4)}"
    }

    var modelName: String
        get() = prefs.getString(PREF_MODEL_NAME, "google/gemma-3-27b-it:free") ?: "google/gemma-3-27b-it:free"
        set(value) = prefs.edit().putString(PREF_MODEL_NAME, value.trim()).apply()

    var stepDelayMs: Long
        get() = prefs.getLong(PREF_STEP_DELAY, 1200L)
        set(value) = prefs.edit().putLong(PREF_STEP_DELAY, value).apply()

    var maxSteps: Int
        get() = prefs.getInt(PREF_MAX_STEPS, 120)
        set(value) = prefs.edit().putInt(PREF_MAX_STEPS, value).apply()

    var maxRetries: Int
        get() = prefs.getInt(PREF_MAX_RETRIES, 3)
        set(value) = prefs.edit().putInt(PREF_MAX_RETRIES, value).apply()

    var askBeforeExport: Boolean
        get() = prefs.getBoolean(PREF_ASK_EXPORT, true)
        set(value) = prefs.edit().putBoolean(PREF_ASK_EXPORT, value).apply()

    var proactiveImprovements: Boolean
        get() = prefs.getBoolean(PREF_PROACTIVE, true)
        set(value) = prefs.edit().putBoolean(PREF_PROACTIVE, value).apply()

    var capcutPackage: String
        get() = prefs.getString(PREF_CAPCUT_PKG, "com.lemon.lvoverseas") ?: "com.lemon.lvoverseas"
        set(value) = prefs.edit().putString(PREF_CAPCUT_PKG, value.trim()).apply()

    var onboardingCompleted: Boolean
        get() = prefs.getBoolean(PREF_ONBOARDING_DONE, false)
        set(value) = prefs.edit().putBoolean(PREF_ONBOARDING_DONE, value).apply()

    fun getInstalledCapCutVariants(): List<String> {
        val pm = context.packageManager
        val installed = mutableListOf<String>()
        for (pkg in KNOWN_CAPCUT_PACKAGES) {
            try {
                pm.getPackageInfo(pkg, 0)
                installed.add(pkg)
            } catch (_: PackageManager.NameNotFoundException) {}
        }
        return if (installed.isEmpty()) listOf("com.lemon.lvoverseas") else installed
    }

    fun saveRecentJob(job: EditJob) {
        val jobs = getRecentJobs().toMutableList()
        jobs.removeAll { it.id == job.id }
        jobs.add(0, job)
        val trimmed = jobs.take(5)

        val array = JSONArray()
        for (item in trimmed) {
            val obj = JSONObject().apply {
                put("id", item.id)
                put("videoUri", item.videoUri ?: "")
                put("videoNote", item.videoNote)
                put("cutTimings", item.cutTimings)
                put("style", item.style)
                put("instructions", item.instructions)
                put("status", item.status.name)
                put("progress", item.progress)
                put("createdAt", item.createdAt)
                put("apiCallsCount", item.apiCallsCount)
            }
            array.put(obj)
        }
        prefs.edit().putString(PREF_RECENT_JOBS, array.toString()).apply()
    }

    fun getRecentJobs(): List<EditJob> {
        val json = prefs.getString(PREF_RECENT_JOBS, null) ?: return emptyList()
        val list = mutableListOf<EditJob>()
        try {
            val array = JSONArray(json)
            for (i in 0 until array.length()) {
                val obj = array.getJSONObject(i)
                list.add(
                    EditJob(
                        id = obj.optString("id"),
                        videoUri = obj.optString("videoUri").ifBlank { null },
                        videoNote = obj.optString("videoNote"),
                        cutTimings = obj.optString("cutTimings"),
                        style = obj.optString("style", "MIRA خود فیصلہ کرے"),
                        instructions = obj.optString("instructions"),
                        status = try {
                            JobStatus.valueOf(obj.optString("status", JobStatus.IDLE.name))
                        } catch (_: Exception) {
                            JobStatus.IDLE
                        },
                        progress = obj.optInt("progress", 0),
                        createdAt = obj.optLong("createdAt", System.currentTimeMillis()),
                        apiCallsCount = obj.optInt("apiCallsCount", 0)
                    )
                )
            }
        } catch (_: Exception) {}
        return list
    }
}
"""

# 7. AgentRunner.kt
FILES["app/src/main/java/com/example/agent/AgentRunner.kt"] = """package com.example.agent

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
import com.example.network.OpenRouterClient
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

        val openRouterClient = OpenRouterClient(systemPrompt)
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

            val (decision, callsUsed) = openRouterClient.decideNextAction(
                apiKey = apiKey,
                modelName = secureStore.modelName,
                job = _currentJob.value ?: initialJob,
                currentObservation = observation,
                history = _logs.value,
                sendScreenshot = needScreenshot,
                onWaitingRateLimit = { waitingMsg ->
                    updateOverlay(context, waitingMsg)
                },
                onHttpError = { code, snippet ->
                    addLog(
                        stepNumber = stepNumber,
                        thoughtUrdu = "اوپن راؤٹر سرور سے خرابی موصول ہوئی (کوڈ $code)",
                        screenSummary = "HTTP $code: $snippet",
                        actionName = "API_ERROR",
                        isSuccess = false,
                        apiCalls = totalApiCalls
                    )
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
"""

# 8. HomeScreen.kt
FILES["app/src/main/java/com/example/ui/screens/HomeScreen.kt"] = """package com.example.ui.screens

import android.content.Context
import android.content.Intent
import android.net.Uri
import android.provider.Settings
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Accessibility
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.Key
import androidx.compose.material.icons.filled.Layers
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.data.SecureStore
import com.example.model.EditJob
import com.example.model.JobStatus
import com.example.service.MiraAccessibilityService
import com.example.service.OverlayService
import com.example.ui.theme.CyanGlow
import com.example.ui.theme.EmeraldSuccess
import com.example.ui.theme.MagentaNeon
import com.example.ui.theme.MidnightDark
import com.example.ui.theme.RoseError
import com.example.ui.theme.SurfaceDark
import com.example.ui.theme.SurfaceElevated
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

@Composable
fun HomeScreen(
    onNavigateToNewEdit: () -> Unit,
    onNavigateToSettings: () -> Unit,
    onNavigateToOnboarding: () -> Unit,
    modifier: Modifier = Modifier
) {
    val context = LocalContext.current
    val secureStore = remember { SecureStore(context) }

    var isAccessibilityEnabled by remember { mutableStateOf(false) }
    var isOverlayEnabled by remember { mutableStateOf(false) }
    var isApiKeySet by remember { mutableStateOf(false) }
    var recentJobs by remember { mutableStateOf<List<EditJob>>(emptyList()) }

    fun refreshStatus() {
        isAccessibilityEnabled = MiraAccessibilityService.isServiceRunning()
        isOverlayEnabled = OverlayService.canDrawOverlays(context)
        isApiKeySet = secureStore.getApiKey().isNotBlank()
        recentJobs = secureStore.getRecentJobs()
    }

    LaunchedEffect(Unit) {
        refreshStatus()
    }

    val isAllReady = isAccessibilityEnabled && isOverlayEnabled && isApiKeySet

    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .background(MidnightDark)
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        item {
            Card(
                colors = CardDefaults.cardColors(
                    containerColor = if (isAllReady) SurfaceDark else SurfaceElevated
                ),
                shape = RoundedCornerShape(24.dp),
                modifier = Modifier
                    .fillMaxWidth()
                    .testTag("status_card")
            ) {
                Column(
                    modifier = Modifier.padding(20.dp),
                    horizontalAlignment = Alignment.Start
                ) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween,
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Box(
                                modifier = Modifier
                                    .size(16.dp)
                                    .clip(CircleShape)
                                    .background(if (isAllReady) EmeraldSuccess else RoseError)
                            )
                            Spacer(modifier = Modifier.width(10.dp))
                            Text(
                                text = if (isAllReady) "MIRA تیار ہے" else "MIRA بند ہے",
                                fontSize = 22.sp,
                                fontWeight = FontWeight.Bold,
                                color = Color.White
                            )
                        }

                        if (!isAllReady) {
                            OutlinedButton(
                                onClick = onNavigateToOnboarding,
                                shape = RoundedCornerShape(16.dp)
                            ) {
                                Text("سیٹ اپ ویژرڈ", color = CyanGlow, fontSize = 12.sp)
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(10.dp))

                    Text(
                        text = if (isAllReady)
                            "تمام بنیادی شرائط اور OpenRouter کنکشن فعال ہیں۔ آپ براہ راست خودکار ایڈیٹنگ شروع کر سکتے ہیں۔"
                        else
                            "کچھ اہم ترتیبات مکمل نہیں ہیں۔ براہ کرم نیچے دیے گئے بٹنوں سے رسائی فعال کریں۔",
                        color = Color(0xFFCBD5E1),
                        fontSize = 14.sp,
                        lineHeight = 20.sp
                    )
                }
            }
        }

        item {
            Card(
                colors = CardDefaults.cardColors(containerColor = SurfaceDark),
                shape = RoundedCornerShape(20.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(
                    modifier = Modifier.padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    Text(
                        text = "ضروری اجازتیں اور ترتیبات",
                        fontSize = 16.sp,
                        fontWeight = FontWeight.Bold,
                        color = Color.White
                    )

                    StatusRow(
                        title = "رسائی سروس (Accessibility)",
                        isOk = isAccessibilityEnabled,
                        icon = Icons.Default.Accessibility,
                        onFix = {
                            val intent = Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS).apply {
                                flags = Intent.FLAG_ACTIVITY_NEW_TASK
                            }
                            context.startActivity(intent)
                        }
                    )

                    StatusRow(
                        title = "اوورلے کنٹرول (Display Over Apps)",
                        isOk = isOverlayEnabled,
                        icon = Icons.Default.Layers,
                        onFix = {
                            val intent = Intent(
                                Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                                Uri.parse("package:${context.packageName}")
                            ).apply {
                                flags = Intent.FLAG_ACTIVITY_NEW_TASK
                            }
                            context.startActivity(intent)
                        }
                    )

                    StatusRow(
                        title = "OpenRouter API Key",
                        isOk = isApiKeySet,
                        icon = Icons.Default.Key,
                        onFix = onNavigateToSettings
                    )
                }
            }
        }

        item {
            Button(
                onClick = onNavigateToNewEdit,
                enabled = isAllReady,
                colors = ButtonDefaults.buttonColors(
                    containerColor = CyanGlow,
                    disabledContainerColor = Color(0xFF334155)
                ),
                shape = RoundedCornerShape(20.dp),
                modifier = Modifier
                    .fillMaxWidth()
                    .height(58.dp)
                    .testTag("start_edit_button")
            ) {
                Icon(
                    imageVector = Icons.Default.Add,
                    contentDescription = null,
                    tint = if (isAllReady) MidnightDark else Color.Gray
                )
                Spacer(modifier = Modifier.width(8.dp))
                Text(
                    text = "نیا ایڈٹ شروع کریں",
                    fontSize = 18.sp,
                    fontWeight = FontWeight.Bold,
                    color = if (isAllReady) MidnightDark else Color.Gray
                )
            }
        }

        item {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "حالیہ ایڈیٹنگ ٹاسکس",
                    fontSize = 18.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.White
                )
            }
        }

        if (recentJobs.isEmpty()) {
            item {
                Card(
                    colors = CardDefaults.cardColors(containerColor = SurfaceDark),
                    shape = RoundedCornerShape(16.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(24.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = "ابھی تک کوئی ٹاسک نہیں چلایا گیا۔ نیا ایڈٹ شروع کریں پر ٹیپ کریں!",
                            color = Color(0xFF94A3B8),
                            fontSize = 13.sp
                        )
                    }
                }
            }
        } else {
            items(recentJobs) { job ->
                JobCard(job = job)
            }
        }

        item {
            Spacer(modifier = Modifier.height(16.dp))
        }
    }
}

@Composable
fun StatusRow(
    title: String,
    isOk: Boolean,
    icon: ImageVector,
    onFix: () -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(12.dp))
            .background(SurfaceElevated)
            .padding(12.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.weight(1f)
        ) {
            Icon(
                imageVector = icon,
                contentDescription = null,
                tint = if (isOk) EmeraldSuccess else RoseError,
                modifier = Modifier.size(22.dp)
            )
            Spacer(modifier = Modifier.width(10.dp))
            Text(
                text = title,
                color = Color.White,
                fontSize = 14.sp,
                fontWeight = FontWeight.Medium
            )
        }

        if (isOk) {
            Icon(
                imageVector = Icons.Default.CheckCircle,
                contentDescription = "فعال ہے",
                tint = EmeraldSuccess,
                modifier = Modifier.size(20.dp)
            )
        } else {
            Button(
                onClick = onFix,
                colors = ButtonDefaults.buttonColors(containerColor = MagentaNeon),
                shape = RoundedCornerShape(10.dp),
                contentPadding = androidx.compose.foundation.layout.PaddingValues(horizontal = 12.dp, vertical = 4.dp),
                modifier = Modifier.height(34.dp)
            ) {
                Text(
                    text = "سیٹ کریں",
                    fontSize = 12.sp,
                    color = Color.White,
                    fontWeight = FontWeight.Bold
                )
            }
        }
    }
}

@Composable
fun JobCard(job: EditJob) {
    val dateFormat = remember { SimpleDateFormat("d MMM, hh:mm a", Locale.getDefault()) }
    val dateString = remember(job.createdAt) { dateFormat.format(Date(job.createdAt)) }

    val statusColor = when (job.status) {
        JobStatus.COMPLETED -> EmeraldSuccess
        JobStatus.FAILED -> RoseError
        JobStatus.STOPPED -> Color(0xFFF59E0B)
        JobStatus.RUNNING -> CyanGlow
        JobStatus.PAUSED -> Color(0xFFF59E0B)
        JobStatus.WAITING_PERMISSION, JobStatus.WAITING_USER -> MagentaNeon
        JobStatus.IDLE -> Color.Gray
        else -> Color.Gray
    }

    val statusUrdu = when (job.status) {
        JobStatus.COMPLETED -> "مکمل ✓"
        JobStatus.FAILED -> "ناکام ✗"
        JobStatus.STOPPED -> "روکا گیا"
        JobStatus.RUNNING -> "جاری ہے..."
        JobStatus.PAUSED -> "وقفہ"
        JobStatus.WAITING_PERMISSION -> "اجازت درکار"
        JobStatus.WAITING_USER -> "صارف کا انتظار"
        JobStatus.IDLE -> "غیر فعال"
        else -> "غیر فعال"
    }

    Card(
        colors = CardDefaults.cardColors(containerColor = SurfaceDark),
        shape = RoundedCornerShape(16.dp),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = job.videoNote.ifBlank { "ویڈیو ایڈیٹنگ ٹاسک" },
                    fontSize = 15.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.White
                )

                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(8.dp))
                        .background(statusColor.copy(alpha = 0.2f))
                        .padding(horizontal = 8.dp, vertical = 3.dp)
                ) {
                    Text(
                        text = statusUrdu,
                        color = statusColor,
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Bold
                    )
                }
            }

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(
                    text = "اسٹائل: ${job.style}",
                    fontSize = 12.sp,
                    color = Color(0xFF94A3B8)
                )
                Text(
                    text = dateString,
                    fontSize = 11.sp,
                    color = Color(0xFF64748B)
                )
            }

            if (job.status == JobStatus.RUNNING) {
                LinearProgressIndicator(
                    progress = { job.progress / 100f },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(6.dp)
                        .clip(RoundedCornerShape(3.dp)),
                    color = CyanGlow,
                    trackColor = SurfaceElevated
                )
            }
        }
    }
}
"""

# 9. SettingsScreen.kt
FILES["app/src/main/java/com/example/ui/screens/SettingsScreen.kt"] = """package com.example.ui.screens

import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.DeleteSweep
import androidx.compose.material.icons.filled.Key
import androidx.compose.material.icons.filled.Speed
import androidx.compose.material.icons.filled.Visibility
import androidx.compose.material.icons.filled.VisibilityOff
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Switch
import androidx.compose.material3.SwitchDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.data.SecureStore
import com.example.data.SkillsStore
import com.example.network.OpenRouterClient
import com.example.ui.theme.CyanGlow
import com.example.ui.theme.EmeraldSuccess
import com.example.ui.theme.MagentaNeon
import com.example.ui.theme.MidnightDark
import com.example.ui.theme.RoseError
import com.example.ui.theme.SurfaceDark
import com.example.ui.theme.SurfaceElevated
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

@Composable
fun SettingsScreen(
    modifier: Modifier = Modifier
) {
    val context = LocalContext.current
    val secureStore = remember { SecureStore(context) }
    val skillsStore = remember { SkillsStore(context) }
    val scope = rememberCoroutineScope()

    var apiKeyInput by remember { mutableStateOf(secureStore.getApiKey()) }
    var showApiKey by remember { mutableStateOf(false) }
    var modelNameInput by remember { mutableStateOf(secureStore.modelName) }
    var stepDelayInput by remember { mutableStateOf(secureStore.stepDelayMs.toString()) }
    var maxStepsInput by remember { mutableStateOf(secureStore.maxSteps.toString()) }
    var maxRetriesInput by remember { mutableStateOf(secureStore.maxRetries.toString()) }

    var askBeforeExport by remember { mutableStateOf(secureStore.askBeforeExport) }
    var proactiveImprovements by remember { mutableStateOf(secureStore.proactiveImprovements) }
    var selectedCapcutPkg by remember { mutableStateOf(secureStore.capcutPackage) }
    val installedVariants = remember { secureStore.getInstalledCapCutVariants() }

    var isTestingKey by remember { mutableStateOf(false) }
    var testResultText by remember { mutableStateOf<String?>(null) }
    var isTestSuccess by remember { mutableStateOf(false) }
    var memoryCount by remember { mutableStateOf(skillsStore.getSkillCount()) }

    Column(
        modifier = modifier
            .fillMaxSize()
            .background(MidnightDark)
            .padding(16.dp)
            .verticalScroll(rememberScrollState()),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text(
            text = "ترتیبات اور ماڈل سیٹ اپ",
            fontSize = 20.sp,
            fontWeight = FontWeight.Bold,
            color = Color.White
        )

        Card(
            colors = CardDefaults.cardColors(containerColor = SurfaceDark),
            shape = RoundedCornerShape(20.dp),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(
                modifier = Modifier.padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(imageVector = Icons.Default.Key, contentDescription = null, tint = CyanGlow)
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("OpenRouter API Key", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 15.sp)
                }

                OutlinedTextField(
                    value = apiKeyInput,
                    onValueChange = {
                        apiKeyInput = it
                        secureStore.saveApiKey(it)
                    },
                    label = { Text("OpenRouter API Key") },
                    placeholder = { Text("sk-or-v1-...") },
                    visualTransformation = if (showApiKey) VisualTransformation.None else PasswordVisualTransformation(),
                    trailingIcon = {
                        IconButton(onClick = { showApiKey = !showApiKey }) {
                            Icon(
                                imageVector = if (showApiKey) Icons.Default.VisibilityOff else Icons.Default.Visibility,
                                contentDescription = if (showApiKey) "چھپائیں" else "دیکھیں",
                                tint = Color.Gray
                            )
                        }
                    },
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedTextColor = Color.White,
                        unfocusedTextColor = Color.White,
                        focusedBorderColor = CyanGlow,
                        unfocusedBorderColor = SurfaceElevated
                    ),
                    shape = RoundedCornerShape(14.dp),
                    modifier = Modifier
                        .fillMaxWidth()
                        .testTag("api_key_input")
                )

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    OutlinedButton(
                        onClick = {
                            scope.launch {
                                isTestingKey = true
                                testResultText = null
                                val client = OpenRouterClient("")
                                val (success, msg) = withContext(Dispatchers.IO) {
                                    client.testApiKey(secureStore.getApiKey())
                                }
                                isTestingKey = false
                                isTestSuccess = success
                                testResultText = msg
                            }
                        },
                        enabled = !isTestingKey && apiKeyInput.isNotBlank(),
                        shape = RoundedCornerShape(12.dp),
                        modifier = Modifier.testTag("test_api_key_btn")
                    ) {
                        if (isTestingKey) {
                            CircularProgressIndicator(modifier = Modifier.size(16.dp), color = CyanGlow, strokeWidth = 2.dp)
                            Spacer(modifier = Modifier.width(8.dp))
                        }
                        Text(if (isTestingKey) "ٹیسٹ ہو رہا ہے..." else "API کی ٹیسٹ کریں", color = CyanGlow)
                    }

                    if (testResultText != null) {
                        Text(
                            text = if (isTestSuccess) "کامیاب ✓" else "ناکام ✗",
                            color = if (isTestSuccess) EmeraldSuccess else RoseError,
                            fontWeight = FontWeight.Bold,
                            fontSize = 13.sp
                        )
                    }
                }

                if (testResultText != null) {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(10.dp))
                            .background(if (isTestSuccess) EmeraldSuccess.copy(alpha = 0.15f) else RoseError.copy(alpha = 0.15f))
                            .padding(10.dp)
                    ) {
                        Text(
                            text = testResultText ?: "",
                            color = if (isTestSuccess) EmeraldSuccess else RoseError,
                            fontSize = 12.sp
                        )
                    }
                }
            }
        }

        Card(
            colors = CardDefaults.cardColors(containerColor = SurfaceDark),
            shape = RoundedCornerShape(20.dp),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(
                modifier = Modifier.padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(14.dp)
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(imageVector = Icons.Default.Speed, contentDescription = null, tint = CyanGlow)
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("ماڈل اور ایگزیکیوشن کی ترتیبات", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 15.sp)
                }

                OutlinedTextField(
                    value = modelNameInput,
                    onValueChange = {
                        modelNameInput = it
                        secureStore.modelName = it
                    },
                    label = { Text("OpenRouter ماڈل کا نام") },
                    placeholder = { Text("google/gemma-3-27b-it:free") },
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedTextColor = Color.White,
                        unfocusedTextColor = Color.White,
                        focusedBorderColor = CyanGlow,
                        unfocusedBorderColor = SurfaceElevated
                    ),
                    shape = RoundedCornerShape(14.dp),
                    modifier = Modifier.fillMaxWidth()
                )

                Text("مفت ماڈل تجاویز (Free Models):", color = Color.Gray, fontSize = 12.sp)
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    listOf(
                        "google/gemma-3-27b-it:free",
                        "meta-llama/llama-3.3-70b-instruct:free"
                    ).forEach { preset ->
                        OutlinedButton(
                            onClick = {
                                modelNameInput = preset
                                secureStore.modelName = preset
                            },
                            shape = RoundedCornerShape(10.dp),
                            modifier = Modifier.weight(1f)
                        ) {
                            Text(
                                text = preset.split("/").getOrNull(1)?.removeSuffix(":free") ?: preset,
                                fontSize = 11.sp,
                                color = if (modelNameInput == preset) CyanGlow else Color.White
                            )
                        }
                    }
                }

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(10.dp)
                ) {
                    OutlinedTextField(
                        value = stepDelayInput,
                        onValueChange = {
                            stepDelayInput = it
                            it.toLongOrNull()?.let { v -> secureStore.stepDelayMs = v }
                        },
                        label = { Text("وقفہ (ms)") },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedTextColor = Color.White,
                            unfocusedTextColor = Color.White,
                            focusedBorderColor = CyanGlow,
                            unfocusedBorderColor = SurfaceElevated
                        ),
                        shape = RoundedCornerShape(14.dp),
                        modifier = Modifier.weight(1f)
                    )

                    OutlinedTextField(
                        value = maxStepsInput,
                        onValueChange = {
                            maxStepsInput = it
                            it.toIntOrNull()?.let { v -> secureStore.maxSteps = v }
                        },
                        label = { Text("مراحل (Max Steps)") },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedTextColor = Color.White,
                            unfocusedTextColor = Color.White,
                            focusedBorderColor = CyanGlow,
                            unfocusedBorderColor = SurfaceElevated
                        ),
                        shape = RoundedCornerShape(14.dp),
                        modifier = Modifier.weight(1f)
                    )
                }
            }
        }

        Card(
            colors = CardDefaults.cardColors(containerColor = SurfaceDark),
            shape = RoundedCornerShape(20.dp),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(
                modifier = Modifier.padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(14.dp)
            ) {
                Text("حفاظتی اور ایڈیٹنگ ٹوگلز", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 15.sp)

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text("ایکسپورٹ سے پہلے اجازت لیں", color = Color.White, fontSize = 14.sp, fontWeight = FontWeight.Medium)
                    }
                    Switch(
                        checked = askBeforeExport,
                        onCheckedChange = {
                            askBeforeExport = it
                            secureStore.askBeforeExport = it
                        },
                        colors = SwitchDefaults.colors(checkedThumbColor = CyanGlow)
                    )
                }

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text("خود سے بہتری تجویز کریں", color = Color.White, fontSize = 14.sp, fontWeight = FontWeight.Medium)
                    }
                    Switch(
                        checked = proactiveImprovements,
                        onCheckedChange = {
                            proactiveImprovements = it
                            secureStore.proactiveImprovements = it
                        },
                        colors = SwitchDefaults.colors(checkedThumbColor = MagentaNeon)
                    )
                }
            }
        }

        Card(
            colors = CardDefaults.cardColors(containerColor = SurfaceDark),
            shape = RoundedCornerShape(20.dp),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(
                modifier = Modifier.padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                Text("CapCut پیکیج منتخب کریں", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 15.sp)

                installedVariants.forEach { pkg ->
                    val isSelected = pkg == selectedCapcutPkg
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(12.dp))
                            .background(if (isSelected) SurfaceElevated else Color.Transparent)
                            .clickable {
                                selectedCapcutPkg = pkg
                                secureStore.capcutPackage = pkg
                            }
                            .padding(10.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = pkg,
                            color = if (isSelected) CyanGlow else Color.White,
                            fontSize = 13.sp,
                            modifier = Modifier.weight(1f)
                        )
                        if (isSelected) {
                            Icon(imageVector = Icons.Default.Check, contentDescription = null, tint = CyanGlow)
                        }
                    }
                }
            }
        }

        Card(
            colors = CardDefaults.cardColors(containerColor = SurfaceDark),
            shape = RoundedCornerShape(20.dp),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(
                modifier = Modifier.padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                Text("مقامی لرننگ میموری (Local Skills Memory)", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 15.sp)
                Text(
                    text = "MIRA نے اب تک CapCut میں $memoryCount بٹن محفوظ کیے ہیں۔",
                    color = Color(0xFF94A3B8),
                    fontSize = 12.sp
                )

                OutlinedButton(
                    onClick = {
                        skillsStore.resetMemory()
                        memoryCount = 0
                        Toast.makeText(context, "میموری صاف کر دی گئی ہے", Toast.LENGTH_SHORT).show()
                    },
                    shape = RoundedCornerShape(12.dp)
                ) {
                    Icon(imageVector = Icons.Default.DeleteSweep, contentDescription = null, tint = RoseError)
                    Spacer(modifier = Modifier.width(6.dp))
                    Text("سیکھی ہوئی میموری صاف کریں", color = RoseError)
                }
            }
        }

        Card(
            colors = CardDefaults.cardColors(containerColor = SurfaceDark),
            shape = RoundedCornerShape(20.dp),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(
                modifier = Modifier.padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Text(
                    text = "رازداری کا نوٹس (Privacy Note)",
                    color = CyanGlow,
                    fontWeight = FontWeight.Bold,
                    fontSize = 15.sp
                )
                Text(
                    text = "ویڈیو ایڈیٹنگ کے دوران اسکرین شاٹس اور UI معلومات صرف OpenRouter اور آپ کے منتخب کردہ AI ماڈل پرووائیڈر کو محفوظ طریقے سے بھیجی جاتی ہیں۔ آپ کی API کی آپ کے فون کے محفوظ Android Keystore میں محفوظ رہتی ہے اور کسی دیگر سرور پر شیئر نہیں کی جاتی۔",
                    color = Color(0xFFCBD5E1),
                    fontSize = 12.sp,
                    lineHeight = 18.sp
                )
            }
        }

        Spacer(modifier = Modifier.height(24.dp))
    }
}
"""

# 10. OnboardingScreen.kt
FILES["app/src/main/java/com/example/ui/screens/OnboardingScreen.kt"] = """package com.example.ui.screens

import android.Manifest
import android.content.Intent
import android.net.Uri
import android.os.Build
import android.provider.Settings
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Accessibility
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.Help
import androidx.compose.material.icons.filled.Key
import androidx.compose.material.icons.filled.Layers
import androidx.compose.material.icons.filled.Movie
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.filled.OpenInNew
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.R
import com.example.data.SecureStore
import com.example.service.MiraAccessibilityService
import com.example.service.OverlayService
import com.example.ui.theme.CyanGlow
import com.example.ui.theme.EmeraldSuccess
import com.example.ui.theme.MagentaNeon
import com.example.ui.theme.MidnightDark
import com.example.ui.theme.SurfaceDark
import com.example.ui.theme.SurfaceElevated

@Composable
fun OnboardingScreen(
    onFinish: () -> Unit,
    modifier: Modifier = Modifier
) {
    val context = LocalContext.current
    val secureStore = remember { SecureStore(context) }

    var apiKeyInput by remember { mutableStateOf(secureStore.getApiKey()) }
    var isApiKeyValid by remember { mutableStateOf(secureStore.getApiKey().isNotBlank()) }
    var isNotificationAllowed by remember { mutableStateOf(true) }
    var isOverlayAllowed by remember { mutableStateOf(false) }
    var isAccessibilityAllowed by remember { mutableStateOf(false) }
    var isCapCutOpened by remember { mutableStateOf(false) }

    var showRestrictedHelp by remember { mutableStateOf(false) }

    val notificationLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestPermission()
    ) { granted ->
        isNotificationAllowed = granted
    }

    fun refreshPermissions() {
        isApiKeyValid = secureStore.getApiKey().isNotBlank()
        isOverlayAllowed = OverlayService.canDrawOverlays(context)
        isAccessibilityAllowed = MiraAccessibilityService.isServiceRunning()
    }

    LaunchedEffect(Unit) {
        refreshPermissions()
    }

    Column(
        modifier = modifier
            .fillMaxSize()
            .background(MidnightDark)
            .padding(16.dp)
            .verticalScroll(rememberScrollState()),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text(
            text = "MIRA AI ابتدائی سیٹ اپ",
            fontSize = 22.sp,
            fontWeight = FontWeight.Bold,
            color = Color.White
        )

        Text(
            text = "MIRA کو مکمل طور پر فعال کرنے کے لیے یہ 5 آسان مراحل مکمل کریں۔ مکمل ہونے پر سبز نشان ظاہر ہو جائے گا۔",
            color = Color(0xFFCBD5E1),
            fontSize = 13.sp,
            lineHeight = 19.sp
        )

        OnboardingStepCard(
            stepNumber = 1,
            title = "OpenRouter API کی شامل کریں",
            description = "openrouter.ai سے اپنی API کی حاصل کریں اور نیچے پیسٹ کریں۔",
            isCompleted = isApiKeyValid,
            icon = Icons.Default.Key
        ) {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                OutlinedTextField(
                    value = apiKeyInput,
                    onValueChange = {
                        apiKeyInput = it
                        secureStore.saveApiKey(it)
                        isApiKeyValid = it.isNotBlank()
                    },
                    label = { Text("API Key پیسٹ کریں") },
                    placeholder = { Text("sk-or-v1-...") },
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedTextColor = Color.White,
                        unfocusedTextColor = Color.White,
                        focusedBorderColor = CyanGlow,
                        unfocusedBorderColor = SurfaceElevated
                    ),
                    shape = RoundedCornerShape(12.dp),
                    modifier = Modifier.fillMaxWidth()
                )

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.End
                ) {
                    OutlinedButton(
                        onClick = {
                            val browserIntent = Intent(Intent.ACTION_VIEW, Uri.parse("https://openrouter.ai/keys"))
                            context.startActivity(browserIntent)
                        },
                        shape = RoundedCornerShape(10.dp)
                    ) {
                        Text("OpenRouter کی حاصل کریں", color = CyanGlow, fontSize = 12.sp)
                        Spacer(modifier = Modifier.width(6.dp))
                        Icon(imageVector = Icons.Default.OpenInNew, contentDescription = null, tint = CyanGlow, modifier = Modifier.size(16.dp))
                    }
                }
            }
        }

        OnboardingStepCard(
            stepNumber = 2,
            title = "اطلاعات (Notifications) کی اجازت",
            description = "پس پردہ ایڈیٹنگ کی حالت اور فوری الرٹس موصول کرنے کے لیے ضروری ہے۔",
            isCompleted = isNotificationAllowed,
            icon = Icons.Default.Notifications
        ) {
            Button(
                onClick = {
                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                        notificationLauncher.launch(Manifest.permission.POST_NOTIFICATIONS)
                    } else {
                        isNotificationAllowed = true
                    }
                },
                colors = ButtonDefaults.buttonColors(
                    containerColor = if (isNotificationAllowed) EmeraldSuccess else CyanGlow
                ),
                shape = RoundedCornerShape(10.dp)
            ) {
                Text(
                    text = if (isNotificationAllowed) "اجازت دی گئی ہے ✓" else "اطلاعات کی اجازت دیں",
                    color = if (isNotificationAllowed) Color.White else MidnightDark,
                    fontWeight = FontWeight.Bold
                )
            }
        }

        OnboardingStepCard(
            stepNumber = 3,
            title = "دیگر ایپس پر ظاہر ہونے کی اجازت (Overlay)",
            description = "CapCut کے اوپر فلوٹنگ ببل، ایمرجنسی اسٹاپ بٹن اور اسٹیٹس دکھانے کے لیے درکار ہے۔",
            isCompleted = isOverlayAllowed,
            icon = Icons.Default.Layers
        ) {
            Button(
                onClick = {
                    val intent = Intent(
                        Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                        Uri.parse("package:${context.packageName}")
                    ).apply {
                        flags = Intent.FLAG_ACTIVITY_NEW_TASK
                    }
                    context.startActivity(intent)
                },
                colors = ButtonDefaults.buttonColors(
                    containerColor = if (isOverlayAllowed) EmeraldSuccess else CyanGlow
                ),
                shape = RoundedCornerShape(10.dp)
            ) {
                Text(
                    text = if (isOverlayAllowed) "اجازت دی گئی ہے ✓" else "اوورلے کی اجازت دیں",
                    color = if (isOverlayAllowed) Color.White else MidnightDark,
                    fontWeight = FontWeight.Bold
                )
            }
        }

        OnboardingStepCard(
            stepNumber = 4,
            title = "رسائی سروس (Accessibility Service) آن کریں",
            description = "CapCut اسکرین دیکھنے اور آپ کی جگہ کٹس اور اسپلٹ لگانے کے لیے ضروری ہے۔",
            isCompleted = isAccessibilityAllowed,
            icon = Icons.Default.Accessibility
        ) {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Button(
                    onClick = {
                        val intent = Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS).apply {
                            flags = Intent.FLAG_ACTIVITY_NEW_TASK
                        }
                        context.startActivity(intent)
                    },
                    colors = ButtonDefaults.buttonColors(
                        containerColor = if (isAccessibilityAllowed) EmeraldSuccess else CyanGlow
                    ),
                    shape = RoundedCornerShape(10.dp)
                ) {
                    Text(
                        text = if (isAccessibilityAllowed) "سروس آن ہے ✓" else "Accessibility کھولیں",
                        color = if (isAccessibilityAllowed) Color.White else MidnightDark,
                        fontWeight = FontWeight.Bold
                    )
                }

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.Start
                ) {
                    OutlinedButton(
                        onClick = { showRestrictedHelp = !showRestrictedHelp },
                        shape = RoundedCornerShape(10.dp)
                    ) {
                        Icon(imageVector = Icons.Default.Help, contentDescription = null, tint = MagentaNeon, modifier = Modifier.size(16.dp))
                        Spacer(modifier = Modifier.width(6.dp))
                        Text("اگر سوئچ گرے / بلاک ہو؟ (Android 13+ رہنمائی)", color = MagentaNeon, fontSize = 12.sp)
                    }
                }

                AnimatedVisibility(visible = showRestrictedHelp) {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(10.dp))
                            .background(SurfaceElevated)
                            .padding(12.dp)
                    ) {
                        Text(
                            text = stringResource(R.string.onboarding_step4_help),
                            color = Color(0xFFFBCFE8),
                            fontSize = 12.sp,
                            lineHeight = 18.sp
                        )
                    }
                }
            }
        }

        OnboardingStepCard(
            stepNumber = 5,
            title = "CapCut کھولیں اور تصدیق کریں",
            description = "یقینی بنائیں کہ CapCut موبائل میں موجود ہے اور کم از کم ایک بار کھل چکا ہے۔",
            isCompleted = isCapCutOpened,
            icon = Icons.Default.Movie
        ) {
            Button(
                onClick = {
                    val pkg = secureStore.capcutPackage
                    val launchIntent = context.packageManager.getLaunchIntentForPackage(pkg)
                    if (launchIntent != null) {
                        context.startActivity(launchIntent)
                        isCapCutOpened = true
                    } else {
                        val playStoreIntent = Intent(Intent.ACTION_VIEW, Uri.parse("market://details?id=$pkg")).apply {
                            flags = Intent.FLAG_ACTIVITY_NEW_TASK
                        }
                        try {
                            context.startActivity(playStoreIntent)
                        } catch (_: Exception) {}
                    }
                },
                colors = ButtonDefaults.buttonColors(
                    containerColor = if (isCapCutOpened) EmeraldSuccess else CyanGlow
                ),
                shape = RoundedCornerShape(10.dp)
            ) {
                Text(
                    text = if (isCapCutOpened) "CapCut کھول دیا گیا ✓" else "CapCut کھولیں",
                    color = if (isCapCutOpened) Color.White else MidnightDark,
                    fontWeight = FontWeight.Bold
                )
            }
        }

        Spacer(modifier = Modifier.height(8.dp))

        Button(
            onClick = {
                secureStore.onboardingCompleted = true
                onFinish()
            },
            colors = ButtonDefaults.buttonColors(containerColor = CyanGlow),
            shape = RoundedCornerShape(16.dp),
            modifier = Modifier
                .fillMaxWidth()
                .height(54.dp)
                .testTag("complete_onboarding_btn")
        ) {
            Text(
                text = "مکمل کریں اور شروع کریں",
                fontSize = 16.sp,
                fontWeight = FontWeight.Bold,
                color = MidnightDark
            )
        }

        Spacer(modifier = Modifier.height(24.dp))
    }
}

@Composable
fun OnboardingStepCard(
    stepNumber: Int,
    title: String,
    description: String,
    isCompleted: Boolean,
    icon: ImageVector,
    content: @Composable () -> Unit
) {
    Card(
        colors = CardDefaults.cardColors(
            containerColor = if (isCompleted) SurfaceDark else SurfaceElevated
        ),
        shape = RoundedCornerShape(18.dp),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween,
                modifier = Modifier.fillMaxWidth()
            ) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier.weight(1f)
                ) {
                    Box(
                        modifier = Modifier
                            .size(32.dp)
                            .clip(RoundedCornerShape(8.dp))
                            .background(if (isCompleted) EmeraldSuccess.copy(alpha = 0.2f) else CyanGlow.copy(alpha = 0.2f)),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            imageVector = icon,
                            contentDescription = null,
                            tint = if (isCompleted) EmeraldSuccess else CyanGlow,
                            modifier = Modifier.size(18.dp)
                        )
                    }
                    Spacer(modifier = Modifier.width(10.dp))
                    Text(
                        text = title,
                        fontSize = 15.sp,
                        fontWeight = FontWeight.Bold,
                        color = Color.White
                    )
                }

                if (isCompleted) {
                    Icon(
                        imageVector = Icons.Default.CheckCircle,
                        contentDescription = "مکمل",
                        tint = EmeraldSuccess,
                        modifier = Modifier.size(22.dp)
                    )
                }
            }

            Text(
                text = description,
                fontSize = 12.sp,
                color = Color(0xFFCBD5E1),
                lineHeight = 17.sp
            )

            content()
        }
    }
}
"""

def main():
    root = Path(".")
    print(f"Applying OpenRouter patch from root: {root.resolve()}")
    
    deprecated = Path("app/src/main/java/com/example/network/GeminiClient.kt")
    if deprecated.exists():
        deprecated.unlink()
        print(f"[-] Removed deprecated: {deprecated}")
    
    changed_files = []
    for rel_path, content in FILES.items():
        file_path = root / rel_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        changed_files.append(rel_path)
        print(f"[+] Written: {rel_path}")

    print("\\nSuccessfully patched MIRA AI for OpenRouter!")
    print(f"Total files updated: {len(changed_files)}")
    for f in changed_files:
        print(f"  - {f}")

if __name__ == "__main__":
    main()