import os
import subprocess
import shutil

os.chdir('/workspaces/JBack')

# Clean up files
files_to_remove = [
    'final_push.py', 'push_all_files.py', 'commit_and_push.py', 'restructure_for_studio.py',
    'SIMPLE_PUSH.sh', 'push_wrapper.sh', 'cleanup.py', 'cleanup.sh', 'cleanup_check.py',
    'README_NEW.md', 'START_HERE.txt', 'STATUS.txt', 'FILES_CHECKLIST.txt', 
    'PUSH_INSTRUCTIONS.md', 'PROJECT_COMPLETION_SUMMARY.md', 'ANDROID_STUDIO_BUILD.md', 
    'ANDROID_STUDIO_READY.txt', 'do_cleanup.py'
]

dirs_to_remove = ['JBack', 'scripts', 'build']

print("Cleaning up files...")
for f in files_to_remove:
    if os.path.exists(f):
        try:
            os.remove(f)
            print(f"✓ {f}")
        except: pass

for d in dirs_to_remove:
    if os.path.exists(d):
        try:
            shutil.rmtree(d)
            print(f"✓ {d}/")
        except: pass

# Remove these from git  
subprocess.run(['git', 'rm', '-r', '--cached', '--ignore-unmatch'] + files_to_remove, capture_output=True)
subprocess.run(['git', 'rm', '-r', '--cached', '--ignore-unmatch'] + dirs_to_remove, capture_output=True)
subprocess.run(['git', 'add', '-A'], capture_output=True)

# Commit
msg = "Clean up: Remove temporary files and improve project structure"
subprocess.run(['git', 'commit', '-m', msg], capture_output=True)

# Push
result = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, text=True)
print("\n✅ All done! Changes pushed to GitHub." if result.returncode == 0 else "✓ Committed locally")

# Remove self
try: os.remove('cleanup_final.py')
except: pass
