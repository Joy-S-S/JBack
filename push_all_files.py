#!/usr/bin/env python3
"""
Push ALL JBack project files to GitHub
"""
import subprocess
import os

os.chdir('/workspaces/JBack')

def run_cmd(cmd, desc=""):
    if desc:
        print(f"\n>>> {desc}")
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    print(result.stdout if result.stdout else result.stderr)
    return result.returncode == 0

print("=" * 70)
print("JBACK - PUSH ALL FILES TO GITHUB")
print("=" * 70)

# Configure git
run_cmd('git config user.email "build@jback.example.com"', "Configuring git email")
run_cmd('git config user.name "JBack Builder"', "Configuring git name")

# Add ALL files
print("\n[1/5] Adding all files...")
run_cmd('git add -A', "Adding all files to staging")

# Show what will be committed
print("\n[2/5] Files to be committed:")
run_cmd('git diff --cached --name-status', "Staged files")

# Commit with detailed message
commit_msg = """Complete JBack project - Android root backup/restore app

SOURCE CODE:
  - MainActivity.kt: Full UI with backup/restore logic
  - RootUtils.kt: Root access helpers using libsu

RESOURCES:
  - activity_main.xml: Complete UI layout
  - styles.xml: AppCompat theme
  - colors.xml: Material colors
  - Adaptive launcher icons (mipmap-anydpi)

BUILD CONFIGURATION:
  - build.gradle (root): Buildscript setup
  - settings.gradle: Plugin & dependency management
  - app/build.gradle: Module configuration
  - gradle-wrapper.properties: Gradle 8.2.0

ANDROID MANIFEST:
  - Complete manifest with all permissions
  - Package: com.jback.rootbackup

GRADLE WRAPPER:
  - gradlew: Unix/Linux/macOS script
  - gradlew.bat: Windows script
  - Gradle 8.2.0 configured

DOCUMENTATION:
  - README_NEW.md: Comprehensive guide
  - PROJECT_COMPLETION_SUMMARY.md: Technical details
  - START_HERE.txt: Quick start
  - STATUS.txt: Project status
  - FILES_CHECKLIST.txt: File listing

FEATURES:
  - Backup selected apps (APK + data)
  - Backup user folders (DCIM, Documents, Pictures, etc.)
  - Restore from backup with ownership/SELinux fixing
  - Root detection via libsu
  - Async operations with Coroutines
  - Runtime permission handling"""

print("\n[3/5] Creating commit...")
run_cmd(f'git commit -m "{commit_msg}"', "Committing all files")

# Push to GitHub
print("\n[4/5] Pushing to GitHub...")
result = run_cmd('git push origin main -v', "Pushing to remote")

# Verify
print("\n[5/5] Verification:")
run_cmd('git log -1 --oneline', "Latest commit")
run_cmd('git ls-files | wc -l', "Total files in repo")

print("\n" + "=" * 70)
print("✓ ALL FILES PUSHED TO GITHUB!")
print("=" * 70)
print("\nVerify at: https://github.com/Joy-S-S/JBack")
print("\nFiles now available for cloning:")
print("  git clone https://github.com/Joy-S-S/JBack.git")
print("  cd JBack")
print("  chmod +x ./gradlew")
print("  ./gradlew assembleDebug --no-daemon")
