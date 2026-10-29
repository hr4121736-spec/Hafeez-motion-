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

class GeminiClient(
    private val defaultSystemPrompt: String
) {
    private val client = OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(60, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        .build()

    private val jsonMediaType = "application/json; charset=utf-8".toMediaType()

    suspend fun decideNextAction(
        apiKey: String,
        modelName: String,
        job: EditJob,
        currentObservation: ObservationResult,
        history: List<StepLog>,
        sendScreenshot: Boolean,
        onWaitingRateLimit: (String) -> Unit
    ): Pair<ActionResponse, Int> {
        var apiCallsMade = 0
        var attempt = 0
        val maxRetries = 3
        var backoffMs = 2000L

        while (attempt < maxRetries) {
            attempt++
            apiCallsMade++

            val requestBody = buildGeminiRequestBody(
                job = job,
                observation = currentObservation,
                history = history,
                sendScreenshot = sendScreenshot
            )

            val url = "https://generativelanguage.googleapis.com/v1beta/models/$modelName:generateContent"
            val request = Request.Builder()
                .url(url)
                .addHeader("x-goog-api-key", apiKey)
                .post(requestBody.toRequestBody(jsonMediaType))
                .build()

            try {
                client.newCall(request).execute().use { response ->
                    val code = response.code
                    val bodyString = response.body?.string() ?: ""

                    if (code == 429 || code in 500..599) {
                        onWaitingRateLimit("MIRA انتظار کر رہی ہے... (سرور بزی ہے، دوبارہ کوشش)")
                        delay(backoffMs)
                        backoffMs = (backoffMs * 2).coerceAtMost(16000L)
                        return@use
                    }

                    if (!response.isSuccessful) {
                        if (attempt >= maxRetries) {
                            return Pair(
                                ActionResponse(
                                    thoughtUrdu = "جیمنائی سرور نے خرابی دی: کوڈ $code",
                                    screenSummary = "API call failed with HTTP $code",
                                    action = ActionType.FAIL
                                ),
                                apiCallsMade
                            )
                        }
                        delay(1000L)
                        return@use
                    }

                    val parsedAction = parseGeminiResponse(bodyString)
                    if (parsedAction != null) {
                        return Pair(parsedAction, apiCallsMade)
                    } else if (attempt < maxRetries) {
                        delay(1000L)
                    }
                }
            } catch (e: IOException) {
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
                screenSummary = "Failed to parse action from Gemini after retries",
                action = ActionType.ASK_USER
            ),
            apiCallsMade
        )
    }

    suspend fun testApiKey(apiKey: String, modelName: String): Pair<Boolean, String> {
        if (apiKey.isBlank()) {
            return Pair(false, "API Key خالی ہے")
        }
        val url = "https://generativelanguage.googleapis.com/v1beta/models/$modelName:generateContent"
        val requestJson = JSONObject().apply {
            val contents = JSONArray().apply {
                val content = JSONObject().apply {
                    val parts = JSONArray().apply {
                        put(JSONObject().apply { put("text", "Respond with the word OK.") })
                    }
                    put("parts", parts)
                }
                put(content)
            }
            put("contents", contents)
        }

        val request = Request.Builder()
            .url(url)
            .addHeader("x-goog-api-key", apiKey)
            .post(requestJson.toString().toRequestBody(jsonMediaType))
            .build()

        return try {
            client.newCall(request).execute().use { response ->
                if (response.isSuccessful) {
                    Pair(true, "API Key درست ہے")
                } else {
                    val errorBody = response.body?.string() ?: ""
                    Pair(false, "خرابی: HTTP ${response.code} - ${errorBody.take(120)}")
                }
            }
        } catch (e: Exception) {
            Pair(false, "رابطہ ناکام: ${e.message}")
        }
    }

    private fun buildGeminiRequestBody(
        job: EditJob,
        observation: ObservationResult,
        history: List<StepLog>,
        sendScreenshot: Boolean
    ): String {
        val root = JSONObject()

        val systemInstruction = JSONObject().apply {
            val parts = JSONArray().apply {
                put(JSONObject().apply { put("text", defaultSystemPrompt) })
            }
            put("parts", parts)
        }
        root.put("system_instruction", systemInstruction)

        val contentsArray = JSONArray()
        val userContent = JSONObject()
        val partsArray = JSONArray()

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

        partsArray.put(JSONObject().apply {
            put("text", promptBuilder.toString())
        })

        if (sendScreenshot && !observation.screenshotBase64.isNullOrBlank()) {
            val inlineData = JSONObject().apply {
                put("mime_type", "image/jpeg")
                put("data", observation.screenshotBase64)
            }
            partsArray.put(JSONObject().apply {
                put("inline_data", inlineData)
            })
        }

        userContent.put("role", "user")
        userContent.put("parts", partsArray)
        contentsArray.put(userContent)
        root.put("contents", contentsArray)

        val genConfig = JSONObject().apply {
            put("response_mime_type", "application/json")
            put("temperature", 0.2)
        }
        root.put("generation_config", genConfig)

        return root.toString()
    }

    private fun parseGeminiResponse(rawBody: String): ActionResponse? {
        return try {
            val root = JSONObject(rawBody)
            val candidates = root.optJSONArray("candidates") ?: return null
            if (candidates.length() == 0) return null
            val content = candidates.getJSONObject(0).optJSONObject("content") ?: return null
            val parts = content.optJSONArray("parts") ?: return null
            if (parts.length() == 0) return null
            var text = parts.getJSONObject(0).optString("text") ?: return null

            text = text.trim()
            if (text.startsWith("```json")) text = text.removePrefix("```json").trim()
            if (text.startsWith("```")) text = text.removePrefix("```").trim()
            if (text.endsWith("```")) text = text.removeSuffix("```").trim()

            val obj = JSONObject(text)
            val thoughtUrdu = obj.optString("thought_urdu", "MIRA اگلا قدم اٹھا رہی ہے...")
            val screenSummary = obj.optString("screen_summary", "CapCut screen active")
            val actionStr = obj.optString("action", "wait")
            val actionType = ActionType.fromString(actionStr)

            val x = if (obj.has("x") && !obj.isNull("x")) obj.optDouble("x").toFloat() else null
            val y = if (obj.has("y") && !obj.isNull("y")) obj.optDouble("y").toFloat() else null
            val x2 = if (obj.has("x2") && !obj.isNull("x2")) obj.optDouble("x2").toFloat() else null
            val y2 = if (obj.has("y2") && !obj.isNull("y2")) obj.optDouble("y2").toFloat() else null
            val durationMs = if (obj.has("duration_ms") && !obj.isNull("duration_ms")) obj.optLong("duration_ms") else null
            val txt = if (obj.has("text") && !obj.isNull("text")) obj.optString("text") else null
            val targetNodeIdx = if (obj.has("target_node_index") && !obj.isNull("target_node_index")) obj.optInt("target_node_index") else null
            val expected = obj.optString("expected_result", "")
            val progress = obj.optInt("progress_percent", 0).coerceIn(0, 100)

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
}
