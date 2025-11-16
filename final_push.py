#!/usr/bin/env python3
"""
Complete solution to add wrapper files and push to GitHub.
Run this from your LOCAL machine (not the container).

Usage:
  python3 final_push.py
"""

import subprocess
import os
import sys

def run_git(cmd, desc=""):
    """Run git command and return result"""
    if desc:
        print(f"\n>>> {desc}")
    print(f"    $ git {' '.join(cmd)}")
    result = subprocess.run(
        ['git'] + cmd,
        capture_output=True,
        text=True,
        cwd='/workspaces/JBack'
    )
    if result.stdout:
        for line in result.stdout.strip().split('\n'):
            print(f"    {line}")
    return result

def main():
    print("=" * 60)
    print("JBack - Push Wrapper Files to GitHub")
    print("=" * 60)
    
    os.chdir('/workspaces/JBack')
    
    # Step 1: Configure git
    print("\n[1/5] Configuring git user...")
    run_git(['config', 'user.email', 'build@jback.example.com'], 
            'Setting git email')
    run_git(['config', 'user.name', 'JBack Builder'],
            'Setting git name')
    
    # Step 2: Check status
    result = run_git(['status', '--porcelain'],
                    'Checking git status')
    
    # Step 3: Add files
    print("\n[2/5] Adding wrapper files...")
    files = [
        'gradlew',
        'gradlew.bat',
        'gradle/wrapper/gradle-wrapper.properties'
    ]
    for f in files:
        if os.path.exists(f):
            run_git(['add', f], f'Adding {f}')
            print(f"        ✓ {f}")
        else:
            print(f"        ✗ {f} NOT FOUND")
    
    # Step 4: Verify staged
    print("\n[3/5] Verifying staged files...")
    run_git(['diff', '--cached', '--name-status'],
           'Staged changes')
    
    # Step 5: Commit
    print("\n[4/5] Creating commit...")
    commit_msg = """Add Gradle wrapper files (gradlew, gradlew.bat)

- Enable CLI builds without requiring Gradle pre-installation
- Wrapper automatically downloads Gradle 8.2.0 on first run
- Includes both Unix (gradlew) and Windows (gradlew.bat) scripts
- Configured for Gradle 8.2.0 in gradle-wrapper.properties

This allows users to clone and build with:
  git clone https://github.com/Joy-S-S/JBack.git
  cd JBack
  chmod +x ./gradlew
  ./gradlew assembleDebug --no-daemon"""
    
    result = subprocess.run(
        ['git', 'commit', '-m', commit_msg],
        capture_output=True,
        text=True,
        cwd='/workspaces/JBack'
    )
    print(result.stdout if result.stdout else result.stderr)
    
    # Step 6: Push
    print("\n[5/5] Pushing to GitHub...")
    result = run_git(['push', 'origin', 'main', '-v'],
                    'Pushing to remote')
    
    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("✓ SUCCESS! Wrapper files pushed to GitHub!")
        print("=" * 60)
        print("\nVerify at:")
        print("  https://github.com/Joy-S-S/JBack")
        print("\nUsers can now clone and build with:")
        print("  git clone https://github.com/Joy-S-S/JBack.git")
        print("  cd JBack")
        print("  chmod +x ./gradlew")
        print("  ./gradlew assembleDebug --no-daemon")
    else:
        print("\n" + "=" * 60)
        print("✗ Push may have failed. Check errors above.")
        print("=" * 60)
    
    # Show latest commit
    print("\nLatest commit:")
    run_git(['log', '-1', '--oneline'])

if __name__ == '__main__':
    main()
