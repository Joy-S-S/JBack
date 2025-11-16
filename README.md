JBack — Android rooted-app scaffold

This repository is a minimal Android Studio project scaffold for building an app that can detect root and run simple root commands.

What I added
- `settings.gradle` and `build.gradle` (root)
- `app/build.gradle` (module)
- `app/src/main/AndroidManifest.xml`
Active Kotlin sources are under `app/src/main/java/com/jback/rootbackup/` (moved from earlier paths).
- `app/src/main/res/layout/activity_main.xml`
- `.gitignore`

How to use
1. Open this folder in Android Studio (`File → Open` → select `/workspaces/JBack`).
2. Let Android Studio sync Gradle and (if needed) create a Gradle wrapper.
3. Run the app on a rooted device or emulator (emulator with root or a real rooted device). The app will attempt to run `id` with `su`.

Notes & safety
- This scaffold only demonstrates calling `su` for legitimate admin actions. Do not use it to bypass security on devices you don't own.
- The project uses a simple `Runtime.exec(arrayOf("su","-c", cmd))` pattern. For production, use safer patterns and validate inputs.

Next steps you might want to do
- Add more robust root-checking and handle `su` prompts.
- Add a Gradle wrapper (`./gradlew`) if you want CLI builds.
- Add permissions or features your tool requires.
Notes on what I changed for you
- I moved Kotlin source files to the conventional package path: `app/src/main/java/com/jback/rootbackup/` and normalized the package to `com.jback.rootbackup` (lowercase, conventional).
- I added a basic AppCompat `styles.xml` and an empty `app/proguard-rules.pro` referenced by the build.
- I added runtime storage permission guidance in `MainActivity` to request `READ/WRITE_EXTERNAL_STORAGE` on older Android and to open the All Files Access settings for Android 11+ (`MANAGE_EXTERNAL_STORAGE`).
- I added JitPack to `settings.gradle` so the `libsu` dependency can be resolved.

Build notes / next steps
- You need Android SDK (API 34) and Android Studio to build the app. CI or local CLI builds require the Android SDK and Gradle.
- I did not add a full Gradle wrapper in this container because generating the wrapper requires Gradle installed in the environment. You can generate it locally with:
```bash
gradle wrapper
```
or let Android Studio generate the wrapper for you (File → Settings → Gradle).
- After you have the wrapper, build locally with:
```bash
./gradlew assembleDebug
```
- Ensure launcher icons exist (`@mipmap/ic_launcher*`) — Android Studio can generate adaptive icons for you (Right-click `res` → New → Image Asset).

Caveats & follow-ups
- Restoring app data by copying files into `/data/data/<package>` often requires restoring ownership (chown) and SELinux contexts. This scaffold copies files, but for robust restores you should use `tar` to preserve permissions or run `chown`/`chmod`/`restorecon` via root after copying.
I removed legacy placeholder files and moved the sources to `app/src/main/java/com/jback/rootbackup/`.

If you want, I can now:
- Add Gradle wrapper files here (will attempt it, but may fail without Gradle present).
- Improve RootUtils to use `libsu` APIs exclusively and add timeouts/result parsing.
- Add icon assets and more polished theme resources.
- Add unit tests and a simple instrumentation test to verify backup/restore flows on an emulator.