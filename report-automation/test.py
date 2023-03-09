import subprocess
import sys

cmd = 'ps'
p = subprocess.Popen(['powershell.exe', cmd], stdout=sys.stdout)
print(p)