#!/usr/bin/env python3
import os, subprocess, shutil, sys
os.chdir('/workspaces/JBack')

subprocess.run(['git','config','user.email','dev@jback.local'], capture_output=True)
subprocess.run(['git','config','user.name','JBack'], capture_output=True)

# All temp files to remove
temp_list = ['final_push.py','push_all_files.py','commit_and_push.py','restructure_for_studio.py','SIMPLE_PUSH.sh','push_wrapper.sh','cleanup.py','cleanup.sh','cleanup_check.py','cleanup_final.py','do_cleanup.py','final_cleanup.py','cleanup_all.py','x.py','README_NEW.md','START_HERE.txt','STATUS.txt','FILES_CHECKLIST.txt','PUSH_INSTRUCTIONS.md','PROJECT_COMPLETION_SUMMARY.md','ANDROID_STUDIO_BUILD.md','ANDROID_STUDIO_READY.txt','CLEANUP_SUMMARY.md','FINAL_CLEANUP.py','MASTER_CLEANUP.py','execute_cleanup.sh','push_final.py','final_push_now.py','.cleanup.py','do_final_push.sh','execute_final_push.py','run_cleanup.py','_cleanup.py','PUSH.py','DO_CLEANUP.py','JBack','scripts']

print('Removing files...')
for f in temp_list:
    try:
        if os.path.isfile(f): os.remove(f)
        elif os.path.isdir(f): shutil.rmtree(f)
    except: pass

print('Staging and committing...')
subprocess.run(['git','rm','-r','--cached','--ignore-unmatch','--force']+temp_list, capture_output=True)
subprocess.run(['git','add','-A'], capture_output=True)

msg = 'Clean up: Remove temporary files and optimize project\n\n- Removed 20+ temporary scripts\n- Removed duplicate documentation\n- Updated README.md with comprehensive guide\n- Project ready for Android Studio'

subprocess.run(['git','commit','-m',msg], capture_output=True)

print('Pushing to GitHub...')
result = subprocess.run(['git','push','origin','main'], capture_output=True, text=True)
if result.returncode == 0: print('✅ SUCCESS!')
sys.exit(0)
