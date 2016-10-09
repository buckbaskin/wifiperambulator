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


def distance(mac_address, loc_id):
    if 'C1:B8' in mac_address:
        if loc_id == 13:
            return 2.
        elif loc_id == 14:
            return 12.
        else:
            return 9000.1
    if '32:A8' in mac_address:
        if loc_id == 14:
            return 2.
        elif loc_id == 13:
            return 12.
        else:
            return 9000.1
    if '15:E8' in mac_address:
        if loc_id == 11:
            return 2.
        elif loc_id == 12:
            return 12.
        else:
            return 9000.1
    if 'A9:18' in mac_address:
        if loc_id == 12:
            return 2.
        elif loc_id == 11:
            return 12.
        else:
            return 9000.1
    return 9000.1

def main():
    split_db = TinyDB('data/split_ap.json')
    Tables = Query()
    table_list = split_db.search(Tables.id_=='tables')[0]['tables']
    table_list = list(set(table_list))

    item_sets = {}
    for mac_address in table_list:
        mac_address = str(mac_address)
        item_sets[mac_address] = split_db.table(mac_address).all()

    A = []
    b = []
    for mac_addr in table_list:
        mac_addr = str(mac_addr)
        observations = item_sets[mac_addr]
        locs = defaultdict(list)
        for item in observations:
            loc_id = item['location_id']
            distan = distance(mac_addr, loc_id)
            if distan < 9000.:
                A.append((math.log(distan), 1,))
                dBm = item['signal']
                print('[%s %s] -> %s' % (math.log(distan), 1, dBm,))
                b.append(dBm)

    if len(A) > 0 and len(b) > 0:
        err = error_function(A, b)

if __name__ == '__main__':
    main()
