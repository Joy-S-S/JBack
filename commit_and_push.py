#!/usr/bin/env python3
"""
Commit and push wrapper files to GitHub
"""
import subprocess
import os
import sys

# Work from the correct directory
os.chdir('/workspaces/JBack')

def run_cmd(cmd, desc):
    """Run a command and handle errors"""
    print(f"\n[*] {desc}")
    print(f"    Command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, cwd='/workspaces/JBack')
    if result.stdout:
        print(f"    Output: {result.stdout[:200]}")
    if result.returncode != 0:
        if result.stderr and "nothing to commit" not in result.stderr.lower():
            print(f"    Error: {result.stderr[:200]}")
            return False
    return True

# Set git configuration
run_cmd(['git', 'config', 'user.email', 'build@jback.local'], 'Configuring git email')
run_cmd(['git', 'config', 'user.name', 'JBack Builder'], 'Configuring git name')

# Check git status
run_cmd(['git', 'status'], 'Current git status')

# Add the wrapper files explicitly
print("\n[*] Adding wrapper files...")
files_to_add = [
    'gradlew',
    'gradlew.bat', 
    'gradle/wrapper/gradle-wrapper.properties'
]
for f in files_to_add:
    full_path = os.path.join('/workspaces/JBack', f)
    if os.path.exists(full_path):
        print(f"    ✓ {f} exists")
        run_cmd(['git', 'add', f], f'Adding {f}')
    else:
        print(f"    ✗ {f} NOT FOUND")

# Check what's staged
run_cmd(['git', 'diff', '--cached', '--name-only'], 'Staged files')

# Commit
commit_msg = '''Add Gradle wrapper files (gradlew, gradlew.bat)

- Enable CLI builds without requiring Gradle pre-installation
- Wrapper automatically downloads Gradle 8.2.0 on first run
- Includes both Unix (gradlew) and Windows (gradlew.bat) scripts
- Configured for gradle-wrapper.properties with Gradle 8.2.0'''

result = subprocess.run(
    ['git', 'commit', '-m', commit_msg],
    capture_output=True,
    text=True,
    cwd='/workspaces/JBack'
)
print(f"\n[*] Committing changes...")
print(result.stdout if result.stdout else result.stderr)

# Push to remote
result = subprocess.run(
    ['git', 'push', 'origin', 'main'],
    capture_output=True,
    text=True,
    cwd='/workspaces/JBack'
)
print(f"\n[*] Pushing to GitHub...")
print(result.stdout if result.stdout else result.stderr)

if result.returncode == 0:
    print("\n✓ Successfully pushed wrapper files to GitHub!")
else:
    print(f"\n✗ Push failed with exit code {result.returncode}")

# Verify
run_cmd(['git', 'log', '-1', '--oneline'], 'Latest commit')
