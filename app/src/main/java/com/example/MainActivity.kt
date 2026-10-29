package com.example

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.BackHandler
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ListAlt
import androidx.compose.material.icons.filled.AddCircle
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.NavigationBarItemDefaults
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.LayoutDirection
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.agent.AgentRunner
import com.example.data.SecureStore
import com.example.ui.screens.HomeScreen
import com.example.ui.screens.LiveLogScreen
import com.example.ui.screens.NewEditScreen
import com.example.ui.screens.OnboardingScreen
import com.example.ui.screens.SettingsScreen
import com.example.ui.theme.CyanGlow
import com.example.ui.theme.EmeraldSuccess
import com.example.ui.theme.MidnightDark
import com.example.ui.theme.MyApplicationTheme
import com.example.ui.theme.RoseError
import com.example.ui.theme.SurfaceDark
import com.example.ui.theme.SurfaceElevated

enum class AppScreen {
    HOME,
    NEW_EDIT,
    LOGS,
    SETTINGS,
    ONBOARDING
}

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MyApplicationTheme {
                CompositionLocalProvider(LocalLayoutDirection provides LayoutDirection.Rtl) {
                    MiraMainApp()
                }
            }
        }
    }
}

@Composable
fun MiraMainApp() {
    val context = LocalContext.current
    val secureStore = remember { SecureStore(context) }
    var currentScreen by remember {
        mutableStateOf(if (secureStore.onboardingCompleted) AppScreen.HOME else AppScreen.ONBOARDING)
    }

    val safetyPrompt by AgentRunner.safetyPrompt.collectAsState()

    if (safetyPrompt != null) {
        AlertDialog(
            onDismissRequest = { AgentRunner.respondSafetyPermission(false) },
            containerColor = SurfaceDark,
            title = {
                Text(
                    text = "اجازت درکار ہے",
                    color = Color.White,
                    fontWeight = FontWeight.Bold,
                    fontSize = 18.sp
                )
            },
            text = {
                Text(
                    text = safetyPrompt ?: "",
                    color = Color(0xFFCBD5E1),
                    fontSize = 14.sp,
                    lineHeight = 20.sp
                )
            },
            confirmButton = {
                Button(
                    onClick = { AgentRunner.respondSafetyPermission(true) },
                    colors = ButtonDefaults.buttonColors(containerColor = EmeraldSuccess)
                ) {
                    Text("ہاں، اجازت دیں", color = Color.White, fontWeight = FontWeight.Bold)
                }
            },
            dismissButton = {
                TextButton(onClick = { AgentRunner.respondSafetyPermission(false) }) {
                    Text("منسوخ کریں", color = RoseError)
                }
            }
        )
    }

    if (currentScreen != AppScreen.HOME) {
        BackHandler {
            currentScreen = AppScreen.HOME
        }
    }

    Scaffold(
        modifier = Modifier.fillMaxSize(),
        bottomBar = {
            if (currentScreen != AppScreen.ONBOARDING) {
                NavigationBar(
                    containerColor = SurfaceDark,
                    tonalElevation = 8.dp
                ) {
                    NavigationBarItem(
                        selected = currentScreen == AppScreen.HOME,
                        onClick = { currentScreen = AppScreen.HOME },
                        icon = { Icon(Icons.Default.Home, contentDescription = "مرکزی صفحہ") },
                        label = { Text("مرکزی صفحہ", fontSize = 11.sp) },
                        colors = NavigationBarItemDefaults.colors(
                            selectedIconColor = CyanGlow,
                            selectedTextColor = CyanGlow,
                            unselectedIconColor = Color(0xFF94A3B8),
                            unselectedTextColor = Color(0xFF94A3B8),
                            indicatorColor = SurfaceElevated
                        )
                    )

                    NavigationBarItem(
                        selected = currentScreen == AppScreen.NEW_EDIT,
                        onClick = { currentScreen = AppScreen.NEW_EDIT },
                        icon = { Icon(Icons.Default.AddCircle, contentDescription = "نیا ایڈٹ") },
                        label = { Text("نیا ایڈٹ", fontSize = 11.sp) },
                        colors = NavigationBarItemDefaults.colors(
                            selectedIconColor = CyanGlow,
                            selectedTextColor = CyanGlow,
                            unselectedIconColor = Color(0xFF94A3B8),
                            unselectedTextColor = Color(0xFF94A3B8),
                            indicatorColor = SurfaceElevated
                        )
                    )

                    NavigationBarItem(
                        selected = currentScreen == AppScreen.LOGS,
                        onClick = { currentScreen = AppScreen.LOGS },
                        icon = { Icon(Icons.AutoMirrored.Filled.ListAlt, contentDescription = "لائیو لاگ") },
                        label = { Text("لائیو لاگ", fontSize = 11.sp) },
                        colors = NavigationBarItemDefaults.colors(
                            selectedIconColor = CyanGlow,
                            selectedTextColor = CyanGlow,
                            unselectedIconColor = Color(0xFF94A3B8),
                            unselectedTextColor = Color(0xFF94A3B8),
                            indicatorColor = SurfaceElevated
                        )
                    )

                    NavigationBarItem(
                        selected = currentScreen == AppScreen.SETTINGS,
                        onClick = { currentScreen = AppScreen.SETTINGS },
                        icon = { Icon(Icons.Default.Settings, contentDescription = "ترتیبات") },
                        label = { Text("ترتیبات", fontSize = 11.sp) },
                        colors = NavigationBarItemDefaults.colors(
                            selectedIconColor = CyanGlow,
                            selectedTextColor = CyanGlow,
                            unselectedIconColor = Color(0xFF94A3B8),
                            unselectedTextColor = Color(0xFF94A3B8),
                            indicatorColor = SurfaceElevated
                        )
                    )
                }
            }
        }
    ) { innerPadding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(MidnightDark)
                .padding(innerPadding)
        ) {
            when (currentScreen) {
                AppScreen.HOME -> HomeScreen(
                    onNavigateToNewEdit = { currentScreen = AppScreen.NEW_EDIT },
                    onNavigateToSettings = { currentScreen = AppScreen.SETTINGS },
                    onNavigateToOnboarding = { currentScreen = AppScreen.ONBOARDING }
                )
                AppScreen.NEW_EDIT -> NewEditScreen(
                    onJobStarted = { currentScreen = AppScreen.LOGS },
                    onNavigateBack = { currentScreen = AppScreen.HOME }
                )
                AppScreen.LOGS -> LiveLogScreen()
                AppScreen.SETTINGS -> SettingsScreen()
                AppScreen.ONBOARDING -> OnboardingScreen(
                    onFinish = { currentScreen = AppScreen.HOME }
                )
            }
        }
    }
}
