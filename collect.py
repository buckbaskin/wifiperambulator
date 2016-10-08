import subprocess
import sys
import io

import datetime

command = "sudo iwlist wlan0 scanning | egrep 'Address|ESSID|Quality'"
counter = 0

# from collections import defaultdict
time = datetime.datetime.now()
data = {}

cycles = 2
for i in range(0, cycles):
    child = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    for line in child.stdout:
        if line == '' and child.poll() != None:
            break
        if line == '':
            continue
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
             ssid = decoded.split('"')[1]
             # print('ssid decode: %s' % (decoded,))
             # print('ssid %s' % (essid,))
             # print('ssid|addr|dBm - %s|%s|%d' % (ssid, mac_address, dBm_int,))
             if ssid and mac_address and dBm_int <= 0:
                 if mac_address not in data:
                      data[mac_address] = []
                 data[mac_address].append((ssid, dBm_int,))
        sys.stdout.flush()

print('data collected at %s' % (time,))

for key in data:
    list_of_results = data[key]
    if len(list_of_results) <= 1:
        continue
    base_ssid = list_of_results[0][0]
    for tup_ in list_of_results:
        if tup_[0] != base_ssid:
            print('ssid fail')
            continue

    sum_ = 0
    max_ = -100
    min_ = 0
    for tup_ in list_of_results:
        sum_ += tup_[1]
        max_ = max(max_, tup_[1])
        min_ = min(min_, tup_[1])

    print('%s -> %s > %s > %s' % (base_ssid, max_, float(sum_)/len(list_of_results), min_,))
sys.stdout.flush()
