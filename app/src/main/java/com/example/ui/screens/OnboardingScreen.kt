package com.example.ui.screens

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
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
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
            title = "Gemini API کی شامل کریں",
            description = "Google AI Studio سے اپنی مفت جیمنائی کی حاصل کریں اور نیچے پیسٹ کریں۔",
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
                    placeholder = { Text("AIzaSy...") },
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
                            val browserIntent = Intent(Intent.ACTION_VIEW, Uri.parse("https://aistudio.google.com/app/apikey"))
                            context.startActivity(browserIntent)
                        },
                        shape = RoundedCornerShape(10.dp)
                    ) {
                        Text("مفت کی حاصل کریں (AI Studio)", color = CyanGlow, fontSize = 12.sp)
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
                    }
                },
                colors = ButtonDefaults.buttonColors(containerColor = CyanGlow),
                shape = RoundedCornerShape(12.dp)
            ) {
                Text("اجازت دیں", color = MidnightDark, fontWeight = FontWeight.Bold)
            }
        }

        OnboardingStepCard(
            stepNumber = 3,
            title = "دیگر ایپس پر ظاہر ہونے کی اجازت (Overlay)",
            description = "CapCut کے اوپر تیرتا ہوا کنٹرول ببل، روکیں بٹن اور پروگریس دیکھنے کے لیے ضروری ہے۔",
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
                colors = ButtonDefaults.buttonColors(containerColor = CyanGlow),
                shape = RoundedCornerShape(12.dp)
            ) {
                Text("اجازت آن کریں", color = MidnightDark, fontWeight = FontWeight.Bold)
            }
        }

        OnboardingStepCard(
            stepNumber = 4,
            title = "رسائی سروس (Accessibility Service)",
            description = "یہ MIRA کے ہاتھ اور آنکھیں ہیں جو CapCut کی اسکرین پڑھ کر بٹن دباتی ہیں۔",
            isCompleted = isAccessibilityAllowed,
            icon = Icons.Default.Accessibility
        ) {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(
                        onClick = {
                            val intent = Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS).apply {
                                flags = Intent.FLAG_ACTIVITY_NEW_TASK
                            }
                            context.startActivity(intent)
                        },
                        colors = ButtonDefaults.buttonColors(containerColor = MagentaNeon),
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Text("سروس آن کریں", color = Color.White, fontWeight = FontWeight.Bold)
                    }

                    OutlinedButton(
                        onClick = { showRestrictedHelp = !showRestrictedHelp },
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Icon(imageVector = Icons.Default.Help, contentDescription = null, tint = CyanGlow)
                        Spacer(modifier = Modifier.width(6.dp))
                        Text("سوئچ گرے ہے؟", color = CyanGlow, fontSize = 12.sp)
                    }
                }

                AnimatedVisibility(visible = showRestrictedHelp) {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(12.dp))
                            .background(SurfaceElevated)
                            .padding(12.dp)
                    ) {
                        Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                            Text(
                                text = "اینڈرائیڈ 13 اور جدید فونز کے لیے رہنمائی:",
                                color = CyanGlow,
                                fontWeight = FontWeight.Bold,
                                fontSize = 13.sp
                            )
                            Text(
                                text = "1. فون کی Settings > Apps > MIRA AI کھولیں۔\n" +
                                        "2. اوپر دائیں کونے میں تین نقطوں پر ٹیپ کریں۔\n" +
                                        "3. 'Allow restricted settings' کو منتخب کریں اور تصدیق کریں۔\n" +
                                        "4. اب واپس آ کر رسائی سروس آن کریں، سوئچ انلاک ہو جائے گا!",
                                color = Color.White,
                                fontSize = 12.sp,
                                lineHeight = 18.sp
                            )
                        }
                    }
                }
            }
        }

        OnboardingStepCard(
            stepNumber = 5,
            title = "CapCut کھولیں اور واپس آئیں",
            description = "یقینی بنائیں کہ CapCut ایپ انسٹال اور ایک بار کھلی ہے۔",
            isCompleted = isCapCutOpened,
            icon = Icons.Default.Movie
        ) {
            Button(
                onClick = {
                    val pkg = secureStore.capcutPackage
                    val launchIntent = context.packageManager.getLaunchIntentForPackage(pkg)
                    if (launchIntent != null) {
                        launchIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                        context.startActivity(launchIntent)
                        isCapCutOpened = true
                    }
                },
                colors = ButtonDefaults.buttonColors(containerColor = CyanGlow),
                shape = RoundedCornerShape(12.dp)
            ) {
                Text("CapCut کھولیں", color = MidnightDark, fontWeight = FontWeight.Bold)
            }
        }

        Spacer(modifier = Modifier.height(16.dp))

        Button(
            onClick = {
                secureStore.onboardingCompleted = true
                onFinish()
            },
            colors = ButtonDefaults.buttonColors(containerColor = EmeraldSuccess),
            shape = RoundedCornerShape(16.dp),
            modifier = Modifier
                .fillMaxWidth()
                .height(54.dp)
                .testTag("finish_onboarding_btn")
        ) {
            Text(
                text = "سیٹ اپ مکمل ہوا (مرکزی صفحہ پر جائیں)",
                color = Color.White,
                fontSize = 16.sp,
                fontWeight = FontWeight.Bold
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
        colors = CardDefaults.cardColors(containerColor = SurfaceDark),
        shape = RoundedCornerShape(20.dp),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier.padding(18.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(imageVector = icon, contentDescription = null, tint = CyanGlow, modifier = Modifier.size(22.dp))
                    Spacer(modifier = Modifier.width(10.dp))
                    Text(
                        text = "$stepNumber. $title",
                        color = Color.White,
                        fontSize = 15.sp,
                        fontWeight = FontWeight.Bold
                    )
                }

                if (isCompleted) {
                    Icon(
                        imageVector = Icons.Default.CheckCircle,
                        contentDescription = "مکمل",
                        tint = EmeraldSuccess,
                        modifier = Modifier.size(24.dp)
                    )
                }
            }

            Text(
                text = description,
                color = Color(0xFFCBD5E1),
                fontSize = 12.sp,
                lineHeight = 17.sp
            )

            content()
        }
    }
}
