package com.example.data

import android.content.Context
import com.example.model.SkillRecord
import org.json.JSONArray
import org.json.JSONObject
import java.io.File

class SkillsStore(context: Context) {

    private val file = File(context.filesDir, "mira_skills_memory.json")

    @Synchronized
    fun saveSkill(record: SkillRecord) {
        val root = loadRoot()
        val versionObj = root.optJSONObject(record.capcutVersion) ?: JSONObject()
        val recordObj = JSONObject().apply {
            put("label", record.label)
            put("viewId", record.viewId ?: "")
            put("relativeX", record.relativeX.toDouble())
            put("relativeY", record.relativeY.toDouble())
        }
        versionObj.put(normalizeKey(record.label), recordObj)
        root.put(record.capcutVersion, versionObj)
        saveRoot(root)
    }

    @Synchronized
    fun findSkill(capcutVersion: String, label: String): SkillRecord? {
        val root = loadRoot()
        val versionObj = root.optJSONObject(capcutVersion) ?: return null
        val recordObj = versionObj.optJSONObject(normalizeKey(label)) ?: return null
        return SkillRecord(
            capcutVersion = capcutVersion,
            label = recordObj.optString("label", label),
            viewId = recordObj.optString("viewId").ifBlank { null },
            relativeX = recordObj.optDouble("relativeX", 0.5).toFloat(),
            relativeY = recordObj.optDouble("relativeY", 0.5).toFloat()
        )
    }

    @Synchronized
    fun getSkillCount(): Int {
        val root = loadRoot()
        var count = 0
        val keys = root.keys()
        while (keys.hasNext()) {
            val vKey = keys.next()
            val versionObj = root.optJSONObject(vKey)
            if (versionObj != null) {
                count += versionObj.length()
            }
        }
        return count
    }

    @Synchronized
    fun resetMemory() {
        if (file.exists()) {
            file.delete()
        }
    }

    private fun normalizeKey(label: String): String {
        return label.trim().lowercase().replace("\\s+".toRegex(), "_")
    }

    private fun loadRoot(): JSONObject {
        if (!file.exists()) return JSONObject()
        return try {
            val content = file.readText(Charsets.UTF_8)
            JSONObject(content)
        } catch (_: Exception) {
            JSONObject()
        }
    }

    private fun saveRoot(root: JSONObject) {
        try {
            file.writeText(root.toString(2), Charsets.UTF_8)
        } catch (_: Exception) {}
    }
}
