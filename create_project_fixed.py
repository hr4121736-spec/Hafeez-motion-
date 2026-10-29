#!/usr/bin/env python3
"""
MIRA AI - Complete Project Generator
Run this script with: python3 create_project.py
It creates the entire native Android project tree and all files.
"""

import os
import stat

FILES = {}

FILES[".env.example"] = """# GEMINI_API_KEY: Required for Gemini AI API calls.
# AI Studio injects this or you paste it in MIRA AI Settings.
# GEMINI_API_KEY=YOUR_FREE_GEMINI_API_KEY
"""

FILES[".gitignore"] = """*.iml
.gradle
.kotlin
/local.properties
/.idea/caches
/.idea/libraries
/.idea/modules.xml
/.idea/workspace.xml
/.idea/navEditor.xml
/.idea/assetWizardSettings.xml
.DS_Store
/build
/captures
.externalNativeBuild
.cxx
local.properties
.env
debug.keystore
"""

FILES["app/.gitignore"] = """/build
"""

FILES["gradle.properties"] = """org.gradle.jvmargs=-Xmx4g -Dfile.encoding=UTF-8
org.gradle.parallel=true
kotlin.code.style=official
android.nonTransitiveRClass=true
org.gradle.caching=true
org.gradle.configuration-cache=true
org.gradle.workers.max=4
kotlin.compiler.execution.strategy=in-process
googleServices.missing.passthrough=true
"""

FILES["settings.gradle.kts"] = """pluginManagement {
  repositories {
    google {
      content {
        includeGroupByRegex("com\\\\.android.*")
        includeGroupByRegex("com\\\\.google.*")
        includeGroupByRegex("androidx.*")
      }
    }
    mavenCentral()
    gradlePluginPortal()
  }
}

plugins { id("org.gradle.toolchains.foojay-resolver-convention") version "1.0.0" }

dependencyResolutionManagement {
  repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
  repositories {
    google()
    mavenCentral()
  }
}

rootProject.name = "MIRA AI"

include(":app")
"""

FILES["build.gradle.kts"] = """plugins {
  alias(libs.plugins.android.application) apply false
  alias(libs.plugins.kotlin.compose) apply false
  alias(libs.plugins.google.devtools.ksp) apply false
  alias(libs.plugins.secrets) apply false
  alias(libs.plugins.google.services) apply false
}
"""

FILES["gradle/wrapper/gradle-wrapper.properties"] = """distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-9.3.1-bin.zip
networkTimeout=10000
validateDistributionUrl=true
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
"""

FILES["gradle/libs.versions.toml"] = """[versions]
agp = "9.1.1"
coreKtx = "1.18.0"
junit = "4.13.2"
junitVersion = "1.3.0"
espressoCore = "3.7.0"
lifecycleRuntimeKtx = "2.8.7"
lifecycleViewmodelCompose = "2.8.7"
lifecycleRuntimeCompose = "2.8.7"
activityCompose = "1.10.1"
kotlin = "2.2.10"
composeBom = "2024.09.00"
googleDevtoolsKsp = "2.3.5"
navigationCompose = "2.8.9"
roomRuntime = "2.7.0"
roomKtx = "2.7.0"
roomCompiler = "2.7.0"
kotlinxCoroutinesTest = "1.10.2"
core = "1.6.1"
runner = "1.6.2"
coilCompose = "2.7.0"
retrofit = "2.12.0"
converterMoshi = "2.12.0"
kotlinxCoroutinesAndroid = "1.10.2"
kotlinxCoroutinesCore = "1.10.2"
accompanistPermissions = "0.37.3"
playServicesLocation = "21.3.0"
cameraCamera2 = "1.5.0"
cameraLifecycle = "1.5.0"
cameraView = "1.5.0"
cameraCore = "1.5.0"
loggingInterceptor = "4.10.0"
okhttp = "4.10.0"
moshiKotlin = "1.15.2"
moshiKotlinCodegen = "1.15.2"
datastorePreferences = "1.1.7"
robolectric = "4.16.1"
firebaseBom = "34.17.0"
secretsGradlePlugin = "2.0.1"
googleServices = "4.5.0"
credentials = "1.5.0"
googleid = "1.1.1"

[libraries]
androidx-core-ktx = { group = "androidx.core", name = "core-ktx", version.ref = "coreKtx" }
junit = { group = "junit", name = "junit", version.ref = "junit" }
androidx-junit = { group = "androidx.test.ext", name = "junit", version.ref = "junitVersion" }
androidx-espresso-core = { group = "androidx.test.espresso", name = "espresso-core", version.ref = "espressoCore" }
androidx-lifecycle-runtime-ktx = { group = "androidx.lifecycle", name = "lifecycle-runtime-ktx", version.ref = "lifecycleRuntimeKtx" }
androidx-lifecycle-viewmodel-compose = { group = "androidx.lifecycle", name = "lifecycle-viewmodel-compose", version.ref = "lifecycleViewmodelCompose" }
androidx-lifecycle-runtime-compose = { group = "androidx.lifecycle", name = "lifecycle-runtime-compose", version.ref = "lifecycleRuntimeCompose" }
androidx-activity-compose = { group = "androidx.activity", name = "activity-compose", version.ref = "activityCompose" }
androidx-compose-bom = { group = "androidx.compose", name = "compose-bom", version.ref = "composeBom" }
androidx-compose-ui = { group = "androidx.compose.ui", name = "ui" }
androidx-compose-ui-graphics = { group = "androidx.compose.ui", name = "ui-graphics" }
androidx-compose-ui-tooling = { group = "androidx.compose.ui", name = "ui-tooling" }
androidx-compose-ui-tooling-preview = { group = "androidx.compose.ui", name = "ui-tooling-preview" }
androidx-compose-ui-test-manifest = { group = "androidx.compose.ui", name = "ui-test-manifest" }
androidx-compose-ui-test-junit4 = { group = "androidx.compose.ui", name = "ui-test-junit4" }
androidx-navigation-compose = { group = "androidx.navigation", name = "navigation-compose", version.ref = "navigationCompose" }
androidx-room-runtime = { group = "androidx.room", name = "room-runtime", version.ref = "roomRuntime" }
androidx-room-ktx = { group = "androidx.room", name = "room-ktx", version.ref = "roomKtx" }
androidx-room-compiler = { group = "androidx.room", name = "room-compiler", version.ref = "roomCompiler" }
kotlinx-coroutines-test = { group = "org.jetbrains.kotlinx", name = "kotlinx-coroutines-test", version.ref = "kotlinxCoroutinesTest" }
androidx-core = { group = "androidx.test", name = "core", version.ref = "core" }
androidx-runner = { group = "androidx.test", name = "runner", version.ref = "runner" }
androidx-compose-material3 = { group = "androidx.compose.material3", name = "material3" }
androidx-compose-material-icons-core = { group = "androidx.compose.material", name = "material-icons-core" }
androidx-compose-material-icons-extended = { group = "androidx.compose.material", name = "material-icons-extended" }
coil-compose = { group = "io.coil-kt", name = "coil-compose", version.ref = "coilCompose" }
retrofit = { group = "com.squareup.retrofit2", name = "retrofit", version.ref = "retrofit" }
converter-moshi = { group = "com.squareup.retrofit2", name = "converter-moshi", version.ref = "converterMoshi" }
kotlinx-coroutines-android = { group = "org.jetbrains.kotlinx", name = "kotlinx-coroutines-android", version.ref = "kotlinxCoroutinesAndroid" }
kotlinx-coroutines-core = { group = "org.jetbrains.kotlinx", name = "kotlinx-coroutines-core", version.ref = "kotlinxCoroutinesCore" }
accompanist-permissions = { group = "com.google.accompanist", name = "accompanist-permissions", version.ref = "accompanistPermissions" }
play-services-location = { group = "com.google.android.gms", name = "play-services-location", version.ref = "playServicesLocation" }
androidx-camera-camera2 = { group = "androidx.camera", name = "camera-camera2", version.ref = "cameraCamera2" }
androidx-camera-lifecycle = { group = "androidx.camera", name = "camera-lifecycle", version.ref = "cameraLifecycle" }
androidx-camera-view = { group = "androidx.camera", name = "camera-view", version.ref = "cameraView" }
androidx-camera-core = { group = "androidx.camera", name = "camera-core", version.ref = "cameraCore" }
logging-interceptor = { group = "com.squareup.okhttp3", name = "logging-interceptor", version.ref = "loggingInterceptor" }
okhttp = { group = "com.squareup.okhttp3", name = "okhttp", version.ref = "okhttp" }
moshi-kotlin = { group = "com.squareup.moshi", name = "moshi-kotlin", version.ref = "moshiKotlin" }
moshi-kotlin-codegen = { group = "com.squareup.moshi", name = "moshi-kotlin-codegen", version.ref = "moshiKotlinCodegen" }
androidx-datastore-preferences = { group = "androidx.datastore", name = "datastore-preferences", version.ref = "datastorePreferences" }
robolectric = { group = "org.robolectric", name = "robolectric", version.ref = "robolectric" }
firebase-bom = { group = "com.google.firebase", name = "firebase-bom", version.ref = "firebaseBom" }
firebase-ai = { group = "com.google.firebase", name = "firebase-ai" }
firebase-appcheck-recaptcha = { group = "com.google.firebase", name = "firebase-appcheck-recaptcha" }
firebase-appcheck-debug = { group = "com.google.firebase", name = "firebase-appcheck-debug" }
firebase-firestore = { group = "com.google.firebase", name = "firebase-firestore" }
firebase-auth = { group = "com.google.firebase", name = "firebase-auth" }
androidx-credentials = { group = "androidx.credentials", name = "credentials", version.ref = "credentials" }
androidx-credentials-play-services = { group = "androidx.credentials", name = "credentials-play-services-auth", version.ref = "credentials" }
googleid = { group = "com.google.android.libraries.identity.googleid", name = "googleid", version.ref = "googleid" }

[plugins]
android-application = { id = "com.android.application", version.ref = "agp" }
kotlin-compose = { id = "org.jetbrains.kotlin.plugin.compose", version.ref = "kotlin" }
google-devtools-ksp = { id = "com.google.devtools.ksp", version.ref = "googleDevtoolsKsp" }
secrets = { id = "com.google.android.libraries.mapsplatform.secrets-gradle-plugin", version.ref = "secretsGradlePlugin" }
google-services = { id = "com.google.gms.google-services", version.ref = "googleServices" }
"""

FILES["gradlew"] = """#!/bin/sh
APP_BASE_NAME=`basename "$0"`
APP_HOME="`pwd -P`"

PRG="$0"
while [ -h "$PRG" ] ; do
    ls=`ls -ld "$PRG"`
    link=`expr "$ls" : '.*-> \\(.*\\)$'`
    if expr "$link" : '/.*' > /dev/null; then
        PRG="$link"
    else
        PRG=`dirname "$PRG"`"/$link"
    fi
done
SAVED="`pwd`"
cd "`dirname \\"$PRG\\"`" >/dev/null
APP_HOME="`pwd -P`"
cd "$SAVED" >/dev/null

CLASSPATH=$APP_HOME/gradle/wrapper/gradle-wrapper.jar

if [ -n "$JAVA_HOME" ] ; then
    if [ -x "$JAVA_HOME/jre/sh/java" ] ; then
        JAVACMD="$JAVA_HOME/jre/sh/java"
    else
        JAVACMD="$JAVA_HOME/bin/java"
    fi
else
    JAVACMD="java"
fi

exec "$JAVACMD" "-Dorg.gradle.appname=$APP_BASE_NAME" -classpath "$CLASSPATH" org.gradle.wrapper.GradleWrapperMain "$@"
"""

FILES["gradlew.bat"] = """@rem
@if "%DEBUG%" == "" @echo off
set DIRNAME=%~dp0
if "%DIRNAME%" == "" set DIRNAME=.
set APP_BASE_NAME=%~n0
set APP_HOME=%DIRNAME%

set JAVA_EXE=java.exe
%JAVA_EXE% -version >NUL 2>&1
if "%ERRORLEVEL%" == "0" goto init

if defined JAVA_HOME goto findJavaFromJavaHome

@echo.
@echo ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH.
goto fail

:findJavaFromJavaHome
set JAVA_HOME=%JAVA_HOME:"=%
set JAVA_EXE=%JAVA_HOME%/bin/java.exe

:init
set CLASSPATH=%APP_HOME%\\gradle\\wrapper\\gradle-wrapper.jar
"%JAVA_EXE%" -classpath "%CLASSPATH%" org.gradle.wrapper.GradleWrapperMain %*
:fail
exit /b 1
"""

FILES[".github/workflows/build-apk.yml"] = """name: Build MIRA AI APK

on:
  push:
    branches: [ "main", "master" ]
  pull_request:
    branches: [ "main", "master" ]
  workflow_dispatch:

jobs:
  build:
    name: Build Debug APK
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'

      - name: Setup Android SDK
        uses: android-actions/setup-android@v3

      - name: Create debug keystore
        run: |
          keytool -genkeypair -v -keystore debug.keystore -storepass android \\
            -alias androiddebugkey -keypass android -keyalg RSA -keysize 2048 \\
            -validity 10000 -dname "CN=Android Debug,O=Android,C=US"

      - name: Set up Gradle
        uses: gradle/actions/setup-gradle@v4
        with:
          gradle-version: '9.3.1'

      - name: Build Debug APK with Gradle
        run: gradle assembleDebug --stacktrace

      - name: Upload Debug APK Artifact
        uses: actions/upload-artifact@v4
        with:
          name: MIRA-AI-debug-apk
          path: app/build/outputs/apk/debug/*.apk
          retention-days: 30
"""

FILES["app/proguard-rules.pro"] = """-dontwarn okhttp3.**
-dontwarn okio.**
-keepattributes *Annotation*,Signature,InnerClasses,EnclosingMethod
"""

FILES["app/build.gradle.kts"] = """import com.google.gms.googleservices.GoogleServicesPlugin.MissingGoogleServicesStrategy

plugins {
  alias(libs.plugins.android.application)
  alias(libs.plugins.kotlin.compose)
  alias(libs.plugins.google.devtools.ksp)
  alias(libs.plugins.secrets)
  alias(libs.plugins.google.services)
}

android {
  namespace = "com.example"
  compileSdk { version = release(36) { minorApiLevel = 1 } }

  defaultConfig {
    applicationId = "com.aistudio.miraai.vkzqtr"
    minSdk = 30
    targetSdk = 34
    versionCode = 1
    versionName = "1.0"

    testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
  }

  signingConfigs {
    create("release") {
      val keystorePath = System.getenv("KEYSTORE_PATH") ?: "${rootDir}/my-upload-key.jks"
      storeFile = file(keystorePath)
      storePassword = System.getenv("STORE_PASSWORD")
      keyAlias = "upload"
      keyPassword = System.getenv("KEY_PASSWORD")
    }
    create("debugConfig") {
      storeFile = file("${rootDir}/debug.keystore")
      storePassword = "android"
      keyAlias = "androiddebugkey"
      keyPassword = "android"
    }
  }

  buildTypes {
    release {
      isCrunchPngs = false
      isMinifyEnabled = false
      proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
      signingConfig = signingConfigs.getByName("release")
    }
    debug {
      signingConfig = signingConfigs.getByName("debugConfig")
    }
  }
  compileOptions {
    sourceCompatibility = JavaVersion.VERSION_11
    targetCompatibility = JavaVersion.VERSION_11
  }
  buildFeatures {
    compose = true
    buildConfig = true
  }
  testOptions { unitTests { isIncludeAndroidResources = true } }
  dependenciesInfo {
    includeInApk = false
    includeInBundle = true
  }
}

secrets {
  propertiesFileName = ".env"
  defaultPropertiesFileName = ".env.example"
  ignoreList.add("FIREBASE_APPCHECK_DEBUG_TOKEN")
}

googleServices { missingGoogleServicesStrategy = MissingGoogleServicesStrategy.WARN }

dependencies {
  implementation(platform(libs.androidx.compose.bom))
  implementation(platform(libs.firebase.bom))
  implementation(libs.androidx.activity.compose)
  implementation(libs.androidx.compose.material.icons.core)
  implementation(libs.androidx.compose.material.icons.extended)
  implementation(libs.androidx.compose.material3)
  implementation(libs.androidx.compose.ui)
  implementation(libs.androidx.compose.ui.graphics)
  implementation(libs.androidx.compose.ui.tooling.preview)
  implementation(libs.androidx.core.ktx)
  implementation(libs.androidx.lifecycle.runtime.compose)
  implementation(libs.androidx.lifecycle.runtime.ktx)
  implementation(libs.androidx.lifecycle.viewmodel.compose)
  implementation(libs.androidx.room.ktx)
  implementation(libs.androidx.room.runtime)
  implementation(libs.converter.moshi)
  implementation(libs.firebase.ai)
  implementation(libs.firebase.appcheck.recaptcha)
  implementation(libs.firebase.appcheck.debug)
  implementation(libs.kotlinx.coroutines.android)
  implementation(libs.kotlinx.coroutines.core)
  implementation(libs.logging.interceptor)
  implementation(libs.moshi.kotlin)
  implementation(libs.okhttp)
  implementation(libs.retrofit)
  testImplementation(libs.androidx.compose.ui.test.junit4)
  testImplementation(libs.androidx.core)
  testImplementation(libs.androidx.junit)
  testImplementation(libs.junit)
  testImplementation(libs.kotlinx.coroutines.test)
  testImplementation(libs.robolectric)
  androidTestImplementation(platform(libs.androidx.compose.bom))
  androidTestImplementation(libs.androidx.compose.ui.test.junit4)
  androidTestImplementation(libs.androidx.espresso.core)
  androidTestImplementation(libs.androidx.junit)
  androidTestImplementation(libs.androidx.runner)
  debugImplementation(libs.androidx.compose.ui.test.manifest)
  debugImplementation(libs.androidx.compose.ui.tooling)
  "ksp"(libs.androidx.room.compiler)
  "ksp"(libs.moshi.kotlin.codegen)
}
"""

FILES["app/src/main/AndroidManifest.xml"] = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.SYSTEM_ALERT_WINDOW" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE_SPECIAL_USE" />
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
    <uses-permission android:name="android.permission.READ_MEDIA_VIDEO" />
    <uses-permission
        android:name="android.permission.READ_EXTERNAL_STORAGE"
        android:maxSdkVersion="32" />

    <queries>
        <package android:name="com.lemon.lvoverseas" />
        <package android:name="com.lemon.lvoverseas.lite" />
        <package android:name="com.capcut.videoeditor" />
        <package android:name="com.lemon.kinevideo" />
    </queries>

    <application
        android:allowBackup="true"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.MyApplication">

        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:label="@string/app_name"
            android:windowSoftInputMode="adjustResize"
            android:theme="@style/Theme.MyApplication">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <service
            android:name=".service.MiraAccessibilityService"
            android:permission="android.permission.BIND_ACCESSIBILITY_SERVICE"
            android:exported="true">
            <intent-filter>
                <action android:name="android.accessibilityservice.AccessibilityService" />
            </intent-filter>
            <meta-data
                android:name="android.accessibilityservice"
                android:resource="@xml/accessibility_service_config" />
        </service>

        <service
            android:name=".service.OverlayService"
            android:foregroundServiceType="specialUse"
            android:exported="false">
            <property
                android:name="android.app.PROPERTY_SPECIAL_USE_FGS_SUBTYPE"
                android:value="Floating video editing control overlay for MIRA AI" />
        </service>

        <service
            android:name=".service.AgentRunnerService"
            android:foregroundServiceType="specialUse"
            android:exported="false">
            <property
                android:name="android.app.PROPERTY_SPECIAL_USE_FGS_SUBTYPE"
                android:value="Autonomous video editing agent runner executing reasoning loops" />
        </service>

    </application>

</manifest>
"""

FILES["app/src/main/res/values/strings.xml"] = """<resources>
    <string name="app_name">MIRA AI</string>
    <string name="accessibility_service_description">میرا اے آئی (MIRA AI) خودکار ویڈیو ایڈیٹنگ کے لیے CapCut میں اسکرین پڑھ کر اشارے اور کٹس انجام دیتی ہے۔</string>

    <string name="nav_home">مرکزی صفحہ</string>
    <string name="nav_new_edit">نیا ایڈٹ</string>
    <string name="nav_logs">لائیو لاگ</string>
    <string name="nav_settings">ترتیبات</string>

    <string name="status_ready">MIRA تیار ہے</string>
    <string name="status_off">MIRA بند ہے</string>
    <string name="status_ready_desc">تمام اجازتیں اور API کی فعال ہیں۔ آپ نیا ایڈیٹنگ ٹاسک شروع کر سکتے ہیں۔</string>
    <string name="status_off_desc">کچھ اہم اجازتیں یا ترتیبات باقی ہیں۔ نیچے دیے گئے بٹن سے سیٹ اپ مکمل کریں۔</string>
    <string name="permission_accessibility">رسائی سروس (Accessibility Service)</string>
    <string name="permission_overlay">اسکرین اوورلے (Display Over Other Apps)</string>
    <string name="permission_api_key">گوگل جیمنائی کی (Gemini API Key)</string>
    <string name="permission_notification">اطلاعات (Notifications)</string>
    <string name="btn_fix">سیٹ کریں</string>
    <string name="btn_start_new_edit">نیا ایڈٹ شروع کریں</string>
    <string name="recent_jobs_title">حالیہ ایڈیٹنگ ٹاسکس</string>
    <string name="no_recent_jobs">ابھی تک کوئی ٹاسک نہیں چلایا گیا</string>

    <string name="step_1_title">1. آج کون سی ویڈیو بنانی ہے؟</string>
    <string name="step_1_pick_video">گیلری سے ویڈیو منتخب کریں</string>
    <string name="step_1_note_hint">ویڈیو کا خیال یا تھیم لکھیں (مثلاً موٹر بائیک ڈرائیو یا ایونٹ کلپ)...</string>
    <string name="step_2_title">2. کٹ کس سیکنڈ پر لگانے ہیں؟</string>
    <string name="step_2_hint">کٹ سیکنڈز لکھیں، مثلاً: 2.5, 5.0, 7.8 (اختیاری)</string>
    <string name="step_3_title">3. کون سا اسٹائل؟</string>
    <string name="step_4_title">4. کوئی خاص ہدایت؟</string>
    <string name="step_4_hint">مثلاً: فلٹر، موسیقی، سلو مو، آٹو کیپشن یا ٹیکسٹ وغیرہ...</string>
    <string name="step_5_title">5. ایڈیٹنگ پلان کا جائزہ</string>
    <string name="btn_start_job">شروع کریں</string>
    <string name="btn_next">اگلا مرحلہ</string>
    <string name="btn_prev">پچھلا مرحلہ</string>

    <string name="style_auto">MIRA خود فیصلہ کرے</string>
    <string name="style_rampage">ریمپیج (Rampage)</string>
    <string name="style_velocity">وائلوسیٹی (Velocity)</string>
    <string name="style_slomo">اسموتھ سلو مو (Smooth Slow-Mo)</string>
    <string name="style_cinematic">سنیماٹک (Cinematic)</string>

    <string name="settings_title">ترتیبات اور ماڈل</string>
    <string name="setting_api_key_label">Gemini API Key</string>
    <string name="setting_api_key_hint">AI Studio سے حاصل کردہ مفت کی یہاں پیسٹ کریں</string>
    <string name="setting_model_label">جیمنائی ماڈل</string>
    <string name="setting_delay_label">ہر ایکشن میں وقفہ (ملی سیکنڈ)</string>
    <string name="setting_max_steps_label">زیادہ سے زیادہ مراحل (Max Steps)</string>
    <string name="setting_max_retries_label">زیادہ سے زیادہ کوششیں (Retries)</string>
    <string name="setting_ask_export_label">ایکسپورٹ سے پہلے مجھ سے اجازت لیں</string>
    <string name="setting_proactive_label">خود سے بہتری تجویز کریں</string>
    <string name="setting_capcut_pkg_label">CapCut پیکیج منتخب کریں</string>
    <string name="btn_test_api_key">API کی ٹیسٹ کریں</string>
    <string name="btn_reset_memory">سیکھی ہوئی میموری صاف کریں</string>
    <string name="api_test_success">ماشاءاللہ! API کی بالکل درست ہے اور جیمنائی سے رابطہ ہو گیا ہے۔</string>
    <string name="api_test_failed">API کی کی تصدیق ناکام ہو گئی۔ براہ کرم کی درستگی چیک کریں۔</string>

    <string name="logs_title">لائیو لاگ اور ایکشن ہسٹری</string>
    <string name="btn_share_logs">لاگ شیئر / محفوظ کریں</string>
    <string name="btn_clear_logs">لاگ صاف کریں</string>
    <string name="no_logs_yet">کوئی ایکشن لاگ موجود نہیں</string>

    <string name="overlay_stop">روکیں</string>
    <string name="overlay_pause">وقفہ</string>
    <string name="overlay_resume">جاری رکھیں</string>
    <string name="overlay_waiting">MIRA انتظار کر رہی ہے...</string>
    <string name="overlay_working">MIRA کام کر رہی ہے...</string>
    <string name="overlay_permission_needed">اجازت درکار ہے: کیا MIRA ایکسپورٹ / محفوظ کرے؟</string>
    <string name="btn_confirm_yes">ہاں، اجازت دیں</string>
    <string name="btn_confirm_no">نہیں، منسوخ کریں</string>

    <string name="onboarding_title">MIRA AI سیٹ اپ ویژرڈ</string>
    <string name="onboarding_step1">1. Gemini API کی شامل کریں (Google AI Studio سے مفت حاصل کریں)</string>
    <string name="onboarding_step2">2. اطلاعات (Notifications) کی اجازت دیں</string>
    <string name="onboarding_step3">3. دیگر ایپس پر ظاہر ہونے کی اجازت (Overlay)</string>
    <string name="onboarding_step4">4. رسائی سروس (Accessibility Service) آن کریں</string>
    <string name="onboarding_step4_help">اگر آپ کا فون Android 13+ ہے اور سوئچ گرے ہے: فون کی Settings > Apps > MIRA AI > تین نقطوں (Three dots) پر ٹیپ کریں اور "Allow restricted settings" آن کریں۔</string>
    <string name="onboarding_step5">5. CapCut کھولیں اور واپس آئیں</string>
    <string name="btn_open_settings">سیٹنگز کھولیں</string>
    <string name="btn_open_capcut">CapCut کھولیں</string>
    <string name="btn_complete_setup">سیٹ اپ مکمل ہوا</string>
</resources>
"""

FILES["app/src/main/res/values/colors.xml"] = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="purple_200">#FFBB86FC</color>
    <color name="purple_500">#FF6200EE</color>
    <color name="purple_700">#FF3700B3</color>
    <color name="teal_200">#FF03DAC5</color>
    <color name="teal_700">#FF018786</color>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
</resources>
"""

FILES["app/src/main/res/values/themes.xml"] = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.MyApplication" parent="android:Theme.DeviceDefault.NoActionBar" />
</resources>
"""

FILES["app/src/main/res/xml/accessibility_service_config.xml"] = """<?xml version="1.0" encoding="utf-8"?>
<accessibility-service xmlns:android="http://schemas.android.com/apk/res/android"
    android:description="@string/accessibility_service_description"
    android:accessibilityEventTypes="typeAllMask"
    android:accessibilityFeedbackType="feedbackGeneric"
    android:notificationTimeout="100"
    android:accessibilityFlags="flagDefault|flagReportViewIds|flagRetrieveInteractiveWindows|flagIncludeNotImportantViews"
    android:canRetrieveWindowContent="true"
    android:canPerformGestures="true"
    android:canTakeScreenshot="true"
    android:packageNames="com.lemon.lvoverseas,com.lemon.lvoverseas.lite,com.capcut.videoeditor,com.lemon.kinevideo,com.aistudio.miraai.vkzqtr,com.example" />
"""

FILES["app/src/main/res/xml/backup_rules.xml"] = """<?xml version="1.0" encoding="utf-8"?>
<full-backup-content>
</full-backup-content>
"""

FILES["app/src/main/res/xml/data_extraction_rules.xml"] = """<?xml version="1.0" encoding="utf-8"?>
<data-extraction-rules>
    <cloud-backup>
    </cloud-backup>
</data-extraction-rules>
"""

FILES["app/src/main/res/drawable/ic_launcher_background.xml"] = """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path
        android:fillColor="#0F172A"
        android:pathData="M0,0h108v108h-108z" />
</vector>
"""

FILES["app/src/main/res/drawable/ic_launcher_foreground.xml"] = """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path
        android:fillColor="#06B6D4"
        android:pathData="M38,30L78,54L38,78Z" />
    <path
        android:fillColor="#EC4899"
        android:pathData="M24,20h8v68h-8zM76,20h8v68h-8z" />
</vector>
"""

FILES["app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml"] = """<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/ic_launcher_background" />
    <foreground android:drawable="@drawable/ic_launcher_foreground" />
</adaptive-icon>
"""

FILES["app/src/main/res/mipmap-anydpi-v26/ic_launcher_round.xml"] = """<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/ic_launcher_background" />
    <foreground android:drawable="@drawable/ic_launcher_foreground" />
</adaptive-icon>
"""

FILES["app/src/main/res/raw/system_prompt.txt"] = """You are MIRA, an autonomous personal video-editing agent that operates the CapCut video editor directly on Android through an Accessibility Service.
You control the device ONLY through the structured JSON action format specified below.
Never attempt to interact with or switch to any other application except CapCut and MIRA AI.
All your internal thoughts for the user log and overlay ("thought_urdu") MUST be written in natural, conversational URDU (Urdu script).

Core Operating Principles:
1. Work in small, deliberate steps: execute one atomic action at a time, wait for the screen to settle, and observe the updated UI state.
2. Dual observation strategy:
   - Always analyze the structured UI tree first (fast and cheap). When an interactive element exists in the tree, set "target_node_index" to its numeric index rather than using raw coordinates.
   - If the UI tree is insufficient (custom canvas, timeline handles, video preview, or missing labels), rely on the provided screenshot. The screenshot coordinates (x, y) should be specified in the 0..1080 coordinate space of the downscaled screenshot.
3. Strict Safety Gates:
   - NEVER tap "Export", "Save", "Share", "Post", "Delete", or proceed with any payment, Pro subscription, Google Sign-in, or purchase dialog without first returning the "request_permission" action with a clear Urdu explanation.
   - If CapCut displays a VIP/Pro feature banner or paywall, dismiss/close it immediately and select a free alternative feature. Never spend money.
   - Never delete original media files.
4. When uncertain or trapped in an ambiguous UI state, return the "ask_user" action with a precise question in Urdu instead of guessing.
5. Default to vertical 9:16 aspect ratio unless the user instructions specify otherwise.

CapCut Operational Knowledge & Editing Workflow:
- New Project Flow:
  From CapCut's home screen, locate and tap "New project" (or "+" button), locate the user's requested video from the gallery picker, and tap "Add" / "Import".
- Applying Cuts / Splits:
  On the timeline, calculate the target timecode or drag the playhead along the ruler to the requested second marks (e.g., 2.5s, 5.0s, 7.8s). Tap the clip to highlight it, then tap "Split" (or scissors icon). Repeat for each cut marker.
- Speed Editing (Velocity / Rampage style):
  Select the target split segment -> tap "Speed" -> tap "Curve" -> select a dynamic speed curve (e.g., Montage, Hero, Bullet, or Flash) to slow down the impact/drop and accelerate transitions.
- Transitions & Visual Effects:
  Between cuts, tap the transition transition square on the timeline -> choose clean cinematic or dynamic cuts (such as Zoom, Flash, or Glitch).
  Under "Effects" -> "Video Effects", select fitting aesthetic overlays (subtle camera shake, chromatic glow, or cinematic grain).
- Audio & Beat Sync:
  If adding audio or matching beats, align cuts with beat markers.
- Proactive Enhancements (when enabled in settings):
  If footage is shaky, check clip options for "Stabilize". Lightly boost saturation and contrast under "Adjust" if flat. Add a subtle zoom punch on major beat drops.
- Finalization:
  Navigate to the top-right export area. Check resolution (1080p, 30/60fps). Do NOT tap export until receiving explicit user confirmation via "request_permission".

JSON Action Output Contract:
You must ALWAYS respond with a single valid JSON object following this exact schema:
{
  "thought_urdu": "اردو میں ایک مختصر جملہ جو بتائے کہ آپ کیا کر رہے ہیں اور کیوں",
  "screen_summary": "One sentence in English summarizing what you see on the screen",
  "action": "tap" | "long_press" | "swipe" | "drag" | "pinch" | "type_text" | "back" | "home" | "open_app" | "wait" | "scroll" | "request_permission" | "ask_user" | "done" | "fail",
  "x": number or null,
  "y": number or null,
  "x2": number or null,
  "y2": number or null,
  "duration_ms": number or null,
  "text": string or null,
  "target_node_index": number or null,
  "expected_result": "Clear English statement of what change should be visible after this action",
  "progress_percent": integer 0 to 100
}
"""

FILES["app/src/main/java/com/example/model/ActionModels.kt"] = """package com.example.model

import android.graphics.Bitmap
import android.graphics.Rect

enum class JobStatus {
    IDLE,
    RUNNING,
    PAUSED,
    WAITING_PERMISSION,
    WAITING_USER,
    COMPLETED,
    FAILED,
    STOPPED
}

enum class ActionType {
    TAP,
    LONG_PRESS,
    SWIPE,
    DRAG,
    PINCH,
    TYPE_TEXT,
    BACK,
    HOME,
    OPEN_APP,
    WAIT,
    SCROLL,
    REQUEST_PERMISSION,
    ASK_USER,
    DONE,
    FAIL;

    companion object {
        fun fromString(value: String): ActionType {
            return entries.firstOrNull { it.name.equals(value.trim(), ignoreCase = true) } ?: WAIT
        }
    }
}

data class ActionResponse(
    val thoughtUrdu: String = "",
    val screenSummary: String = "",
    val action: ActionType = ActionType.WAIT,
    val x: Float? = null,
    val y: Float? = null,
    val x2: Float? = null,
    val y2: Float? = null,
    val durationMs: Long? = null,
    val text: String? = null,
    val targetNodeIndex: Int? = null,
    val expectedResult: String = "",
    val progressPercent: Int = 0
)

data class UiNode(
    val index: Int,
    val className: String,
    val text: String,
    val contentDescription: String,
    val viewIdResourceName: String,
    val bounds: Rect,
    val clickable: Boolean,
    val scrollable: Boolean,
    val editable: Boolean,
    val enabled: Boolean
)

data class ObservationResult(
    val treeJson: String,
    val nodes: List<UiNode>,
    val screenshot: Bitmap?,
    val screenshotBase64: String?,
    val scaleFactorX: Float = 1.0f,
    val scaleFactorY: Float = 1.0f,
    val packageName: String = "",
    val windowTitle: String = ""
)

data class StepLog(
    val stepNumber: Int,
    val timestamp: Long = System.currentTimeMillis(),
    val thoughtUrdu: String,
    val screenSummary: String,
    val actionName: String,
    val resultUrdu: String,
    val isSuccess: Boolean = true,
    val apiCalls: Int = 0
)

data class EditJob(
    val id: String = java.util.UUID.randomUUID().toString(),
    val videoUri: String? = null,
    val videoNote: String = "",
    val cutTimings: String = "",
    val style: String = "MIRA خود فیصلہ کرے",
    val instructions: String = "",
    val status: JobStatus = JobStatus.IDLE,
    val progress: Int = 0,
    val createdAt: Long = System.currentTimeMillis(),
    val apiCallsCount: Int = 0
)

data class SkillRecord(
    val capcutVersion: String,
    val label: String,
    val viewId: String? = null,
    val relativeX: Float = 0.5f,
    val relativeY: Float = 0.5f
)
"""

FILES["app/src/main/java/com/example/data/SecureStore.kt"] = """package com.example.data

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
        get() = prefs.getString(PREF_MODEL_NAME, "gemini-2.5-flash") ?: "gemini-2.5-flash"
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
"""

FILES["app/src/main/java/com/example/data/SkillsStore.kt"] = """package com.example.data

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
        return label.trim().lowercase().replace("\\\\s+".toRegex(), "_")
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
"""

FILES["app/src/main/java/com/example/service/MiraAccessibilityService.kt"] = """package com.example.service

import android.accessibilityservice.AccessibilityService
import android.accessibilityservice.GestureDescription
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.ColorSpace
import android.graphics.Path
import android.graphics.Rect
import android.hardware.HardwareBuffer
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.util.Base64
import android.view.Display
import android.view.accessibility.AccessibilityEvent
import android.view.accessibility.AccessibilityNodeInfo
import com.example.model.ObservationResult
import com.example.model.UiNode
import kotlinx.coroutines.suspendCancellableCoroutine
import org.json.JSONArray
import org.json.JSONObject
import java.io.ByteArrayOutputStream
import java.util.concurrent.Executor
import kotlin.coroutines.resume

class MiraAccessibilityService : AccessibilityService() {

    companion object {
        @Volatile
        var instance: MiraAccessibilityService? = null
            private set

        fun isServiceRunning(): Boolean = instance != null
    }

    private val mainHandler = Handler(Looper.getMainLooper())
    private val mainExecutor = Executor { command -> mainHandler.post(command) }
    private var lastForegroundPackage: String = ""

    override fun onServiceConnected() {
        super.onServiceConnected()
        instance = this
    }

    override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        event?.packageName?.toString()?.let {
            if (it.isNotBlank()) {
                lastForegroundPackage = it
            }
        }
    }

    override fun onInterrupt() {}

    override fun onDestroy() {
        super.onDestroy()
        if (instance == this) {
            instance = null
        }
    }

    fun getCurrentPackageName(): String {
        val root = rootInActiveWindow
        val pkg = root?.packageName?.toString() ?: lastForegroundPackage
        root?.recycle()
        return pkg
    }

    fun isAllowedForeground(): Boolean {
        val pkg = getCurrentPackageName()
        return pkg.contains("lemon") ||
                pkg.contains("capcut") ||
                pkg.contains("mira") ||
                pkg.contains("example")
    }

    suspend fun observe(includeScreenshot: Boolean = true): ObservationResult {
        val nodes = mutableListOf<UiNode>()
        val root = rootInActiveWindow
        val currentPkg = root?.packageName?.toString() ?: lastForegroundPackage
        val windowTitle = root?.text?.toString() ?: ""

        if (root != null) {
            flattenTree(root, nodes)
            root.recycle()
        }

        val treeJson = buildTreeJson(nodes)

        var screenshot: Bitmap? = null
        var base64Jpeg: String? = null
        var scaleX = 1.0f
        var scaleY = 1.0f

        if (includeScreenshot) {
            val rawBmp = captureScreenshot()
            if (rawBmp != null) {
                val origW = rawBmp.width
                val origH = rawBmp.height
                val maxDim = 1080
                val longSide = maxOf(origW, origH)

                val scaledBmp = if (longSide > maxDim) {
                    val scale = maxDim.toFloat() / longSide
                    val targetW = (origW * scale).toInt().coerceAtLeast(1)
                    val targetH = (origH * scale).toInt().coerceAtLeast(1)
                    scaleX = origW.toFloat() / targetW
                    scaleY = origH.toFloat() / targetH
                    Bitmap.createScaledBitmap(rawBmp, targetW, targetH, true).also {
                        if (it != rawBmp) rawBmp.recycle()
                    }
                } else {
                    scaleX = 1.0f
                    scaleY = 1.0f
                    rawBmp
                }

                val stream = ByteArrayOutputStream()
                scaledBmp.compress(Bitmap.CompressFormat.JPEG, 70, stream)
                val bytes = stream.toByteArray()
                base64Jpeg = Base64.encodeToString(bytes, Base64.NO_WRAP)
                screenshot = scaledBmp
            }
        }

        return ObservationResult(
            treeJson = treeJson,
            nodes = nodes,
            screenshot = screenshot,
            screenshotBase64 = base64Jpeg,
            scaleFactorX = scaleX,
            scaleFactorY = scaleY,
            packageName = currentPkg,
            windowTitle = windowTitle
        )
    }

    private suspend fun captureScreenshot(): Bitmap? = suspendCancellableCoroutine { cont ->
        try {
            takeScreenshot(
                Display.DEFAULT_DISPLAY,
                mainExecutor,
                object : TakeScreenshotCallback {
                    override fun onSuccess(result: ScreenshotResult) {
                        val hardwareBuffer = result.hardwareBuffer
                        val colorSpace = result.colorSpace ?: ColorSpace.get(ColorSpace.Named.SRGB)
                        val bmp = Bitmap.wrapHardwareBuffer(hardwareBuffer, colorSpace)
                        hardwareBuffer.close()

                        val softwareBmp = bmp?.copy(Bitmap.Config.ARGB_8888, false)
                        bmp?.recycle()
                        if (cont.isActive) {
                            cont.resume(softwareBmp)
                        }
                    }

                    override fun onFailure(errorCode: Int) {
                        if (cont.isActive) {
                            cont.resume(null)
                        }
                    }
                }
            )
        } catch (_: Exception) {
            if (cont.isActive) {
                cont.resume(null)
            }
        }
    }

    private fun flattenTree(node: AccessibilityNodeInfo, list: MutableList<UiNode>) {
        val bounds = Rect()
        node.getBoundsInScreen(bounds)

        val text = node.text?.toString() ?: ""
        val desc = node.contentDescription?.toString() ?: ""
        val viewId = node.viewIdResourceName ?: ""
        val className = node.className?.toString() ?: ""

        val isUseful = text.isNotBlank() ||
                desc.isNotBlank() ||
                viewId.isNotBlank() ||
                node.isClickable ||
                node.isEditable ||
                node.isScrollable

        if (isUseful) {
            list.add(
                UiNode(
                    index = list.size,
                    className = className,
                    text = text.take(60),
                    contentDescription = desc.take(60),
                    viewIdResourceName = viewId,
                    bounds = bounds,
                    clickable = node.isClickable,
                    scrollable = node.isScrollable,
                    editable = node.isEditable,
                    enabled = node.isEnabled
                )
            )
        }

        for (i in 0 until node.childCount) {
            val child = node.getChild(i) ?: continue
            flattenTree(child, list)
            child.recycle()
        }
    }

    private fun buildTreeJson(nodes: List<UiNode>): String {
        val array = JSONArray()
        for (node in nodes.take(40)) {
            val obj = JSONObject().apply {
                put("idx", node.index)
                if (node.text.isNotBlank()) put("text", node.text)
                if (node.contentDescription.isNotBlank()) put("desc", node.contentDescription)
                if (node.viewIdResourceName.isNotBlank()) put("id", node.viewIdResourceName.substringAfterLast('/'))
                put("x", node.bounds.centerX())
                put("y", node.bounds.centerY())
                if (node.clickable) put("click", true)
                if (node.editable) put("edit", true)
                if (node.scrollable) put("scroll", true)
            }
            array.put(obj)
        }
        return array.toString()
    }

    suspend fun tap(x: Float, y: Float): Boolean {
        val path = Path().apply { moveTo(x, y) }
        val stroke = GestureDescription.StrokeDescription(path, 0L, 50L)
        val gesture = GestureDescription.Builder().addStroke(stroke).build()
        return dispatchGestureSuspending(gesture)
    }

    suspend fun longPress(x: Float, y: Float, durationMs: Long = 600L): Boolean {
        val path = Path().apply { moveTo(x, y) }
        val stroke = GestureDescription.StrokeDescription(path, 0L, durationMs.coerceIn(400L, 2000L))
        val gesture = GestureDescription.Builder().addStroke(stroke).build()
        return dispatchGestureSuspending(gesture)
    }

    suspend fun swipe(x1: Float, y1: Float, x2: Float, y2: Float, durationMs: Long = 300L): Boolean {
        val path = Path().apply {
            moveTo(x1, y1)
            lineTo(x2, y2)
        }
        val stroke = GestureDescription.StrokeDescription(path, 0L, durationMs.coerceIn(100L, 1500L))
        val gesture = GestureDescription.Builder().addStroke(stroke).build()
        return dispatchGestureSuspending(gesture)
    }

    suspend fun drag(x1: Float, y1: Float, x2: Float, y2: Float, durationMs: Long = 800L): Boolean {
        return swipe(x1, y1, x2, y2, durationMs)
    }

    suspend fun pinch(centerX: Float, centerY: Float, zoomIn: Boolean = true, durationMs: Long = 350L): Boolean {
        val offset = 180f
        val path1 = Path()
        val path2 = Path()

        if (zoomIn) {
            path1.moveTo(centerX - 40f, centerY)
            path1.lineTo(centerX - offset, centerY)
            path2.moveTo(centerX + 40f, centerY)
            path2.lineTo(centerX + offset, centerY)
        } else {
            path1.moveTo(centerX - offset, centerY)
            path1.lineTo(centerX - 40f, centerY)
            path2.moveTo(centerX + offset, centerY)
            path2.lineTo(centerX + offset, centerY)
        }

        val stroke1 = GestureDescription.StrokeDescription(path1, 0L, durationMs)
        val stroke2 = GestureDescription.StrokeDescription(path2, 0L, durationMs)
        val gesture = GestureDescription.Builder().addStroke(stroke1).addStroke(stroke2).build()
        return dispatchGestureSuspending(gesture)
    }

    suspend fun scroll(down: Boolean = true): Boolean {
        val metrics = resources.displayMetrics
        val centerX = metrics.widthPixels / 2f
        val startY = if (down) metrics.heightPixels * 0.7f else metrics.heightPixels * 0.3f
        val endY = if (down) metrics.heightPixels * 0.3f else metrics.heightPixels * 0.7f
        return swipe(centerX, startY, centerX, endY, 300L)
    }

    fun typeText(text: String): Boolean {
        val root = rootInActiveWindow ?: return false
        val focused = root.findFocus(AccessibilityNodeInfo.FOCUS_INPUT)
        val target = focused ?: findFirstEditable(root)
        root.recycle()

        if (target != null) {
            val arguments = Bundle().apply {
                putCharSequence(AccessibilityNodeInfo.ACTION_ARGUMENT_SET_TEXT_CHARSEQUENCE, text)
            }
            val success = target.performAction(AccessibilityNodeInfo.ACTION_SET_TEXT, arguments)
            target.recycle()
            return success
        }
        return false
    }

    private fun findFirstEditable(node: AccessibilityNodeInfo): AccessibilityNodeInfo? {
        if (node.isEditable) return node
        for (i in 0 until node.childCount) {
            val child = node.getChild(i) ?: continue
            val found = findFirstEditable(child)
            if (found != null) return found
            child.recycle()
        }
        return null
    }

    fun pressBack(): Boolean = performGlobalAction(GLOBAL_ACTION_BACK)

    fun pressHome(): Boolean = performGlobalAction(GLOBAL_ACTION_HOME)

    fun openApp(packageName: String): Boolean {
        return try {
            val launchIntent = packageManager.getLaunchIntentForPackage(packageName)
            if (launchIntent != null) {
                launchIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                startActivity(launchIntent)
                true
            } else {
                false
            }
        } catch (_: Exception) {
            false
        }
    }

    private suspend fun dispatchGestureSuspending(gesture: GestureDescription): Boolean =
        suspendCancellableCoroutine { cont ->
            try {
                val dispatched = dispatchGesture(
                    gesture,
                    object : GestureResultCallback() {
                        override fun onCompleted(gestureDescription: GestureDescription?) {
                            if (cont.isActive) cont.resume(true)
                        }

                        override fun onCancelled(gestureDescription: GestureDescription?) {
                            if (cont.isActive) cont.resume(false)
                        }
                    },
                    mainHandler
                )
                if (!dispatched && cont.isActive) {
                    cont.resume(false)
                }
            } catch (_: Exception) {
                if (cont.isActive) {
                    cont.resume(false)
                }
            }
        }
}
"""

FILES["app/src/main/java/com/example/network/GeminiClient.kt"] = """package com.example.network

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
"""

FILES["app/src/main/java/com/example/service/OverlayService.kt"] = """package com.example.service

import android.annotation.SuppressLint
import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Context
import android.content.Intent
import android.graphics.Color
import android.graphics.PixelFormat
import android.graphics.drawable.GradientDrawable
import android.os.Build
import android.os.IBinder
import android.provider.Settings
import android.view.Gravity
import android.view.MotionEvent
import android.view.View
import android.view.WindowManager
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView
import androidx.core.app.NotificationCompat
import com.example.MainActivity
import com.example.R
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

class OverlayService : Service() {

    companion object {
        const val ACTION_START_OVERLAY = "com.example.mira.ACTION_START_OVERLAY"
        const val ACTION_STOP_OVERLAY = "com.example.mira.ACTION_STOP_OVERLAY"
        const val ACTION_UPDATE_STATUS = "com.example.mira.ACTION_UPDATE_STATUS"
        const val ACTION_HIDE_TEMP = "com.example.mira.ACTION_HIDE_TEMP"
        const val ACTION_SHOW_TEMP = "com.example.mira.ACTION_SHOW_TEMP"
        const val ACTION_SHOW_SAFETY_DIALOG = "com.example.mira.ACTION_SHOW_SAFETY_DIALOG"

        const val EXTRA_STATUS_URDU = "extra_status_urdu"
        const val EXTRA_IS_PAUSED = "extra_is_paused"
        const val EXTRA_PERMISSION_PROMPT = "extra_permission_prompt"

        @Volatile
        var isOverlayRunning = false
            private set

        @Volatile
        var onStopClicked: (() -> Unit)? = null

        @Volatile
        var onPauseResumeClicked: (() -> Unit)? = null

        @Volatile
        var onSafetyApproved: ((Boolean) -> Unit)? = null

        fun canDrawOverlays(context: Context): Boolean {
            return Settings.canDrawOverlays(context)
        }
    }

    private var windowManager: WindowManager? = null
    private var bubbleView: View? = null
    private var safetyDialogView: View? = null
    private var bubbleParams: WindowManager.LayoutParams? = null

    private var statusTextView: TextView? = null
    private var pauseResumeButton: Button? = null
    private var isPausedState: Boolean = false

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onCreate() {
        super.onCreate()
        windowManager = getSystemService(Context.WINDOW_SERVICE) as WindowManager
        createNotificationChannel()
        val notification = buildForegroundNotification("MIRA AI فعال ہے")
        startForeground(1001, notification)
        isOverlayRunning = true
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val action = intent?.action ?: return START_STICKY

        when (action) {
            ACTION_START_OVERLAY -> {
                if (bubbleView == null) {
                    createFloatingBubble()
                }
            }
            ACTION_STOP_OVERLAY -> {
                removeFloatingBubble()
                removeSafetyDialog()
                stopForeground(STOP_FOREGROUND_REMOVE)
                stopSelf()
            }
            ACTION_UPDATE_STATUS -> {
                val status = intent.getStringExtra(EXTRA_STATUS_URDU) ?: "MIRA کام کر رہی ہے..."
                isPausedState = intent.getBooleanExtra(EXTRA_IS_PAUSED, false)
                statusTextView?.text = status
                pauseResumeButton?.text = if (isPausedState) "جاری رکھیں" else "وقفہ"
                updateNotification(status)
            }
            ACTION_HIDE_TEMP -> {
                bubbleView?.visibility = View.GONE
                safetyDialogView?.visibility = View.GONE
            }
            ACTION_SHOW_TEMP -> {
                bubbleView?.visibility = View.VISIBLE
            }
            ACTION_SHOW_SAFETY_DIALOG -> {
                val prompt = intent.getStringExtra(EXTRA_PERMISSION_PROMPT) ?: "کیا آپ ایکسپورٹ / محفوظ کرنے کی اجازت دیتے ہیں؟"
                showSafetyPromptDialog(prompt)
            }
        }

        return START_STICKY
    }

    @SuppressLint("ClickableViewAccessibility")
    private fun createFloatingBubble() {
        if (!Settings.canDrawOverlays(this)) return

        val layoutType = WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
        bubbleParams = WindowManager.LayoutParams(
            WindowManager.LayoutParams.WRAP_CONTENT,
            WindowManager.LayoutParams.WRAP_CONTENT,
            layoutType,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or
                    WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.TOP or Gravity.START
            x = 40
            y = 200
        }

        val container = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            setPadding(24, 16, 24, 16)
            background = GradientDrawable().apply {
                setColor(Color.parseColor("#EE0F172A"))
                cornerRadius = 40f
                setStroke(3, Color.parseColor("#06B6D4"))
            }
        }

        statusTextView = TextView(this).apply {
            text = "MIRA کام کر رہی ہے..."
            setTextColor(Color.WHITE)
            textSize = 13f
            maxWidth = 420
            setPadding(0, 0, 16, 0)
        }

        pauseResumeButton = Button(this).apply {
            text = "وقفہ"
            textSize = 11f
            setTextColor(Color.WHITE)
            background = GradientDrawable().apply {
                setColor(Color.parseColor("#334155"))
                cornerRadius = 24f
            }
            setOnClickListener {
                isPausedState = !isPausedState
                text = if (isPausedState) "جاری رکھیں" else "وقفہ"
                onPauseResumeClicked?.invoke()
            }
        }

        val stopButton = Button(this).apply {
            text = "روکیں"
            textSize = 11f
            setTextColor(Color.WHITE)
            background = GradientDrawable().apply {
                setColor(Color.parseColor("#E11D48"))
                cornerRadius = 24f
            }
            setOnClickListener {
                onStopClicked?.invoke()
            }
        }

        container.addView(statusTextView)
        container.addView(pauseResumeButton)
        container.addView(View(this).apply {
            layoutParams = LinearLayout.LayoutParams(12, 1)
        })
        container.addView(stopButton)

        container.setOnTouchListener(object : View.OnTouchListener {
            private var initialX = 0
            private var initialY = 0
            private var initialTouchX = 0f
            private var initialTouchY = 0f
            private var isMoving = false

            override fun onTouch(v: View, event: MotionEvent): Boolean {
                when (event.action) {
                    MotionEvent.ACTION_DOWN -> {
                        initialX = bubbleParams?.x ?: 0
                        initialY = bubbleParams?.y ?: 0
                        initialTouchX = event.rawX
                        initialTouchY = event.rawY
                        isMoving = false
                        return false
                    }
                    MotionEvent.ACTION_MOVE -> {
                        val dx = event.rawX - initialTouchX
                        val dy = event.rawY - initialTouchY
                        if (Math.abs(dx) > 10 || Math.abs(dy) > 10) {
                            isMoving = true
                            bubbleParams?.x = initialX + dx.toInt()
                            bubbleParams?.y = initialY + dy.toInt()
                            windowManager?.updateViewLayout(bubbleView, bubbleParams)
                            return true
                        }
                    }
                    MotionEvent.ACTION_UP -> {
                        return isMoving
                    }
                }
                return false
            }
        })

        bubbleView = container
        try {
            windowManager?.addView(bubbleView, bubbleParams)
        } catch (_: Exception) {}
    }

    private fun showSafetyPromptDialog(prompt: String) {
        removeSafetyDialog()
        val layoutType = WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
        val dialogParams = WindowManager.LayoutParams(
            WindowManager.LayoutParams.MATCH_PARENT,
            WindowManager.LayoutParams.WRAP_CONTENT,
            layoutType,
            WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.CENTER
        }

        val dialog = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER
            setPadding(40, 36, 40, 36)
            background = GradientDrawable().apply {
                setColor(Color.parseColor("#FA0F172A"))
                cornerRadius = 32f
                setStroke(4, Color.parseColor("#F59E0B"))
            }
        }

        val promptView = TextView(this).apply {
            text = prompt
            setTextColor(Color.WHITE)
            textSize = 16f
            gravity = Gravity.CENTER
            setPadding(0, 0, 0, 24)
        }

        val buttonRow = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER
        }

        val approveBtn = Button(this).apply {
            text = "ہاں، آگے بڑھیں"
            setTextColor(Color.WHITE)
            background = GradientDrawable().apply {
                setColor(Color.parseColor("#10B981"))
                cornerRadius = 24f
            }
            setOnClickListener {
                removeSafetyDialog()
                onSafetyApproved?.invoke(true)
            }
        }

        val cancelBtn = Button(this).apply {
            text = "منسوخ کریں"
            setTextColor(Color.WHITE)
            background = GradientDrawable().apply {
                setColor(Color.parseColor("#E11D48"))
                cornerRadius = 24f
            }
            setOnClickListener {
                removeSafetyDialog()
                onSafetyApproved?.invoke(false)
            }
        }

        buttonRow.addView(approveBtn)
        buttonRow.addView(View(this).apply {
            layoutParams = LinearLayout.LayoutParams(24, 1)
        })
        buttonRow.addView(cancelBtn)

        dialog.addView(promptView)
        dialog.addView(buttonRow)

        safetyDialogView = dialog
        try {
            windowManager?.addView(safetyDialogView, dialogParams)
        } catch (_: Exception) {}
    }

    private fun removeFloatingBubble() {
        if (bubbleView != null) {
            try {
                windowManager?.removeView(bubbleView)
            } catch (_: Exception) {}
            bubbleView = null
        }
    }

    private fun removeSafetyDialog() {
        if (safetyDialogView != null) {
            try {
                windowManager?.removeView(safetyDialogView)
            } catch (_: Exception) {}
            safetyDialogView = null
        }
    }

    private fun createNotificationChannel() {
        val channel = NotificationChannel(
            "mira_agent_channel",
            "MIRA AI Agent Service",
            NotificationManager.IMPORTANCE_LOW
        ).apply {
            description = "MIRA video editing autonomous agent loop"
        }
        val nm = getSystemService(NotificationManager::class.java)
        nm.createNotificationChannel(channel)
    }

    private fun buildForegroundNotification(statusText: String): Notification {
        val openIntent = Intent(this, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_SINGLE_TOP
        }
        val pendingIntent = PendingIntent.getActivity(
            this,
            0,
            openIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        return NotificationCompat.Builder(this, "mira_agent_channel")
            .setContentTitle("MIRA AI ایڈیٹنگ جاری ہے")
            .setContentText(statusText)
            .setSmallIcon(R.mipmap.ic_launcher)
            .setOngoing(true)
            .setContentIntent(pendingIntent)
            .build()
    }

    private fun updateNotification(statusText: String) {
        val nm = getSystemService(NotificationManager::class.java)
        nm.notify(1001, buildForegroundNotification(statusText))
    }

    override fun onDestroy() {
        super.onDestroy()
        removeFloatingBubble()
        removeSafetyDialog()
        isOverlayRunning = false
    }
}
"""

FILES["app/src/main/java/com/example/service/AgentRunnerService.kt"] = """package com.example.service

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Intent
import android.os.IBinder
import androidx.core.app.NotificationCompat
import com.example.MainActivity
import com.example.R
import com.example.agent.AgentRunner

class AgentRunnerService : Service() {

    companion object {
        private const val CHANNEL_ID = "mira_runner_channel"
        private const val NOTIFICATION_ID = 2002
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
        startForeground(NOTIFICATION_ID, buildNotification("MIRA AI ایڈیٹنگ بیک گراؤنڈ میں فعال ہے"))
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        return START_STICKY
    }

    private fun createNotificationChannel() {
        val channel = NotificationChannel(
            CHANNEL_ID,
            "MIRA AI Task Runner",
            NotificationManager.IMPORTANCE_LOW
        )
        val nm = getSystemService(NotificationManager::class.java)
        nm.createNotificationChannel(channel)
    }

    private fun buildNotification(text: String): Notification {
        val intent = Intent(this, MainActivity::class.java)
        val pendingIntent = PendingIntent.getActivity(
            this,
            0,
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("MIRA AI ایجنٹ سروس")
            .setContentText(text)
            .setSmallIcon(R.mipmap.ic_launcher)
            .setContentIntent(pendingIntent)
            .build()
    }

    override fun onDestroy() {
        super.onDestroy()
        AgentRunner.stopJob(this)
    }
}
"""

FILES["app/src/main/java/com/example/agent/AgentRunner.kt"] = """package com.example.agent

import android.content.Context
import android.content.Intent
import com.example.R
import com.example.data.SecureStore
import com.example.data.SkillsStore
import com.example.model.ActionResponse
import com.example.model.ActionType
import com.example.model.EditJob
import com.example.model.JobStatus
import com.example.model.ObservationResult
import com.example.model.SkillRecord
import com.example.model.StepLog
import com.example.network.GeminiClient
import com.example.service.MiraAccessibilityService
import com.example.service.OverlayService
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import kotlinx.coroutines.suspendCancellableCoroutine
import kotlin.coroutines.resume

object AgentRunner {

    private val _currentJob = MutableStateFlow<EditJob?>(null)
    val currentJob: StateFlow<EditJob?> = _currentJob.asStateFlow()

    private val _logs = MutableStateFlow<List<StepLog>>(emptyList())
    val logs: StateFlow<List<StepLog>> = _logs.asStateFlow()

    private val _isPaused = MutableStateFlow(false)
    val isPaused: StateFlow<Boolean> = _isPaused.asStateFlow()

    private val _safetyPrompt = MutableStateFlow<String?>(null)
    val safetyPrompt: StateFlow<String?> = _safetyPrompt.asStateFlow()

    private var executionJob: Job? = null
    private var permissionContinuation: (suspend (Boolean) -> Unit)? = null

    fun startJob(context: Context, job: EditJob) {
        stopJob(context)

        _currentJob.value = job.copy(status = JobStatus.RUNNING)
        _logs.value = emptyList()
        _isPaused.value = false
        _safetyPrompt.value = null

        val overlayIntent = Intent(context, OverlayService::class.java).apply {
            action = OverlayService.ACTION_START_OVERLAY
        }
        context.startService(overlayIntent)

        OverlayService.onStopClicked = {
            stopJob(context)
        }
        OverlayService.onPauseResumeClicked = {
            togglePause(context)
        }
        OverlayService.onSafetyApproved = { approved ->
            permissionContinuation?.let { cb ->
                CoroutineScope(Dispatchers.Default).launch {
                    cb(approved)
                }
            }
        }

        executionJob = CoroutineScope(Dispatchers.Default).launch {
            runAgentLoop(context.applicationContext, job)
        }
    }

    fun stopJob(context: Context) {
        executionJob?.cancel()
        executionJob = null
        val job = _currentJob.value
        if (job != null && job.status == JobStatus.RUNNING) {
            val updated = job.copy(status = JobStatus.STOPPED)
            _currentJob.value = updated
            SecureStore(context).saveRecentJob(updated)
        }
        _isPaused.value = false
        _safetyPrompt.value = null

        val overlayIntent = Intent(context, OverlayService::class.java).apply {
            action = OverlayService.ACTION_STOP_OVERLAY
        }
        context.startService(overlayIntent)
    }

    fun togglePause(context: Context) {
        val next = !_isPaused.value
        _isPaused.value = next
        updateOverlay(context, if (next) "MIRA رکی ہوئی ہے (وقفہ)" else "MIRA دوبارہ جاری ہے", next)
    }

    fun respondSafetyPermission(approved: Boolean) {
        _safetyPrompt.value = null
        OverlayService.onSafetyApproved?.invoke(approved)
    }

    fun clearLogs() {
        _logs.value = emptyList()
    }

    private suspend fun runAgentLoop(context: Context, initialJob: EditJob) {
        val secureStore = SecureStore(context)
        val skillsStore = SkillsStore(context)
        val apiKey = secureStore.getApiKey()

        if (apiKey.isBlank()) {
            addLog(1, "API Key موجود نہیں ہے", "API Key missing", "ناکامی", false)
            finishJob(context, initialJob.copy(status = JobStatus.FAILED))
            return
        }

        val systemPrompt = try {
            context.resources.openRawResource(R.raw.system_prompt).bufferedReader().use { it.readText() }
        } catch (_: Exception) {
            "You are MIRA, an autonomous CapCut video editing agent on Android."
        }

        val geminiClient = GeminiClient(systemPrompt)
        val capcutPkg = secureStore.capcutPackage
        val stepDelayMs = secureStore.stepDelayMs
        val maxSteps = secureStore.maxSteps
        val maxRetries = secureStore.maxRetries

        var stepNumber = 0
        var totalApiCalls = 0
        var consecutiveFailures = 0
        var lastActionSummary = ""
        var sameActionCount = 0

        val service = MiraAccessibilityService.instance
        if (service == null) {
            addLog(1, "رسائی سروس (Accessibility) فعال نہیں ہے", "AccessibilityService null", "ناکامی", false)
            finishJob(context, initialJob.copy(status = JobStatus.FAILED))
            return
        }

        if (!service.isAllowedForeground()) {
            updateOverlay(context, "CapCut کھولا جا رہا ہے...")
            service.openApp(capcutPkg)
            delay(3000L)
        }

        while (stepNumber < maxSteps && CoroutineScope(Dispatchers.Default).isActive) {
            while (_isPaused.value) {
                delay(500L)
            }

            stepNumber++

            sendOverlayCommand(context, OverlayService.ACTION_HIDE_TEMP)
            delay(150L)

            val needScreenshot = (stepNumber == 1) || (consecutiveFailures > 0) || (stepNumber % 4 == 0)
            val observation = service.observe(includeScreenshot = needScreenshot)

            sendOverlayCommand(context, OverlayService.ACTION_SHOW_TEMP)

            if (!service.isAllowedForeground()) {
                addLog(
                    stepNumber = stepNumber,
                    thoughtUrdu = "ہم CapCut سے باہر ہیں۔ حفاظت کے لیے عمل روکا گیا۔",
                    screenSummary = "Outside CapCut: ${observation.packageName}",
                    actionName = "SAFETY_HALT",
                    isSuccess = false,
                    apiCalls = totalApiCalls
                )
                updateOverlay(context, "ہم CapCut سے باہر ہیں!")
                delay(2000L)
                service.openApp(capcutPkg)
                delay(2500L)
                continue
            }

            updateOverlay(context, "MIRA سوچ رہی ہے...")

            val (decision, callsUsed) = geminiClient.decideNextAction(
                apiKey = apiKey,
                modelName = secureStore.modelName,
                job = _currentJob.value ?: initialJob,
                currentObservation = observation,
                history = _logs.value,
                sendScreenshot = needScreenshot,
                onWaitingRateLimit = { waitingMsg ->
                    updateOverlay(context, waitingMsg)
                }
            )
            totalApiCalls += callsUsed

            _currentJob.value = _currentJob.value?.copy(
                progress = decision.progressPercent.coerceIn(0, 100),
                apiCallsCount = totalApiCalls
            )

            updateOverlay(context, decision.thoughtUrdu.ifBlank { "MIRA ایکشن لے رہی ہے..." })

            val currentActionKey = "${decision.action}_${decision.x}_${decision.y}_${decision.targetNodeIndex}"
            if (currentActionKey == lastActionSummary) {
                sameActionCount++
                if (sameActionCount >= 3) {
                    addLog(
                        stepNumber = stepNumber,
                        thoughtUrdu = "ایک ہی عمل 3 بار دہرایا گیا ہے۔ آپ کی رائے درکار ہے۔",
                        screenSummary = "Loop detected: $currentActionKey",
                        actionName = "LOOP_DETECTED",
                        isSuccess = false,
                        apiCalls = totalApiCalls
                    )
                    pauseForUser(context, "ایک ہی اسکرین پر بار بار کوشش ناکام رہی۔ کیا آپ ہاتھ سے اگلا مرحلہ مکمل کریں گے؟")
                    sameActionCount = 0
                    continue
                }
            } else {
                sameActionCount = 1
                lastActionSummary = currentActionKey
            }

            val isSensitiveAction = decision.action == ActionType.REQUEST_PERMISSION ||
                    (secureStore.askBeforeExport && decision.expectedResult.contains("export", ignoreCase = true)) ||
                    decision.thoughtUrdu.contains("محفوظ") ||
                    decision.thoughtUrdu.contains("ایکسپورٹ")

            if (isSensitiveAction) {
                _currentJob.value = _currentJob.value?.copy(status = JobStatus.WAITING_PERMISSION)
                val promptText = "MIRA ویڈیو کو ایکسپورٹ یا محفوظ کرنا چاہتی ہے۔ کیا آپ اجازت دیتے ہیں؟"
                _safetyPrompt.value = promptText

                val permissionApproved = requestUserPermissionSuspend(context, promptText)
                _safetyPrompt.value = null

                if (!permissionApproved) {
                    addLog(
                        stepNumber = stepNumber,
                        thoughtUrdu = "صارف نے ایکسپورٹ کی اجازت نہیں دی۔",
                        screenSummary = "User declined permission",
                        actionName = "PERMISSION_DENIED",
                        isSuccess = false,
                        apiCalls = totalApiCalls
                    )
                    _currentJob.value = _currentJob.value?.copy(status = JobStatus.STOPPED)
                    finishJob(context, _currentJob.value ?: initialJob)
                    return
                }
                _currentJob.value = _currentJob.value?.copy(status = JobStatus.RUNNING)
            }

            if (decision.action == ActionType.DONE) {
                addLog(
                    stepNumber = stepNumber,
                    thoughtUrdu = decision.thoughtUrdu.ifBlank { "الحمدللہ! ویڈیو ایڈیٹنگ مکمل ہو گئی۔" },
                    screenSummary = decision.screenSummary,
                    actionName = "DONE",
                    isSuccess = true,
                    apiCalls = totalApiCalls
                )
                finishJob(context, (_currentJob.value ?: initialJob).copy(status = JobStatus.COMPLETED, progress = 100))
                return
            }

            if (decision.action == ActionType.FAIL) {
                addLog(
                    stepNumber = stepNumber,
                    thoughtUrdu = decision.thoughtUrdu.ifBlank { "ایڈیٹنگ مکمل نہیں ہو سکی۔" },
                    screenSummary = decision.screenSummary,
                    actionName = "FAIL",
                    isSuccess = false,
                    apiCalls = totalApiCalls
                )
                finishJob(context, (_currentJob.value ?: initialJob).copy(status = JobStatus.FAILED))
                return
            }

            if (decision.action == ActionType.ASK_USER) {
                pauseForUser(context, decision.thoughtUrdu)
                continue
            }

            val executionSuccess = executeAction(service, decision, observation)

            addLog(
                stepNumber = stepNumber,
                thoughtUrdu = decision.thoughtUrdu,
                screenSummary = decision.screenSummary,
                actionName = "${decision.action} (${decision.expectedResult.take(30)})",
                isSuccess = executionSuccess,
                apiCalls = totalApiCalls
            )

            if (executionSuccess && decision.targetNodeIndex != null && decision.targetNodeIndex in observation.nodes.indices) {
                val node = observation.nodes[decision.targetNodeIndex]
                val label = node.text.ifBlank { node.contentDescription }
                if (label.isNotBlank()) {
                    val capcutVer = try {
                        context.packageManager.getPackageInfo(capcutPkg, 0).versionName ?: "unknown"
                    } catch (_: Exception) { "unknown" }

                    val metrics = context.resources.displayMetrics
                    skillsStore.saveSkill(
                        SkillRecord(
                            capcutVersion = capcutVer,
                            label = label,
                            viewId = node.viewIdResourceName,
                            relativeX = node.bounds.centerX().toFloat() / metrics.widthPixels,
                            relativeY = node.bounds.centerY().toFloat() / metrics.heightPixels
                        )
                    )
                }
            }

            delay(stepDelayMs)

            val postObservation = service.observe(includeScreenshot = false)
            val screenChanged = postObservation.treeJson != observation.treeJson
            if (!screenChanged && decision.action != ActionType.WAIT) {
                consecutiveFailures++
                if (consecutiveFailures >= maxRetries) {
                    pauseForUser(context, "مسلسل $maxRetries کوششوں کے باوجود اسکرین میں تبدیلی نہیں ہوئی۔ آپ کی رہنمائی درکار ہے۔")
                    consecutiveFailures = 0
                }
            } else {
                consecutiveFailures = 0
            }
        }

        finishJob(context, (_currentJob.value ?: initialJob).copy(status = JobStatus.COMPLETED))
    }

    private suspend fun executeAction(
        service: MiraAccessibilityService,
        action: ActionResponse,
        observation: ObservationResult
    ): Boolean {
        return try {
            when (action.action) {
                ActionType.TAP -> {
                    if (action.targetNodeIndex != null && action.targetNodeIndex in observation.nodes.indices) {
                        val node = observation.nodes[action.targetNodeIndex]
                        service.tap(node.bounds.centerX().toFloat(), node.bounds.centerY().toFloat())
                    } else if (action.x != null && action.y != null) {
                        val realX = action.x * observation.scaleFactorX
                        val realY = action.y * observation.scaleFactorY
                        service.tap(realX, realY)
                    } else {
                        false
                    }
                }
                ActionType.LONG_PRESS -> {
                    val realX = (action.x ?: 500f) * observation.scaleFactorX
                    val realY = (action.y ?: 500f) * observation.scaleFactorY
                    service.longPress(realX, realY, action.durationMs ?: 600L)
                }
                ActionType.SWIPE, ActionType.DRAG -> {
                    val x1 = (action.x ?: 300f) * observation.scaleFactorX
                    val y1 = (action.y ?: 500f) * observation.scaleFactorY
                    val x2 = (action.x2 ?: 700f) * observation.scaleFactorX
                    val y2 = (action.y2 ?: 500f) * observation.scaleFactorY
                    service.swipe(x1, y1, x2, y2, action.durationMs ?: 350L)
                }
                ActionType.PINCH -> {
                    val cx = (action.x ?: 500f) * observation.scaleFactorX
                    val cy = (action.y ?: 500f) * observation.scaleFactorY
                    service.pinch(cx, cy, zoomIn = true, durationMs = action.durationMs ?: 350L)
                }
                ActionType.SCROLL -> {
                    val scrollDown = (action.y2 ?: 0f) < (action.y ?: 1f)
                    service.scroll(scrollDown)
                }
                ActionType.TYPE_TEXT -> {
                    service.typeText(action.text ?: "")
                }
                ActionType.BACK -> {
                    service.pressBack()
                }
                ActionType.HOME -> {
                    service.pressHome()
                }
                ActionType.OPEN_APP -> {
                    service.openApp(action.text ?: "com.lemon.lvoverseas")
                }
                ActionType.WAIT -> {
                    delay(action.durationMs ?: 1200L)
                    true
                }
                else -> true
            }
        } catch (_: Exception) {
            false
        }
    }

    private suspend fun requestUserPermissionSuspend(context: Context, prompt: String): Boolean =
        suspendCancellableCoroutine { cont ->
            permissionContinuation = { approved ->
                permissionContinuation = null
                if (cont.isActive) cont.resume(approved)
            }
            val intent = Intent(context, OverlayService::class.java).apply {
                action = OverlayService.ACTION_SHOW_SAFETY_DIALOG
                putExtra(OverlayService.EXTRA_PERMISSION_PROMPT, prompt)
            }
            context.startService(intent)
        }

    private fun pauseForUser(context: Context, urduMessage: String) {
        _isPaused.value = true
        _currentJob.value = _currentJob.value?.copy(status = JobStatus.WAITING_USER)
        updateOverlay(context, urduMessage, isPaused = true)
    }

    private fun updateOverlay(context: Context, statusUrdu: String, isPaused: Boolean = false) {
        val intent = Intent(context, OverlayService::class.java).apply {
            action = OverlayService.ACTION_UPDATE_STATUS
            putExtra(OverlayService.EXTRA_STATUS_URDU, statusUrdu)
            putExtra(OverlayService.EXTRA_IS_PAUSED, isPaused)
        }
        context.startService(intent)
    }

    private fun sendOverlayCommand(context: Context, action: String) {
        val intent = Intent(context, OverlayService::class.java).apply {
            this.action = action
        }
        context.startService(intent)
    }

    private fun addLog(
        stepNumber: Int,
        thoughtUrdu: String,
        screenSummary: String,
        actionName: String,
        isSuccess: Boolean,
        apiCalls: Int = 0
    ) {
        val step = StepLog(
            stepNumber = stepNumber,
            thoughtUrdu = thoughtUrdu,
            screenSummary = screenSummary,
            actionName = actionName,
            resultUrdu = if (isSuccess) "کامیاب" else "دوبارہ کوشش",
            isSuccess = isSuccess,
            apiCalls = apiCalls
        )
        val current = _logs.value.toMutableList()
        current.add(step)
        _logs.value = current
    }

    private fun finishJob(context: Context, job: EditJob) {
        _currentJob.value = job
        SecureStore(context).saveRecentJob(job)
        updateOverlay(
            context,
            when (job.status) {
                JobStatus.COMPLETED -> "ایڈیٹنگ مکمل ہو گئی!"
                JobStatus.FAILED -> "ٹاسک ناکام ہو گیا"
                JobStatus.STOPPED -> "ٹاسک روک دیا گیا"
                else -> "MIRA بند ہے"
            }
        )
    }
}
"""

FILES["app/src/main/java/com/example/ui/theme/Color.kt"] = """package com.example.ui.theme

import androidx.compose.ui.graphics.Color

val MidnightDark = Color(0xFF0F172A)
val SurfaceDark = Color(0xFF1E293B)
val SurfaceElevated = Color(0xFF334155)

val CyanNeon = Color(0xFF06B6D4)
val CyanGlow = Color(0xFF22D3EE)
val MagentaNeon = Color(0xFFEC4899)
val VioletNeon = Color(0xFF8B5CF6)

val EmeraldSuccess = Color(0xFF10B981)
val RoseError = Color(0xFFF43F5E)
val AmberWarning = Color(0xFFF59E0B)

val TextPrimaryDark = Color(0xFFF8FAFC)
val TextSecondaryDark = Color(0xFF94A3B8)
"""

FILES["app/src/main/java/com/example/ui/theme/Type.kt"] = """package com.example.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

val Typography = Typography(
    bodyLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 16.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.5.sp
    )
)
"""

FILES["app/src/main/java/com/example/ui/theme/Theme.kt"] = """package com.example.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val DarkColorScheme = darkColorScheme(
    primary = CyanGlow,
    onPrimary = MidnightDark,
    primaryContainer = SurfaceElevated,
    onPrimaryContainer = CyanGlow,
    secondary = MagentaNeon,
    onSecondary = Color.White,
    secondaryContainer = SurfaceElevated,
    onSecondaryContainer = MagentaNeon,
    tertiary = VioletNeon,
    background = MidnightDark,
    surface = SurfaceDark,
    surfaceVariant = SurfaceElevated,
    onBackground = TextPrimaryDark,
    onSurface = TextPrimaryDark,
    onSurfaceVariant = TextSecondaryDark,
    error = RoseError,
    onError = Color.White
)

@Composable
fun MyApplicationTheme(
    darkTheme: Boolean = true,
    dynamicColor: Boolean = false,
    content: @Composable () -> Unit
) {
    MaterialTheme(
        colorScheme = DarkColorScheme,
        typography = Typography,
        content = content
    )
}
"""

FILES["app/src/main/java/com/example/ui/screens/HomeScreen.kt"] = """package com.example.ui.screens

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
"""

FILES["app/src/main/java/com/example/ui/screens/NewEditScreen.kt"] = """package com.example.ui.screens

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
"""

FILES["app/src/main/java/com/example/ui/screens/SettingsScreen.kt"] = """package com.example.ui.screens

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
"""

FILES["app/src/main/java/com/example/ui/screens/LiveLogScreen.kt"] = """package com.example.ui.screens

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
"""

FILES["app/src/main/java/com/example/ui/screens/OnboardingScreen.kt"] = """package com.example.ui.screens

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
                                text = "1. فون کی Settings > Apps > MIRA AI کھولیں۔\\n" +
                                        "2. اوپر دائیں کونے میں تین نقطوں پر ٹیپ کریں۔\\n" +
                                        "3. 'Allow restricted settings' کو منتخب کریں اور تصدیق کریں۔\\n" +
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
"""

FILES["app/src/main/java/com/example/MainActivity.kt"] = """package com.example

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
"""

FILES["app/src/test/java/com/example/ExampleUnitTest.kt"] = """package com.example

import com.example.model.ActionType
import com.example.ui.screens.normalizeDigits
import org.junit.Assert.assertEquals
import org.junit.Test

class ExampleUnitTest {
    @Test
    fun testUrduDigitsNormalization() {
        val urduInput = "۲.۵, ۵.۰, ۷.۸"
        val normalized = normalizeDigits(urduInput)
        assertEquals("2.5, 5.0, 7.8", normalized)
    }

    @Test
    fun testActionTypeParsing() {
        assertEquals(ActionType.TAP, ActionType.fromString("tap"))
        assertEquals(ActionType.LONG_PRESS, ActionType.fromString("long_press"))
        assertEquals(ActionType.REQUEST_PERMISSION, ActionType.fromString("request_permission"))
        assertEquals(ActionType.WAIT, ActionType.fromString("unknown_action"))
    }
}
"""

FILES["app/src/test/java/com/example/ExampleRobolectricTest.kt"] = """package com.example

import android.content.Context
import androidx.test.core.app.ApplicationProvider
import org.junit.Assert.assertEquals
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [34])
class ExampleRobolectricTest {

  @Test
  fun `read string from context`() {
    val context = ApplicationProvider.getApplicationContext<Context>()
    val appName = context.getString(R.string.app_name)
    assertEquals("MIRA AI", appName)
  }
}
"""

FILES["app/src/androidTest/java/com/example/ExampleInstrumentedTest.kt"] = """package com.example

import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class ExampleInstrumentedTest {
  @Test
  fun useAppContext() {
    val appContext = InstrumentationRegistry.getInstrumentation().targetContext
    assertEquals(BuildConfig.APPLICATION_ID, appContext.packageName)
  }
}
"""

FILES["metadata.json"] = """{
  "name": "MIRA AI",
  "description": "Urdu-speaking autonomous AI video editing agent for CapCut with Accessibility Service, floating overlay, and Gemini reasoning.",
  "requestFramePermissions": [],
  "majorCapabilities": ["MAJOR_CAPABILITY_SERVER_SIDE_GEMINI_API"]
}
"""

FILES["README.md"] = """# MIRA AI - Personal Autonomous Video Editing Agent for CapCut 🎬🤖

**MIRA AI** is an intelligent, free, native Android assistant that operates the **CapCut** app on your Android phone just like a human editor. It looks at the screen using an Accessibility Service, reasons about the next editing action using Google's **Gemini Flash API**, and performs taps, cuts, splits, speed curves (Velocity/Rampage), and transitions autonomously.

The entire user interface and interaction is in **Urdu (RTL)**, while the underlying Kotlin engine is engineered for rock-solid reliability, safety, and privacy.

---

## 🌟 Key Highlights & Architecture

- **100% Free**: Uses Google AI Studio's free Gemini API key. No subscriptions, no ads, no backend server, no Firebase.
- **Android Native**: Built with **Kotlin**, **Jetpack Compose (Material 3)**, and **Coroutines**.
- **Eyes & Hands**: Uses `MiraAccessibilityService` (`minSdk 30`) with `canTakeScreenshot` and `dispatchGesture`.
- **Dual Observation Strategy**: Analyzes the fast Android UI accessibility node tree first; falls back to downscaled 1080p JPEG screenshots when inspecting custom canvas elements like CapCut's timeline.
- **Floating Overlay Bubble**: `SYSTEM_ALERT_WINDOW` floating widget showing current steps in Urdu with an instant **"روکیں" (STOP)** emergency button and pause/resume.
- **Strict Safety Gate**: Requires explicit Urdu approval before saving, exporting, or making changes outside the project.
- **Local Learning Memory**: Caches successful UI coordinates and button identifiers in a local JSON skills store to save API quota.

---

## 🚀 How to Build and Download the APK for Free (GitHub Actions)

You do not need Android Studio installed on your computer. You can build the APK directly on GitHub using the included workflow:

### Step 1: Push or Upload Project to GitHub
1. Create a new GitHub repository (public or private).
2. Push this folder to your repository, or upload the files directly via GitHub's web interface.

### Step 2: Run GitHub Actions Workflow
1. Go to your repository on GitHub.
2. Click on the **Actions** tab.
3. Select **"Build MIRA AI APK"** from the left sidebar.
4. Click **Run workflow** -> Select `main` branch -> Click **Run workflow**.

### Step 3: Download and Install APK
1. When the workflow finishes (typically ~2-3 minutes with green checkmark), click on the completed run.
2. Scroll to the bottom to find **Artifacts**.
3. Download **`MIRA-AI-debug-apk`**.
4. Unzip the downloaded file to get `app-debug.apk` and transfer/open it on your Android phone to install.

---

## 📲 First-Run Setup & Onboarding Wizard (Urdu)

When you first launch **MIRA AI**, complete the 5 simple setup steps:

1. **Gemini API Key**:
   - Go to [Google AI Studio](https://aistudio.google.com/app/apikey) and create a free Gemini API key.
   - Paste it in MIRA AI Settings. It is encrypted in Android Keystore and never sent anywhere except directly to Google's API.
2. **Notifications**: Allow notification access so MIRA can run in the foreground.
3. **Display Over Other Apps (Overlay)**: Enable permission to show the floating control bubble over CapCut.
4. **Accessibility Service**:
   - Turn ON **"MIRA AI"** in Accessibility settings.
   - **Note for Android 13+ Users**: If the switch is greyed out ("Restricted setting"):
     - Go to phone **Settings** > **Apps** > **MIRA AI**.
     - Tap the **3-dots menu** at the top right.
     - Tap **"Allow restricted settings"** and verify with fingerprint/PIN.
     - Return to Accessibility and turn on the switch!
5. **Open CapCut**: Ensure CapCut is installed and has been opened at least once.

---

## ⚠️ Known Limitations

1. **CapCut Version Differences**: CapCut frequently updates its user interface. While MIRA uses adaptive multimodal vision and caches UI nodes, major design overhauls by CapCut may occasionally require Gemini to re-explore button menus.
2. **Custom Canvas Timeline**: CapCut draws its video clips and timeline ruler on a custom OpenGL/Skia canvas without standard text accessibility labels. MIRA seamlessly handles this by capturing screenshot coordinates and mapping them to screen pixels.
3. **Free Gemini Rate Limits**: Google AI Studio's free tier has per-minute request limits. MIRA includes exponential backoff and shows *"MIRA انتظار کر رہی ہے"* if rate-limited, continuing smoothly as soon as the quota resets.

---

## 🧪 10-Second Test Checklist (Run on Your Phone)

Use this quick verification procedure with a 10-second test video:

1. [ ] **Verify Status**: Launch MIRA AI. Ensure the Home card says **"MIRA تیار ہے"** with green indicators.
2. [ ] **Start New Edit**: Tap **"نیا ایڈٹ شروع کریں"**.
3. [ ] **Step 1**: Pick your 10-second video from the Gallery and enter a title.
4. [ ] **Step 2**: Enter cut timing: `2.5, 5.0, 7.5`.
5. [ ] **Step 3**: Select style: **وائلوسیٹی (Velocity)** or **ریمپیج (Rampage)**.
6. [ ] **Step 4**: Enter note: *"Fast cuts with smooth zoom"*.
7. [ ] **Step 5**: Tap **"شروع کریں"**.
8. [ ] **Observe Floating Bubble**: Notice CapCut opens automatically and the floating bubble displays Urdu progress.
9. [ ] **Test Stop Button**: Tap the red **"روکیں"** button at any point to verify immediate cancellation.
10. [ ] **Check Live Logs**: Re-open MIRA AI and switch to the **"لائیو لاگ"** tab to see the exact sequence of actions taken.
"""

def main():
    print("Creating MIRA AI project structure...")
    for path, content in FILES.items():
        dir_name = os.path.dirname(path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        if path == "gradlew":
            st = os.stat(path)
            os.chmod(path, st.st_mode | stat.S_IEXEC)
        print(f"Created: {path}")

    os.makedirs("gradle/wrapper", exist_ok=True)
    print("\nSuccess! Complete MIRA AI project has been generated.")

if __name__ == "__main__":
    main()