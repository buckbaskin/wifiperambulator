import subprocess
import sys
import io

print('parse output, display it again in a nice sorted way')
command = "sudo iwlist wlan0 scanning | egrep 'Address|ESSID|Quality'"
counter = 0
child = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
for line in child.stdout:
    if line == '' and child.poll() != None:
        break
    if line != '':
        decoded = line.decode().strip()
        # sys.stdout.write(decoded+'\n')
        if 'Address' in decoded:
             mac_address = decoded.split(' ')[4]
             # print('mac_address %s' % (mac_address,))
        if 'Signal level' in decoded:
             special = 'Signal level='
             dBm_index = decoded.find(special) + len(special)
             dBm_str = decoded[dBm_index:-3].strip()
             dBm_int = int(dBm_str)
             # print('dbm %d' % (dBm_int,))
        if 'ESSID' in decoded:
             essid = decoded.split('"')[1]
             print('ssid decode: %s' % (decoded,))
             # print('ssid %s' % (essid,))
             print('ssid|addr|dBm - %s|%s|%d' % (essid, mac_address, dBm_int,))
        sys.stdout.flush()

