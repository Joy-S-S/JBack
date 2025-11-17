import os, subprocess, sys
os.chdir('/workspaces/JBack')
subprocess.run(['git','config','user.email','dev@jback.local'], capture_output=True)
subprocess.run(['git','config','user.name','JBack'], capture_output=True)
r1 = subprocess.run(['git','commit','-m','Clean up: Remove temporary files and optimize project structure\n\n- Removed 20+ temporary scripts and duplicate docs\n- Updated README.md with comprehensive guide\n- Project ready for Android Studio'], capture_output=True, text=True)
print('COMMIT:', r1.returncode, r1.stdout[:100] if r1.stdout else r1.stderr[:100])
r2 = subprocess.run(['git','push','origin','main'], capture_output=True, text=True)
print('PUSH:', r2.returncode, r2.stdout[:100] if r2.stdout else r2.stderr[:100])
if r2.returncode == 0: print('\n✅ SUCCESS!')
