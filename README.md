# MIRA AI - Personal Autonomous Video Editing Agent for CapCut 🎬🤖

**MIRA AI** is an intelligent, free, native Android assistant that operates the **CapCut** app on your Android phone just like a human editor. It looks at the screen using an Accessibility Service, reasons about the next editing action using **OpenRouter** (defaulting to free models like `google/gemma-3-27b-it:free`), and performs taps, cuts, splits, speed curves (Velocity/Rampage), and transitions autonomously.

The entire user interface and interaction is in **Urdu (RTL)**, while the underlying Kotlin engine is engineered for rock-solid reliability, safety, and privacy.

---

## 🌟 Key Highlights & Architecture

- **Powered by OpenRouter**: Connects to `https://openrouter.ai/api/v1/chat/completions` supporting top free & premium models (default: `google/gemma-3-27b-it:free`).
- **Android Native**: Built with **Kotlin**, **Jetpack Compose (Material 3)**, and **Coroutines**.
- **Eyes & Hands**: Uses `MiraAccessibilityService` (`minSdk 30`) with `canTakeScreenshot` and `dispatchGesture`.
- **Dual Observation Strategy**: Analyzes the fast Android UI accessibility node tree first; falls back to downscaled 1080p JPEG screenshots when inspecting custom canvas elements like CapCut's timeline.
- **Robust JSON Action Protocol**: Does not rely on rigid JSON schemas that break on free models; cleans markdown fences, extracts outermost `{...}`, and automatically retries with strict reminders.
- **Detailed Error Logging**: For any non-200 response, logs both the HTTP status code and the first 300 characters of the response body into the Live Log. Includes exponential backoff for 429 rate limits and 5xx server issues.
- **Floating Overlay Bubble**: `SYSTEM_ALERT_WINDOW` floating widget showing current steps in Urdu with an instant **"روکیں" (STOP)** emergency button and pause/resume.
- **Strict Safety Gate**: Requires explicit Urdu approval before saving, exporting, or making changes outside the project.
- **Local Learning Memory**: Caches successful UI coordinates and button identifiers in a local JSON skills store to save API quota.

---

## 🔒 Privacy Notice (رازداری کا نوٹس)

> **اردو:** ویڈیو ایڈیٹنگ کے دوران اسکرین شاٹس اور UI معلومات صرف OpenRouter اور آپ کے منتخب کردہ AI ماڈل پرووائیڈر کو محفوظ طریقے سے بھیجی جاتی ہیں۔ آپ کی OpenRouter API کی آپ کے فون کے محفوظ Android Keystore میں محفوظ رہتی ہے اور کسی دیگر سرور پر شیئر نہیں کی جاتی۔

- **API Key Storage**: Stored locally in `EncryptedSharedPreferences` backed by the **Android Keystore (AES-256 GCM)**. Never logged, never transmitted anywhere except directly to OpenRouter.
- **Data Transmission**: Screenshots and UI trees are sent exclusively to OpenRouter's endpoint with HTTPS encryption.

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

1. **OpenRouter API Key**:
   - Go to [openrouter.ai/keys](https://openrouter.ai/keys) and create an API key (`sk-or-v1-...`).
   - Paste it in MIRA AI Settings. You can tap **"API کی ٹیسٹ کریں"** to verify connection via `GET https://openrouter.ai/api/v1/auth/key`.
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

## 🤖 Recommended OpenRouter Models

In Settings, you can configure any model on OpenRouter:
- `google/gemma-3-27b-it:free` (Default: fast, free, excellent reasoning)
- `meta-llama/llama-3.3-70b-instruct:free` (High reasoning capacity)
- `deepseek/deepseek-r1:free` (Deep reasoning)
- Any paid vision-capable model (e.g., `google/gemini-2.0-flash-001`, `anthropic/claude-3.5-sonnet`)

---

## 🧪 10-Second Test Checklist (Run on Your Phone)

Use this quick verification procedure with a 10-second test video:

1. [ ] **Verify Status**: Launch MIRA AI. Ensure the Home card says **"MIRA تیار ہے"** with green indicators.
2. [ ] **Test API Key**: Go to Settings, enter your key, tap **"API کی ٹیسٹ کریں"**, confirm green success.
3. [ ] **Start New Edit**: Tap **"نیا ایڈٹ شروع کریں"**.
4. [ ] **Step 1**: Pick your 10-second video from the Gallery and enter a title.
5. [ ] **Step 2**: Enter cut timing: `2.5, 5.0, 7.5`.
6. [ ] **Step 3**: Select style: **وائلوسیٹی (Velocity)** or **ریمپیج (Rampage)**.
7. [ ] **Step 4**: Enter note: *"Fast cuts with smooth zoom"*.
8. [ ] **Step 5**: Tap **"شروع کریں"**.
9. [ ] **Observe Floating Bubble**: Notice CapCut opens automatically and the floating bubble displays Urdu progress.
10. [ ] **Test Stop Button**: Tap the red **"روکیں"** button at any point to verify immediate cancellation.
11. [ ] **Check Live Logs**: Re-open MIRA AI and switch to the **"لائیو لاگ"** tab to see every action and API response snippet.
