package com.example.data

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
