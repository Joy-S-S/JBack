# JBack — Android Root Backup/Restore App

A complete Android application for backing up and restoring apps and user data on rooted devices. Built with Kotlin, AndroidX, and **libsu** for safe root access.

## Features

✅ **Backup & Restore**
- Select and backup specific apps
- Backup user data (DCIM, Documents, Pictures, Downloads, Music, Videos)
- Create ZIP archives with metadata
- Restore to exact previous state

✅ **Root Access**
- Uses **libsu** (TopJohnWu) for safe root command execution
- Automatic root detection
- Proper ownership and SELinux context restoration after restore

✅ **User Interface**
- Modern Material Design UI (AppCompat theme)
- ListView with multi-select for app picking
- Real-time status updates
- Async operations with Coroutines (no UI freezing)

✅ **Permissions & Safety**
- Handles runtime permissions (Android 6.0+)
- Requests MANAGE_EXTERNAL_STORAGE for Android 11+
- Graceful degradation if root not available

## Tech Stack

| Component | Version | Purpose |
|-----------|---------|---------|
| Gradle | 8.2.0 | Build system |
| Android Gradle Plugin | 8.2.0 | Android build support |
| Kotlin | 1.8.20 | Language |
| Target SDK | 34 | Android 14 |
| Min SDK | 21 | Android 5.0+ support |
| libsu | 5.0.4 | Root access (JitPack) |
| Kotlin Coroutines | 1.7.3 | Async operations |
| AndroidX | 1.6.1+ | Modern Android libraries |

## Project Structure

```
JBack/
├── app/
│   ├── src/main/
│   │   ├── AndroidManifest.xml              # App configuration & permissions
│   │   ├── java/com/jback/rootbackup/
│   │   │   ├── MainActivity.kt              # Main UI & backup/restore logic (1400+ lines)
│   │   │   └── RootUtils.kt                 # Root access helpers
│   │   └── res/
│   │       ├── layout/activity_main.xml     # UI layout
│   │       ├── values/styles.xml            # Material theme
│   │       ├── values/colors.xml            # Color definitions
│   │       └── mipmap-*/*.xml               # App icons (adaptive)
│   ├── build.gradle                         # Module build config
│   └── proguard-rules.pro                   # ProGuard obfuscation rules
├── build.gradle                             # Root build config
├── settings.gradle                          # Plugin management
├── gradle/wrapper/                          # Gradle wrapper files
├── gradlew & gradlew.bat                    # Build scripts (Unix/Windows)
└── README.md                                # This file
```

## Getting Started

### Prerequisites

- **Android Studio** (latest)
- **Android SDK** API 34
- **JDK 8+**
- **Rooted Android device or emulator** with root access

### Build & Run

#### Option 1: Android Studio (Recommended)

1. **Open Project**
   ```
   File → Open → Select /path/to/JBack
   ```

2. **Wait for Gradle Sync**
   - Initial sync downloads dependencies (5-10 minutes first time)
   - gradle-wrapper.jar auto-downloads during sync

3. **Build APK**
   ```
   Build → Build Bundle(s)/APK(s) → Build APK(s)
   ```

4. **Run on Device**
   ```
   Click green Run (▶) → Select device
   ```

#### Option 2: CLI (Gradle Wrapper)

```bash
# Build debug APK
./gradlew assembleDebug

# Install on connected device
adb install app/build/outputs/apk/debug/app-debug.apk

# Run app
adb shell am start -n com.jback.rootbackup/.MainActivity
```

## Usage

### Creating a Backup

1. Grant storage permissions when prompted
2. Toggle app checkboxes to select apps to backup
3. Toggle data folder checkboxes for user data backup
4. Click **"Backup Selected"**
5. Wait for completion (status shows progress)
6. APK created at `/sdcard/JBackup/backup_TIMESTAMP.zip`

### Restoring from Backup

1. Click **"Restore from Backup"**
2. Select backup ZIP file
3. Click **"Restore"**
4. App restores with proper ownership and SELinux contexts

### Backup Contents

Each backup ZIP contains:
```
backup/
├── apps/                    # APK files
├── app_data/               # /data/data/* for each app
├── external_data/          # DCIM, Documents, Pictures, etc.
├── obb_data/               # OBB expansion files
├── user_data/              # User folders
└── manifest.json           # Backup metadata
```

## Code Highlights

### Backup Implementation (Simplified)

```kotlin
// Coroutine-based backup with root access
CoroutineScope(Dispatchers.Main).launch {
    withContext(Dispatchers.IO) {
        val shell = Shell.getShell()
        
        // Backup app APK
        for (app in selectedApps) {
            SuFile(app.sourceDir).newInputStream().use { input ->
                zipOut.putNextEntry(ZipEntry("apps/${app.packageName}.apk"))
                input.copyTo(zipOut)
            }
        }
        
        // Backup app data with proper permissions
        Shell.cmd(
            "tar czf /sdcard/appdata.tar.gz /data/data/*",
            "chmod 777 /sdcard/appdata.tar.gz"
        ).exec()
    }
}
```

### Root Access Pattern

```kotlin
// Safe root command execution with libsu
if (Shell.isAppGrantedRoot()) {
    val result = Shell.cmd("ls /data/data/").exec()
    if (result.isSuccess) {
        Log.d("Root", result.out)
    }
}
```

## Permissions Required

```xml
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.MANAGE_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.INTERNET" />
```

## Device Requirements

- **Android 5.0+** (API 21)
- **Rooted device** (Magisk, SuperSU, or equivalent)
- **50+ MB free storage**
- Storage permissions granted at runtime

## Troubleshooting

### Gradle Sync Issues

```bash
# Clear Gradle cache
rm -rf ~/.gradle

# Resync in Android Studio
File → Sync Project with Gradle Files
```

### gradle-wrapper.jar Missing

Android Studio automatically downloads during first sync. If manual download needed:

```bash
cd gradle/wrapper
wget https://repo.gradle.org/gradle/distributions/gradle-8.2.0-all.zip
# Extract gradle-8.2.0/lib/gradle-8.2.0-all.jar to gradle-wrapper.jar
```

### Build Fails

```bash
# Clean build
./gradlew clean assembleDebug

# Or in Android Studio
Build → Clean Project → Rebuild Project
```

### App Won't Detect Root

1. Device must be rooted (Magisk/SuperSU)
2. Grant root permission when app prompts
3. Check root with: `adb shell su -c id`

### No Storage Access

1. Grant "Files & Media" permission at runtime
2. For Android 11+, request "All Files Access" (will direct to settings)
3. Manually grant in Settings → Apps → JBack → Permissions

## Architecture & Design

- **Activity-based UI**: Single MainActivity with Coroutines for async ops
- **libsu Integration**: Safe root command execution via Shell API
- **Kotlin Coroutines**: Non-blocking I/O and UI updates
- **Material Design**: Modern AppCompat theme with MD colors
- **ZIP-based Backup**: Easy to extract and inspect backup contents
- **Metadata Storage**: manifest.json preserves app info and restore context

## Performance Considerations

- Backups run on `Dispatchers.IO` to avoid freezing UI
- Large app backups (100+ apps) may take 5-15 minutes
- Restore operations use tar for efficiency
- ZIP compression reduces backup size by ~30-50%

## Security Notes

⚠️ **This app requires root access to function.** Use only on devices you own and control.

- Backups are created in `/sdcard/JBackup/` (unencrypted by default)
- Consider encrypting backups for sensitive data
- SELinux contexts are restored to maintain security boundaries
- Ownership is restored to original app UIDs post-restore

## Future Enhancements

- [ ] Backup encryption
- [ ] Cloud backup support
- [ ] Automatic scheduling
- [ ] Backup differential/incremental
- [ ] APK downgrade protection
- [ ] Settings backup integration
- [ ] Restore to alternative location

## License

This project is provided as-is for educational and personal backup purposes.

## Support

For issues, feature requests, or questions:
- Check GitHub Issues: https://github.com/Joy-S-S/JBack/issues
- Review code comments in MainActivity.kt for detailed implementation notes

---

**Happy backing up! 🚀**
- Improve RootUtils to use `libsu` APIs exclusively and add timeouts/result parsing.
- Add icon assets and more polished theme resources.
- Add unit tests and a simple instrumentation test to verify backup/restore flows on an emulator.