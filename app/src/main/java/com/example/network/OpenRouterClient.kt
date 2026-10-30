package com.example.network

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
            val nextLine = clean.indexOf('\n', startIndex)
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
