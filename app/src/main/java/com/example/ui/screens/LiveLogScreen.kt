package com.example.ui.screens

import android.content.Intent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Share
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.agent.AgentRunner
import com.example.model.StepLog
import com.example.ui.theme.CyanGlow
import com.example.ui.theme.EmeraldSuccess
import com.example.ui.theme.MidnightDark
import com.example.ui.theme.RoseError
import com.example.ui.theme.SurfaceDark
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

@Composable
fun LiveLogScreen(
    modifier: Modifier = Modifier
) {
    val context = LocalContext.current
    val logs by AgentRunner.logs.collectAsState()
    val currentJob by AgentRunner.currentJob.collectAsState()

    Column(
        modifier = modifier
            .fillMaxSize()
            .background(MidnightDark)
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column {
                Text(
                    text = "لائیو لاگ (Live Steps)",
                    fontSize = 20.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.White
                )
                Text(
                    text = "مجموعی مراحل: ${logs.size} | API کالز: ${currentJob?.apiCallsCount ?: 0}",
                    fontSize = 12.sp,
                    color = CyanGlow
                )
            }

            Row {
                IconButton(
                    onClick = {
                        val textLog = buildShareableLog(logs)
                        val sendIntent = Intent().apply {
                            action = Intent.ACTION_SEND
                            putExtra(Intent.EXTRA_TEXT, textLog)
                            type = "text/plain"
                        }
                        context.startActivity(Intent.createChooser(sendIntent, "MIRA لاگ شیئر کریں"))
                    },
                    enabled = logs.isNotEmpty()
                ) {
                    Icon(imageVector = Icons.Default.Share, contentDescription = "شیئر کریں", tint = CyanGlow)
                }

                IconButton(
                    onClick = { AgentRunner.clearLogs() },
                    enabled = logs.isNotEmpty()
                ) {
                    Icon(imageVector = Icons.Default.Delete, contentDescription = "صاف کریں", tint = RoseError)
                }
            }
        }

        if (logs.isEmpty()) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(32.dp),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = "جب MIRA ایڈیٹنگ کا ٹاسک شروع کرے گی تو ہر ایک قدم کی تفصیلات یہاں دکھائی دیں گی۔",
                    color = Color(0xFF64748B),
                    fontSize = 14.sp
                )
            }
        } else {
            LazyColumn(
                modifier = Modifier
                    .fillMaxSize()
                    .testTag("logs_list"),
                verticalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                items(logs.reversed()) { log ->
                    LogItemCard(log = log)
                }
            }
        }
    }
}

@Composable
fun LogItemCard(log: StepLog) {
    val sdf = remember { SimpleDateFormat("hh:mm:ss", Locale.getDefault()) }
    val timeStr = remember(log.timestamp) { sdf.format(Date(log.timestamp)) }

    Card(
        colors = CardDefaults.cardColors(containerColor = SurfaceDark),
        shape = RoundedCornerShape(16.dp),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier.padding(14.dp),
            verticalArrangement = Arrangement.spacedBy(6.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Box(
                        modifier = Modifier
                            .size(10.dp)
                            .clip(CircleShape)
                            .background(if (log.isSuccess) EmeraldSuccess else RoseError)
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = "مرحلہ نمبر ${log.stepNumber}",
                        fontWeight = FontWeight.Bold,
                        color = Color.White,
                        fontSize = 14.sp
                    )
                }

                Text(
                    text = timeStr,
                    color = Color(0xFF64748B),
                    fontSize = 11.sp
                )
            }

            Text(
                text = log.thoughtUrdu,
                color = CyanGlow,
                fontSize = 13.sp,
                fontWeight = FontWeight.Medium,
                lineHeight = 18.sp
            )

            Text(
                text = "اسکرین: ${log.screenSummary}",
                color = Color(0xFFCBD5E1),
                fontSize = 11.sp
            )

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(
                    text = "عمل: ${log.actionName}",
                    color = Color(0xFF94A3B8),
                    fontSize = 11.sp
                )
                Text(
                    text = log.resultUrdu,
                    color = if (log.isSuccess) EmeraldSuccess else RoseError,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold
                )
            }
        }
    }
}

private fun buildShareableLog(logs: List<StepLog>): String {
    val sb = StringBuilder()
    sb.appendLine("=== MIRA AI Execution Log ===")
    val sdf = SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault())
    for (log in logs) {
        sb.appendLine("[Step ${log.stepNumber}] ${sdf.format(Date(log.timestamp))}")
        sb.appendLine("Urdu Thought: ${log.thoughtUrdu}")
        sb.appendLine("Screen: ${log.screenSummary}")
        sb.appendLine("Action: ${log.actionName}")
        sb.appendLine("Result: ${log.resultUrdu} (Success=${log.isSuccess})")
        sb.appendLine("---------------------------------------")
    }
    return sb.toString()
}
