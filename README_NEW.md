# JBack — Android Root Backup/Restore App

A complete Android application scaffold for performing root-level backup and restore of apps and user data on rooted devices.

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/Joy-S-S/JBack.git
cd JBack

# Build the project with Gradle Wrapper
chmod +x ./gradlew
./gradlew assembleDebug --no-daemon
```

## ✨ Features

### Backup Functionality
- ✅ Select specific apps to backup
- ✅ Backup app APK files
- ✅ Backup app private data (`/data/data/<package>`)
- ✅ Backup user folders (DCIM, Documents, Downloads, Pictures, Music, etc.)
- ✅ Backup messaging apps data (Telegram, WhatsApp, Signal, Messenger)
- ✅ Create timestamped ZIP archives

### Restore Functionality
- ✅ List available backups
- ✅ Restore APK files (re-installs apps)
- ✅ Restore app data with correct permissions
- ✅ Fix SELinux contexts after restore
- ✅ Restore user data to original locations

### Root Integration
- ✅ Reliable root detection using libsu
- ✅ Safe root file access via libsu APIs
- ✅ Automatic permission fixing after restore
- ✅ Support for Magisk and traditional su

## 📦 Project Structure

```
JBack/
├── app/
│   ├── src/main/
│   │   ├── java/com/jback/rootbackup/
│   │   │   ├── MainActivity.kt          # Main UI and logic
│   │   │   └── RootUtils.kt            # Root helpers
│   │   ├── res/
│   │   │   ├── layout/activity_main.xml
│   │   │   ├── mipmap-anydpi/          # Adaptive icons
│   │   │   └── values/                 # Theme, colors
│   │   └── AndroidManifest.xml
│   └── build.gradle
├── gradle/
│   └── wrapper/
│       ├── gradle-wrapper.jar          # Downloaded on first build
│       └── gradle-wrapper.properties   # Gradle 8.2.0 config
├── gradlew                             # Unix/macOS build script
├── gradlew.bat                         # Windows build script
├── build.gradle                        # Root build config
└── settings.gradle                     # Plugin and dependency repos

```

## 🏗️ Tech Stack

- **Language**: Kotlin
- **Android SDK**: API 34 (target), API 21 (min)
- **Build System**: Gradle 8.2.0
- **Root Access**: libsu (TopJohnWu)
- **Async**: Kotlin Coroutines
- **UI Framework**: AndroidX AppCompat
- **Layout**: ConstraintLayout

## 📋 Dependencies

```gradle
androidx.core:core-ktx:1.12.0
androidx.appcompat:appcompat:1.6.1
com.google.android.material:material:1.10.0
androidx.constraintlayout:constraintlayout:2.1.4
androidx.lifecycle:lifecycle-viewmodel-ktx:2.7.0
org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3
com.github.topjohnwu.libsu:core:5.0.4
com.github.topjohnwu.libsu:io:5.0.4
```

## 🔨 Building

### Option 1: Gradle Wrapper (Recommended)
```bash
# Debug build
./gradlew assembleDebug --no-daemon

# Release build
./gradlew assembleRelease --no-daemon

# Run on device/emulator
./gradlew installDebug --no-daemon
```

### Option 2: Android Studio
1. File → Open → Select `/workspaces/JBack`
2. Wait for Gradle sync
3. Build → Build APK

### Prerequisites
- Java 8+
- Android SDK with build-tools (API 34)
- 1.5 GB free disk space

## 📱 Usage

1. **Install & Grant Root**: 
   - Transfer APK to rooted device
   - Install and grant root access when prompted

2. **Backup**:
   - Check "Backup App Data" and/or "Backup Folders" switches
   - Select apps from the list
   - Click "Create Backup"
   - Find ZIP in `app/Backups/` directory

3. **Restore**:
   - Click "Restore" button
   - Select a backup file
   - Confirm and wait for completion

## 📁 Backup File Format

```
backup_YYYYMMDD_HHMMSS.zip
├── apps/
│   ├── com.example.app1.apk
│   └── com.example.app2.apk
├── app_data/
│   ├── com.example.app1/
│   │   └── ... (private app data)
│   └── com.example.app2/
├── external_data/
│   └── com.example.app/
├── obb_data/
│   └── com.example.app/
├── user_data/
│   ├── DCIM/
│   ├── Documents/
│   ├── Download/
│   ├── Movies/
│   ├── Music/
│   ├── Pictures/
│   ├── Videos/
│   ├── Telegram/
│   ├── WhatsApp/
│   ├── Signal/
│   └── Messenger/
└── backup_manifest.txt
```

## 🔐 Security & Safety

⚠️ **Important**: This app requires root access. Use responsibly:

- ✅ Backup your own device
- ✅ Restore to devices you own
- ❌ Never use on third-party devices without permission
- ❌ Never use to bypass device security
- ❌ Never extract/modify others' app data

## 🛠️ Build Configuration

| Setting | Value |
|---------|-------|
| Gradle Version | 8.2.0 |
| AGP (Android Gradle Plugin) | 8.2.0 |
| Kotlin | 1.8.20 |
| Target SDK | 34 |
| Min SDK | 21 |
| Java Compatibility | 1.8 |

## 🎯 Permissions

- `WRITE_EXTERNAL_STORAGE` - Write backups
- `READ_EXTERNAL_STORAGE` - Read user folders
- `MANAGE_EXTERNAL_STORAGE` - All files access (Android 11+)
- `INTERNET` - Future cloud backup features

## 🔄 How It Works

### Backup Process
1. List all installed apps using PackageManager
2. For selected apps:
   - Copy APK from app source directory
   - Use libsu to access and zip app private data
3. For folders: Standard file I/O with user permissions
4. Create manifest with backup metadata
5. Compress all to timestamped ZIP

### Restore Process
1. Extract ZIP entries
2. For APKs: Install via `pm install -r`
3. For app data: Use `SuFileOutputStream` to write to `/data/data/`
4. Fix ownership: `chown -R <uid>:<uid> /data/data/<pkg>`
5. Fix permissions: `chmod -R 700 /data/data/<pkg>`
6. Restore SELinux: `restorecon -R /data/data/<pkg>`
7. For user data: Standard file I/O

## 📝 Implementation Details

### Root Access
- Uses **libsu** for safe, non-blocking root shell execution
- Automatic fallback to `Runtime.exec()` if needed
- Async/await with Kotlin Coroutines

### File I/O
- **libsu Streams**: `SuFileInputStream`, `SuFileOutputStream` for `/data/` access
- **Standard I/O**: Regular Java streams for user-accessible paths
- ZIP streaming for efficient memory usage

### UI Architecture
- Single Activity with multiple views
- Async loading of installed apps
- Live progress feedback

## 🚨 Troubleshooting

### "Root access denied"
```bash
# Verify su is available
adb shell which su

# Check Magisk or SuperSU is installed
adb shell ls -la /system/xbin/su
```

### "Permission denied" errors
- Ensure `MANAGE_EXTERNAL_STORAGE` granted (Android 11+)
- Check device is actually rooted
- Try restarting app and granting root again

### Backup fails silently
- Check available storage space
- Verify selected apps are still installed
- Check logcat: `adb logcat | grep jback`

### APK won't restore
- Verify APK file isn't corrupted
- Check device has sufficient space
- Ensure app isn't system app (can't reinstall)

## 🔮 Future Enhancements

- [ ] Backup encryption/password protection
- [ ] Incremental backups
- [ ] Backup scheduling & automation
- [ ] Cloud backup support (Drive, Dropbox, etc.)
- [ ] Selective restore (choose files/folders)
- [ ] Backup comparison tool
- [ ] Database backup utilities
- [ ] Settings backup integration

## 📄 License

This project is provided as-is for educational and personal use.

## 👤 Author

Created as a complete Android root backup/restore scaffold.

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

For issues and questions, open a GitHub issue.

---

**Remember**: With great power (root) comes great responsibility. Use wisely! 🚀
