import subprocess
import sys
import io
import datetime
import time

# database
from tinydb import TinyDB
top_database = TinyDB('data/live_mapping.json.freeze') 
database = top_database.table('data')

from kalman_filter.sensor.nonmetric_map import NonMetricMap
nmap = NonMetricMap(top_database)

from kalman_filter.sensor import SensorData

nice_output = {
        'E0:10:7F:7A:A9:18': 'Basement, Stage Right',
        'E0:10:7F:FE:C1:B8': 'Basement, Stage Right too',
        'E0:10:7F:FD:CB:48': 'Basement, Stage Left',
        'E0:10:7F:BE:C1:B8': 'Basement, Stage Left too',
        'E0:10:7F:3D:32:A8': 'Basement center back',
        'E0:10:7F:FD:54:A8': 'Basement outside stage right',
        '00:3A:98:91:BD:60': '1st Floor, Near Entrance',
        'F0:B0:52:9F:FC:C8': '1st to 2nd stairs',
        'F0:B0:52:1F:FC:C8': '1st to 2nd stairs too',
        'F0:B0:52:9F:F5:98': '2nd Floor, Near Concur',
        'F0:B0:52:9F:FC:C8': '2nd Floor Top Right',
        '80:1F:02:F6:6F:EA': '2nd Floor Top Right Too',
        'F0:B0:52:5F:F3:08': '3rd Floor, GE Side',
        'F0:B0:52:5F:FB:28': '3rd Floor, Front of Red Wings Room',
        'F0:B0:52:1F:FB:28': '3rd Floor Red Wings Room Too',
        'F0:B0:52:9F:FB:A8': '4th Floor Attrium',
        'F0:B0:52:61:DF:08': '4th Floor, Hardware Desk',
        'F0:B0:52:A1:DF:D8': '5th Floor, Kitchen',
        'F0:B0:52:1F:FB:18': '5th Floor, Qualtrics/RetailMeNot',
        }

command = "sudo iwlist wlan0 scanning | egrep 'Address|ESSID|Quality'"
cycles = 50

print_only = 'no'
start = 'no'
while start == 'no':
    start = input('start? y/no? ')

data = {}

for i in range(0, cycles):
    print('%4d updating' % i)
    timestamp = datetime.datetime.now()
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
        if 'Signal level' in decoded:
             special = 'Signal level='
             dBm_index = decoded.find(special) + len(special)
             dBm_str = decoded[dBm_index:-3].strip()
             dBm_int = int(dBm_str)
        if 'ESSID' in decoded:
            ssid = decoded.split('"')[1]
            if ssid and mac_address and dBm_int <= 0:
                if mac_address not in data:
                      data[mac_address] = []
                data[mac_address].append((ssid, dBm_int,))
                if print_only == 'yes':
                    print('%(mac)s | %(dBm)d' % {'mac': mac_address, 'dBm': dBm_int})
                elif '00:02' in mac_address:
                    # print('skipping my hardware')
                    pass
                else:
                    # print('SensorData(%s, %s)' % (mac_address, dBm_int,))
                    write_list.append({'mac_address': mac_address, 'signal': dBm_int})

        sys.stdout.flush()
    # print('end collection round %d' % i)
    try:
        result = nmap.get_space(write_list)
        print('location estimate %s' % (result,))
        if result[0] in nice_output:
            print('Real talk: %s at %s' % (nice_output[result[0]], result[1],))
        else:
            print('%d location estimate %s' % (i, result,))
    except IndexError:
        pass
    finally: 
        write_list = []
    # print('begin inter-round sleep')
    time.sleep(0.50)
    # print('end inter-round sleep')


print('data collected at %s' % (timestamp,))




sys.stdout.flush()

