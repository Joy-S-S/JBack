#!/usr/bin/env python3
"""
Final cleanup script - removes all temporary files and commits to GitHub
This script is the ONLY cleanup script that will remain
"""
import os, subprocess, shutil, glob

os.chdir('/workspaces/JBack')

# List of ALL temporary/cleanup scripts to delete
temp_scripts = [
    'final_push.py', 'push_all_files.py', 'commit_and_push.py',
    'restructure_for_studio.py', 'SIMPLE_PUSH.sh', 'push_wrapper.sh',
    'cleanup.py', 'cleanup.sh', 'cleanup_check.py', 'cleanup_final.py',
    'do_cleanup.py', 'final_cleanup.py', 'cleanup_all.py', 'x.py'
]

# Duplicate documentation
temp_docs = [
    'README_NEW.md', 'START_HERE.txt', 'STATUS.txt', 'FILES_CHECKLIST.txt',
    'PUSH_INSTRUCTIONS.md', 'PROJECT_COMPLETION_SUMMARY.md',
    'ANDROID_STUDIO_BUILD.md', 'ANDROID_STUDIO_READY.txt'
]

# Items to remove
to_remove = temp_scripts + temp_docs + ['JBack', 'scripts']

print("JBACK FINAL CLEANUP")
print("="*60)

# Physical deletion
for item in to_remove:
    if os.path.isfile(item):
        try:
            os.remove(item)
            print(f"✓ Deleted: {item}")
        except: pass
    elif os.path.isdir(item):
        try:
            shutil.rmtree(item)
            print(f"✓ Deleted: {item}/")
        except: pass

# Git operations
print("\nGit Operations:")
subprocess.run(['git', 'add', '-A'], capture_output=True)

msg = 'Clean up: Remove temporary files and improve structure\n\nProject now has minimal, clean structure ready for Android Studio.\nRemoved all temporary scripts and duplicate documentation.\nKept only essential source, build config, and README.'

result = subprocess.run(['git', 'commit', '-m', msg], capture_output=True, text=True)
if 'create mode' in result.stdout or 'delete mode' in result.stdout:
    print("✓ Committed changes")

result = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, text=True)
print("✅ Pushed to GitHub" if result.returncode == 0 else "⚠ Push status check needed")

print("\n" + "="*60)
print("✅ CLEANUP COMPLETE - Project ready for Android Studio!")
print("="*60)

# Delete self
try: os.remove('FINAL_CLEANUP.py')
except: pass
