import subprocess
import sys
import io

command = "sudo iwlist wlan0 scanning | egrep 'ESSID|Quality'"
counter = 0
child = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
for line in child.stdout:
    if line == '' and child.poll() != None:
        break
    if line != '':
        sys.stdout.write(line.decode())
        sys.stdout.flush()

