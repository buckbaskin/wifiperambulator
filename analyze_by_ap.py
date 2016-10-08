'''Split stored observations into location pools'''
import math

import numpy
from tinydb import TinyDB, Query
from collections import defaultdict
from typing import List, Dict, Any

def error_function(A, b):
    # calculate the best fit and return the error from that fit
    A = numpy.array(A)
    b = numpy.array(b)
    x, residuals, rank, singular_values = numpy.linalg.lstsq(a=A, b=b)
    
    print('x: %s' % (x,))
    b_alt = numpy.dot(A, x)
    err = numpy.subtract(b, b_alt)
    return numpy.sum(err)

def dist_to_loc_id(x, y, loc_id):
    if loc_id >= 5:
        ly = 8
        loc_id -= 4
    else:
        ly = 0
    if loc_id == 1:
        lx = 0
    elif loc_id == 2:
        lx = 8
    elif loc_id == 3:
        lx = 8+1
    elif loc_id == 4:
        lx = 8+1+8
    else:
        assert False

    dx = x-lx
    dy = y-ly

    return math.sqrt(dx*dx + dy*dy)

def analyze_space(
        mac_address: str,
        dict_by_loc_id: Dict[int, List[Dict[str, Any]]]):
    # print(dict_by_loc_id)
    locs = dict_by_loc_id
    for x in range(-4,-4+2*8+1, 8):
        for y in range(-4, -4+3*8+1, 8):
            A = []
            b = []
            for loc_id in locs:
                dist_to_loc = dist_to_loc_id(x, y, loc_id=loc_id)
                for datapoint in locs[loc_id]:
                    dBm = datapoint['signal']
                    A.append((math.log(dist_to_loc), 1,))
                    b.append(dBm)
                    print('[%s %s] -> %s' % (math.log(dist_to_loc), 1, dBm,))

            # print('A: %s\nB: %s' % (A, b,))
            err = error_function(A=A, b=b)
            print('%s | error at (%s, %s) is %s' % (mac_address, x, y, err,))
    
def main():
    split_db = TinyDB('data/split_ap.json')

    Tables = Query()
    table_list = split_db.search(Tables.id_=='tables')[0]['tables']
    table_list = list(set(table_list))
    item_sets = {}
    for mac_address in table_list:
        mac_address = str(mac_address)
        item_sets[mac_address] = split_db.table(mac_address).all()

    print('start analyzing for log fit')

    for mac_address in table_list:
        mac_address = str(mac_address)
        observations = item_sets[mac_address]
        locs = defaultdict(list)
        for item in observations:
            if 'MHacksGuest' not in item['ssid']:
                continue
            locs[item['location_id']].append(item)

        if len(locs) <= 0:
            continue
        if len(locs) >= 3:
            print('\n%s **' % (mac_address,))
        else:
            continue
            print('\n%s' % (mac_address,))
        for key in locs:
            list_ = locs[key]
            max_signal = -100
            min_signal = -0
            sum_signal = 0

            for item in list_:
                sum_signal += item['signal']
                max_signal = max(max_signal, item['signal'])
                min_signal = min(min_signal, item['signal'])
            avg_signal = float(sum_signal)/len(list_)

        print('the real mvp')
        analyze_space(mac_address, locs)
        print('end the real mvp')
        break

    print('done analyzing for log fit')

if __name__ == '__main__':
    main()
