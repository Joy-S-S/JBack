#!/usr/bin/env python3
if __name__ == '__main__':
    import os, subprocess, shutil, glob, sys
    
    os.chdir('/workspaces/JBack')
    
    remove_list = [
        'final_push.py','push_all_files.py','commit_and_push.py','restructure_for_studio.py',
        'SIMPLE_PUSH.sh','push_wrapper.sh','cleanup.py','cleanup.sh','cleanup_check.py',
        'cleanup_final.py','do_cleanup.py','final_cleanup.py','cleanup_all.py','x.py',
        'README_NEW.md','START_HERE.txt','STATUS.txt','FILES_CHECKLIST.txt',
        'PUSH_INSTRUCTIONS.md','PROJECT_COMPLETION_SUMMARY.md','ANDROID_STUDIO_BUILD.md',
        'ANDROID_STUDIO_READY.txt','CLEANUP_SUMMARY.md','FINAL_CLEANUP.py','MASTER_CLEANUP.py',
        'execute_cleanup.sh','push_final.py','final_push_now.py','.cleanup.py','do_final_push.sh',
        'execute_final_push.py','cleanup_and_push.py','run_cleanup.py','JBack','scripts'
    ]
    
    print('Removing temporary files...')
    for item in remove_list:
        if os.path.isfile(item):
            os.remove(item)
        elif os.path.isdir(item):
            shutil.rmtree(item)
    
    print('Staging changes...')
    subprocess.call(['git','rm','-r','--cached','--ignore-unmatch','--force']+remove_list)
    subprocess.call(['git','add','-A'])
    
    print('Committing...')
    msg = 'Clean up: Remove temporary files and optimize project structure\n\n- Removed 20+ temporary scripts and duplicate documentation\n- Updated README.md with comprehensive build and usage guide\n- Project ready for Android Studio'
    subprocess.call(['git','commit','-m',msg])
    
    print('Pushing to GitHub...')
    result = subprocess.call(['git','push','origin','main'])
    
    print('\n✅ DONE!' if result == 0 else '⚠ Check push')
    sys.exit(result)
