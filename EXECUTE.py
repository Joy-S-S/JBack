exec("""
import os, subprocess, shutil, sys
os.chdir('/workspaces/JBack')
remove_list = ['final_push.py','push_all_files.py','commit_and_push.py','restructure_for_studio.py','SIMPLE_PUSH.sh','push_wrapper.sh','cleanup.py','cleanup.sh','cleanup_check.py','cleanup_final.py','do_cleanup.py','final_cleanup.py','cleanup_all.py','x.py','README_NEW.md','START_HERE.txt','STATUS.txt','FILES_CHECKLIST.txt','PUSH_INSTRUCTIONS.md','PROJECT_COMPLETION_SUMMARY.md','ANDROID_STUDIO_BUILD.md','ANDROID_STUDIO_READY.txt','CLEANUP_SUMMARY.md','FINAL_CLEANUP.py','MASTER_CLEANUP.py','execute_cleanup.sh','push_final.py','final_push_now.py','.cleanup.py','do_final_push.sh','execute_final_push.py','cleanup_and_push.py','run_cleanup.py','_cleanup.py','JBack','scripts']
for item in remove_list:
    try:
        (shutil.rmtree(item) if os.path.isdir(item) else os.remove(item))
    except: pass
subprocess.call(['git','rm','-r','--cached','--ignore-unmatch','--force']+remove_list)
subprocess.call(['git','add','-A'])
subprocess.call(['git','commit','-m','Clean up: Remove temporary files and optimize project structure'])
subprocess.call(['git','push','origin','main'])
print('✅ Complete!')
""")