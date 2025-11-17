#!/usr/bin/env python3
import subprocess, sys
result = subprocess.run([sys.executable, '/workspaces/JBack/cleanup_and_push.py'])
sys.exit(result.returncode)
