import subprocess
import os


subprocess.call('powershell.exe Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser', shell=True)
subprocess.call('powershell.exe Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression')

os.system('scoop install ffmpeg')
os.system('pip install -r requirements.txt')