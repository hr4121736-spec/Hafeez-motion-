package com.example.ui.screens

import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.PickVisualMediaRequest
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.slideInHorizontally
import androidx.compose.animation.slideOutHorizontally
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.background
import androidx.compose.foundation.border
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
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.ArrowForward
import androidx.compose.material.icons.filled.Movie
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.VideoLibrary
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.RadioButton
import androidx.compose.material3.RadioButtonDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
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
import com.example.model.EditJob
import com.example.ui.theme.CyanGlow
import com.example.ui.theme.MagentaNeon
import com.example.ui.theme.MidnightDark
import com.example.ui.theme.SurfaceDark
import com.example.ui.theme.SurfaceElevated

fun normalizeDigits(input: String): String {
    val urduDigits = charArrayOf('۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹')
    var result = input
    for (i in urduDigits.indices) {
        result = result.replace(urduDigits[i], ('0' + i))
    }
    return result
}

@Composable
fun NewEditScreen(
    onJobStarted: () -> Unit,
    onNavigateBack: () -> Unit,
    modifier: Modifier = Modifier
) {
    val context = LocalContext.current
    var currentStep by remember { mutableIntStateOf(1) }

    var selectedVideoUri by remember { mutableStateOf<Uri?>(null) }
    var videoNote by remember { mutableStateOf("") }
    var cutTimingsRaw by remember { mutableStateOf("") }
    var selectedStyle by remember { mutableStateOf("MIRA خود فیصلہ کرے") }
    var specialInstructions by remember { mutableStateOf("") }

    val videoPickerLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.PickVisualMedia()
    ) { uri: Uri? ->
        if (uri != null) {
            selectedVideoUri = uri
        }
    }

    val stylesList = listOf(
        "MIRA خود فیصلہ کرے",
        "ریمپیج (Rampage)",
        "وائلوسیٹی (Velocity)",
        "اسموتھ سلو مو (Smooth Slow-Mo)",
        "سنیماٹک (Cinematic)"
    )

    Column(
        modifier = modifier
            .fillMaxSize()
            .background(MidnightDark)
            .padding(16.dp)
            .verticalScroll(rememberScrollState()),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            for (step in 1..5) {
                val isDone = step < currentStep
                val isCurrent = step == currentStep
                Box(
                    modifier = Modifier
                        .weight(1f)
                        .height(6.dp)
                        .padding(horizontal = 2.dp)
                        .clip(RoundedCornerShape(3.dp))
                        .background(
                            when {
                                isDone -> CyanGlow
                                isCurrent -> MagentaNeon
                                else -> SurfaceElevated
                            }
                        )
                )
            }
        }

        Text(
            text = "مرحلہ $currentStep از 5",
            color = CyanGlow,
            fontSize = 13.sp,
            fontWeight = FontWeight.Bold
        )

        AnimatedContent(
            targetState = currentStep,
            transitionSpec = {
                if (targetState > initialState) {
                    slideInHorizontally { width -> -width } togetherWith slideOutHorizontally { width -> width }
                } else {
                    slideInHorizontally { width -> width } togetherWith slideOutHorizontally { width -> -width }
                }
            },
            label = "step_animation"
        ) { step ->
            when (step) {
                1 -> Step1VideoPick(
                    selectedUri = selectedVideoUri,
                    videoNote = videoNote,
                    onPickClick = {
                        videoPickerLauncher.launch(
                            PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.VideoOnly)
                        )
                    },
                    onNoteChange = { videoNote = it }
                )
                2 -> Step2Cuts(
                    cutTimings = cutTimingsRaw,
                    onCutTimingsChange = { cutTimingsRaw = it }
                )
                3 -> Step3Style(
                    styles = stylesList,
                    selectedStyle = selectedStyle,
                    onSelect = { selectedStyle = it }
                )
                4 -> Step4Instructions(
                    instructions = specialInstructions,
                    onChange = { specialInstructions = it }
                )
                5 -> Step5Summary(
                    videoUri = selectedVideoUri,
                    videoNote = videoNote,
                    cutTimings = normalizeDigits(cutTimingsRaw),
                    style = selectedStyle,
                    instructions = specialInstructions,
                    onConfirmStart = {
                        val newJob = EditJob(
                            videoUri = selectedVideoUri?.toString(),
                            videoNote = videoNote.ifBlank { "خودکار ویڈیو ایڈیٹ" },
                            cutTimings = normalizeDigits(cutTimingsRaw),
                            style = selectedStyle,
                            instructions = specialInstructions
                        )
                        AgentRunner.startJob(context, newJob)
                        onJobStarted()
                    }
                )
            }
        }

        Spacer(modifier = Modifier.weight(1f))

        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(vertical = 12.dp),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            if (currentStep > 1) {
                OutlinedButton(
                    onClick = { currentStep-- },
                    shape = RoundedCornerShape(16.dp),
                    modifier = Modifier
                        .height(50.dp)
                        .testTag("btn_prev_step")
                ) {
                    Icon(imageVector = Icons.Default.ArrowForward, contentDescription = null, tint = Color.White)
                    Spacer(modifier = Modifier.width(6.dp))
                    Text("پچھلا مرحلہ", color = Color.White)
                }
            } else {
                OutlinedButton(
                    onClick = onNavigateBack,
                    shape = RoundedCornerShape(16.dp),
                    modifier = Modifier.height(50.dp)
                ) {
                    Text("منسوخ کریں", color = Color(0xFF94A3B8))
                }
            }

            if (currentStep < 5) {
                Button(
                    onClick = { currentStep++ },
                    colors = ButtonDefaults.buttonColors(containerColor = CyanGlow),
                    shape = RoundedCornerShape(16.dp),
                    modifier = Modifier
                        .height(50.dp)
                        .testTag("btn_next_step")
                ) {
                    Text("اگلا مرحلہ", color = MidnightDark, fontWeight = FontWeight.Bold)
                    Spacer(modifier = Modifier.width(6.dp))
                    Icon(imageVector = Icons.Default.ArrowBack, contentDescription = null, tint = MidnightDark)
                }
            }
        }
    }
}

@Composable
fun Step1VideoPick(
    selectedUri: Uri?,
    videoNote: String,
    onPickClick: () -> Unit,
    onNoteChange: (String) -> Unit
) {
    Card(
        colors = CardDefaults.cardColors(containerColor = SurfaceDark),
        shape = RoundedCornerShape(20.dp),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier.padding(20.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Text(
                text = "1. آج کون سی ویڈیو بنانی ہے؟",
                fontSize = 18.sp,
                fontWeight = FontWeight.Bold,
                color = Color.White
            )

            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(130.dp)
                    .clip(RoundedCornerShape(16.dp))
                    .background(SurfaceElevated)
                    .clickable { onPickClick() }
                    .border(1.dp, if (selectedUri != null) CyanGlow else Color.Transparent, RoundedCornerShape(16.dp))
                    .testTag("pick_video_box"),
                contentAlignment = Alignment.Center
            ) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Icon(
                        imageVector = if (selectedUri != null) Icons.Default.Movie else Icons.Default.VideoLibrary,
                        contentDescription = null,
                        tint = if (selectedUri != null) CyanGlow else MagentaNeon,
                        modifier = Modifier.size(36.dp)
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        text = if (selectedUri != null) "ویڈیو منتخب ہو چکی ہے ✓" else "گیلری سے ویڈیو منتخب کریں (Photo Picker)",
                        color = Color.White,
                        fontSize = 14.sp,
                        fontWeight = FontWeight.Medium
                    )
                }
            }

            OutlinedTextField(
                value = videoNote,
                onValueChange = onNoteChange,
                label = { Text("ویڈیو کا خیال یا عنوان") },
                placeholder = { Text("مثلاً: بائیک ڈرائیو، ٹریول بلاگ یا ایونٹ ہائی لائٹ...") },
                colors = OutlinedTextFieldDefaults.colors(
                    focusedTextColor = Color.White,
                    unfocusedTextColor = Color.White,
                    focusedBorderColor = CyanGlow,
                    unfocusedBorderColor = SurfaceElevated
                ),
                shape = RoundedCornerShape(16.dp),
                modifier = Modifier
                    .fillMaxWidth()
                    .testTag("video_note_input")
            )
        }
    }
}

@Composable
fun Step2Cuts(
    cutTimings: String,
    onCutTimingsChange: (String) -> Unit
) {
    Card(
        colors = CardDefaults.cardColors(containerColor = SurfaceDark),
        shape = RoundedCornerShape(20.dp),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier.padding(20.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Text(
                text = "2. کٹ کس سیکنڈ پر لگانے ہیں؟",
                fontSize = 18.sp,
                fontWeight = FontWeight.Bold,
                color = Color.White
            )

            Text(
                text = "ویڈیو میں مخصوص سیکنڈز پر کٹس لگانے کے لیے ٹائمنگز لکھیں۔ اردو یا انگلش ہندسے قبول کیے جائیں گے۔ (اختیاری)",
                color = Color(0xFFCBD5E1),
                fontSize = 13.sp
            )

            OutlinedTextField(
                value = cutTimings,
                onValueChange = onCutTimingsChange,
                label = { Text("کٹ ٹائمنگز (سیکنڈز)") },
                placeholder = { Text("مثلاً: 2.5, 5, 7.8 یا ۲.۵، ۵، ۷.۸") },
                colors = OutlinedTextFieldDefaults.colors(
                    focusedTextColor = Color.White,
                    unfocusedTextColor = Color.White,
                    focusedBorderColor = CyanGlow,
                    unfocusedBorderColor = SurfaceElevated
                ),
                shape = RoundedCornerShape(16.dp),
                modifier = Modifier
                    .fillMaxWidth()
                    .testTag("cut_timings_input")
            )
        }
    }
}

@Composable
fun Step3Style(
    styles: List<String>,
    selectedStyle: String,
    onSelect: (String) -> Unit
) {
    Card(
        colors = CardDefaults.cardColors(containerColor = SurfaceDark),
        shape = RoundedCornerShape(20.dp),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier.padding(20.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Text(
                text = "3. کون سا اسٹائل؟",
                fontSize = 18.sp,
                fontWeight = FontWeight.Bold,
                color = Color.White
            )

            styles.forEach { style ->
                val isSelected = style == selectedStyle
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(14.dp))
                        .background(if (isSelected) SurfaceElevated else Color.Transparent)
                        .clickable { onSelect(style) }
                        .padding(horizontal = 12.dp, vertical = 10.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    RadioButton(
                        selected = isSelected,
                        onClick = { onSelect(style) },
                        colors = RadioButtonDefaults.colors(selectedColor = CyanGlow)
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = style,
                        color = Color.White,
                        fontSize = 15.sp,
                        fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal
                    )
                }
            }
        }
    }
}

@Composable
fun Step4Instructions(
    instructions: String,
    onChange: (String) -> Unit
) {
    Card(
        colors = CardDefaults.cardColors(containerColor = SurfaceDark),
        shape = RoundedCornerShape(20.dp),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier.padding(20.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Text(
                text = "4. کوئی خاص ہدایت؟",
                fontSize = 18.sp,
                fontWeight = FontWeight.Bold,
                color = Color.White
            )

            OutlinedTextField(
                value = instructions,
                onValueChange = onChange,
                label = { Text("اضافی ہدایات (اختیاری)") },
                placeholder = { Text("مثلاً: تیز موسیقی کے ساتھ زوم ان اور شیک ایفیکٹ لگائیں...") },
                minLines = 4,
                colors = OutlinedTextFieldDefaults.colors(
                    focusedTextColor = Color.White,
                    unfocusedTextColor = Color.White,
                    focusedBorderColor = CyanGlow,
                    unfocusedBorderColor = SurfaceElevated
                ),
                shape = RoundedCornerShape(16.dp),
                modifier = Modifier
                    .fillMaxWidth()
                    .testTag("special_instructions_input")
            )
        }
    }
}

@Composable
fun Step5Summary(
    videoUri: Uri?,
    videoNote: String,
    cutTimings: String,
    style: String,
    instructions: String,
    onConfirmStart: () -> Unit
) {
    Card(
        colors = CardDefaults.cardColors(containerColor = SurfaceDark),
        shape = RoundedCornerShape(20.dp),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier.padding(20.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            Text(
                text = "5. ایڈیٹنگ پلان کا جائزہ",
                fontSize = 18.sp,
                fontWeight = FontWeight.Bold,
                color = Color.White
            )

            SummaryRow(label = "خیال / عنوان", value = videoNote.ifBlank { "خودکار ویڈیو ایڈیٹ" })
            SummaryRow(label = "منتخب ویڈیو", value = if (videoUri != null) "گیلری سے منتخب شدہ ✓" else "CapCut کی پہلے سے کھلی ویڈیو")
            SummaryRow(label = "کٹ ٹائمنگز", value = cutTimings.ifBlank { "MIRA کی صوابدید پر (Beat Sync)" })
            SummaryRow(label = "اسٹائل", value = style)
            if (instructions.isNotBlank()) {
                SummaryRow(label = "خاص ہدایات", value = instructions)
            }

            Spacer(modifier = Modifier.height(8.dp))

            Button(
                onClick = onConfirmStart,
                colors = ButtonDefaults.buttonColors(containerColor = CyanGlow),
                shape = RoundedCornerShape(18.dp),
                modifier = Modifier
                    .fillMaxWidth()
                    .height(58.dp)
                    .testTag("confirm_start_button")
            ) {
                Icon(imageVector = Icons.Default.PlayArrow, contentDescription = null, tint = MidnightDark)
                Spacer(modifier = Modifier.width(8.dp))
                Text(
                    text = "شروع کریں (Start Edit)",
                    color = MidnightDark,
                    fontSize = 18.sp,
                    fontWeight = FontWeight.Bold
                )
            }
        }
    }
}

@Composable
fun SummaryRow(label: String, value: String) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Text(text = label, color = Color(0xFF94A3B8), fontSize = 13.sp)
        Text(text = value, color = Color.White, fontWeight = FontWeight.SemiBold, fontSize = 13.sp)
    }
}
