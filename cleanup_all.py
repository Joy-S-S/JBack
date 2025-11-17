#!/usr/bin/env python3
import os, subprocess, shutil
os.chdir('/workspaces/JBack')

files_to_delete = ['final_push.py','push_all_files.py','commit_and_push.py','restructure_for_studio.py','SIMPLE_PUSH.sh','push_wrapper.sh','cleanup.py','cleanup.sh','cleanup_check.py','cleanup_final.py','do_cleanup.py','final_cleanup.py','README_NEW.md','START_HERE.txt','STATUS.txt','FILES_CHECKLIST.txt','PUSH_INSTRUCTIONS.md','PROJECT_COMPLETION_SUMMARY.md','ANDROID_STUDIO_BUILD.md','ANDROID_STUDIO_READY.txt','x.py']

dirs_to_delete = ['JBack','scripts']

print("Removing files...")
for f in files_to_delete:
    if os.path.isfile(f):
        os.remove(f)

print("Removing directories...")
for d in dirs_to_delete:
    if os.path.isdir(d):
        shutil.rmtree(d)

print("Staging with git...")
subprocess.run(['git','add','-A'],capture_output=True)

print("Committing...")
subprocess.run(['git','commit','-m','Clean up: Remove temporary files and improve structure - Project ready for Android Studio'],capture_output=True)

print("Pushing...")
result = subprocess.run(['git','push','origin','main'],capture_output=True,text=True)
print('\n✅ COMPLETE - All changes pushed to GitHub' if result.returncode==0 else f'✓ Committed locally')

try: os.remove('cleanup_all.py')
except: pass
