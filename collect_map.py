import subprocess
import sys
import io
import datetime

# database
from tinydb import TinyDB
top_database = TinyDB('data/live_mapping.json') 
database = top_database.table('data')

from kalman_filter.sensor.nonmetric_map import NonMetricMap
nmap = NonMetricMap(database)

from kalman_filter.sensor import SensorData

def schema_to_db(
        time: 'datetime.datetime',
        location: str,
        mac_address: str,
        signal: int,
        ssid: str):
    return {
            'time': {
                'year': time.year,
                'month': time.month,
                'day': time.day,
                'hour': time.hour,
                'minute': time.minute,
                'second': time.second,
                'microsecond': time.microsecond
                },
            'location': location,
            'mac_address': mac_address,
            'signal': signal,
            'ssid': ssid
            }


command = "sudo iwlist wlan0 scanning | egrep 'Address|ESSID|Quality'"
cycles = int(input('cycles? '))
counter = 0

start = 'no'
while start == 'no':
    start = input('start? y/no? ')

data = {}

for i in range(0, cycles):
    print('begin collection round %d' % i)
    time = datetime.datetime.now()
    child = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    write_list = []
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
                if print_only == 'yes':
                    print('%(mac)s | %(dBm)d' % {'mac': mac_address, 'dBm': dBm_int})
                elif '00:02' in mac_address:
                    print('skipping my hardware')
                else:
                    print('SensorData(%s, %s)' % (mac_address, dBm_int,))
                    write_list.append({'time': time, 'mac_address': mac_address, 'signal': dBm_int})

        sys.stdout.flush()
    database.insert(write_list)
    nmap.update(write_list)
    print('end collection round %d' % i)

print('data collected at %s' % (time,))

nmap.get_space(write_list)

sys.stdout.flush()

