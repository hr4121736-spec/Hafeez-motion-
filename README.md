# MIRA AI - Personal Autonomous Video Editing Agent for CapCut 🎬🤖

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
