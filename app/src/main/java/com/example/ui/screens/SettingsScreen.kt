package com.example.ui.screens

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
import com.example.network.GeminiClient
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
                    Text("Google AI Studio Gemini API Key", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 15.sp)
                }

                OutlinedTextField(
                    value = apiKeyInput,
                    onValueChange = {
                        apiKeyInput = it
                        secureStore.saveApiKey(it)
                    },
                    label = { Text("Gemini API Key") },
                    placeholder = { Text("AIzaSy...") },
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
                                val client = GeminiClient("")
                                val (success, msg) = withContext(Dispatchers.IO) {
                                    client.testApiKey(secureStore.getApiKey(), modelNameInput)
                                }
                                isTestingKey = false
                                isTestSuccess = success
                                testResultText = if (success) "ماشاءاللہ! API کی درست ہے اور رابطہ ہو گیا ہے۔" else msg
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
                    label = { Text("Gemini ماڈل کا نام") },
                    placeholder = { Text("gemini-2.5-flash") },
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedTextColor = Color.White,
                        unfocusedTextColor = Color.White,
                        focusedBorderColor = CyanGlow,
                        unfocusedBorderColor = SurfaceElevated
                    ),
                    shape = RoundedCornerShape(14.dp),
                    modifier = Modifier.fillMaxWidth()
                )

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

        Spacer(modifier = Modifier.height(24.dp))
    }
}
