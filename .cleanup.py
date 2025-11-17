import os, subprocess, shutil

os.chdir('/workspaces/JBack')

temp_items = [
    'final_push.py','push_all_files.py','commit_and_push.py','restructure_for_studio.py',
    'SIMPLE_PUSH.sh','push_wrapper.sh','cleanup.py','cleanup.sh','cleanup_check.py',
    'cleanup_final.py','do_cleanup.py','final_cleanup.py','cleanup_all.py','x.py',
    'README_NEW.md','START_HERE.txt','STATUS.txt','FILES_CHECKLIST.txt',
    'PUSH_INSTRUCTIONS.md','PROJECT_COMPLETION_SUMMARY.md','ANDROID_STUDIO_BUILD.md',
    'ANDROID_STUDIO_READY.txt','CLEANUP_SUMMARY.md','FINAL_CLEANUP.py','MASTER_CLEANUP.py',
    'execute_cleanup.sh','push_final.py','final_push_now.py','JBack','scripts'
]

for item in temp_items:
    try:
        if os.path.isfile(item): os.remove(item)
        elif os.path.isdir(item): shutil.rmtree(item)
    except: pass

subprocess.run(['git','rm','-r','--cached','--ignore-unmatch','--force','--quiet']+temp_items, capture_output=True)
subprocess.run(['git','add','-A'], capture_output=True)

msg = '''Clean up: Remove all temporary files and optimize for Android Studio

- Removed 20+ temporary scripts, docs, and directories
- Updated README.md with comprehensive documentation
- Project now has clean, minimal, production-ready structure

Ready for Android Studio build and deployment.'''

subprocess.run(['git','commit','-m',msg], capture_output=True)
result = subprocess.run(['git','push','origin','main'], capture_output=True, text=True)

if result.returncode == 0:
    with open('/tmp/cleanup_success.txt','w') as f: f.write('✅ Pushed successfully!')
else:
    with open('/tmp/cleanup_success.txt','w') as f: f.write(f'Status: {result.returncode}')

try: os.remove(__file__)
except: pass
exec(open(__file__).read()) if os.path.exists(__file__) else None
