package com.example.ui.screens

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
                            "تمام بنیادی شرائط اور جیمنائی کنکشن فعال ہیں۔ آپ براہ راست خودکار ایڈیٹنگ شروع کر سکتے ہیں۔"
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
                        title = "Gemini API Key",
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
            Text(
                text = "حالیہ ایڈیٹنگ ٹاسکس (Last 5 Jobs)",
                fontSize = 18.sp,
                fontWeight = FontWeight.Bold,
                color = Color.White,
                modifier = Modifier.padding(top = 8.dp)
            )
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
                            .padding(28.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = "ابھی تک کوئی ٹاسک نہیں چلایا گیا",
                            color = Color(0xFF94A3B8),
                            fontSize = 14.sp
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
            Spacer(modifier = Modifier.height(24.dp))
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
            .padding(horizontal = 14.dp, vertical = 10.dp),
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
                modifier = Modifier.size(20.dp)
            )
            Spacer(modifier = Modifier.width(10.dp))
            Text(
                text = title,
                color = Color.White,
                fontSize = 13.sp
            )
        }

        if (isOk) {
            Icon(
                imageVector = Icons.Default.CheckCircle,
                contentDescription = "فعال",
                tint = EmeraldSuccess,
                modifier = Modifier.size(20.dp)
            )
        } else {
            Button(
                onClick = onFix,
                colors = ButtonDefaults.buttonColors(containerColor = MagentaNeon),
                shape = RoundedCornerShape(10.dp),
                modifier = Modifier.height(34.dp)
            ) {
                Text("سیٹ کریں", color = Color.White, fontSize = 11.sp, fontWeight = FontWeight.Bold)
            }
        }
    }
}

@Composable
fun JobCard(job: EditJob) {
    val sdf = remember { SimpleDateFormat("dd MMM, hh:mm a", Locale.getDefault()) }
    val dateStr = remember(job.createdAt) { sdf.format(Date(job.createdAt)) }

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
                    text = job.videoNote.ifBlank { "خودکار ویڈیو ایڈیٹ" },
                    color = Color.White,
                    fontWeight = FontWeight.Bold,
                    fontSize = 15.sp,
                    maxLines = 1
                )

                JobStatusBadge(status = job.status)
            }

            Text(
                text = "اسٹائل: ${job.style} | کٹ سیکنڈز: ${job.cutTimings.ifBlank { "خودکار" }}",
                color = Color(0xFF94A3B8),
                fontSize = 12.sp
            )

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(
                    text = dateStr,
                    color = Color(0xFF64748B),
                    fontSize = 11.sp
                )
                Text(
                    text = "API کالز: ${job.apiCallsCount}",
                    color = CyanGlow,
                    fontSize = 11.sp
                )
            }

            if (job.progress in 1..99) {
                LinearProgressIndicator(
                    progress = { job.progress / 100f },
                    color = CyanGlow,
                    trackColor = SurfaceElevated,
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(4.dp)
                        .clip(RoundedCornerShape(2.dp))
                )
            }
        }
    }
}

@Composable
fun JobStatusBadge(status: JobStatus) {
    val (label, bg, fg) = when (status) {
        JobStatus.COMPLETED -> Triple("مکمل (Done)", EmeraldSuccess.copy(alpha = 0.2f), EmeraldSuccess)
        JobStatus.FAILED -> Triple("ناکام (Failed)", RoseError.copy(alpha = 0.2f), RoseError)
        JobStatus.STOPPED -> Triple("روکا گیا (Stopped)", Color(0xFFF59E0B).copy(alpha = 0.2f), Color(0xFFF59E0B))
        JobStatus.RUNNING -> Triple("جاری ہے...", CyanGlow.copy(alpha = 0.2f), CyanGlow)
        JobStatus.WAITING_PERMISSION -> Triple("اجازت کا انتظار", Color(0xFFF59E0B).copy(alpha = 0.2f), Color(0xFFF59E0B))
        JobStatus.WAITING_USER -> Triple("مدد کا انتظار", MagentaNeon.copy(alpha = 0.2f), MagentaNeon)
        else -> Triple("تیار", Color(0xFF334155), Color.White)
    }

    Box(
        modifier = Modifier
            .clip(RoundedCornerShape(8.dp))
            .background(bg)
            .padding(horizontal = 8.dp, vertical = 4.dp)
    ) {
        Text(
            text = label,
            color = fg,
            fontSize = 11.sp,
            fontWeight = FontWeight.SemiBold
        )
    }
}
