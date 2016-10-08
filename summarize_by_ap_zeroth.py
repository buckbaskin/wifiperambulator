'''Split stored observations into location pools'''

from tinydb import TinyDB, Query
from collections import defaultdict

split_db = TinyDB('data/split_ap.json')

Tables = Query()
table_list = split_db.search(Tables.id_=='tables')[0]['tables']
table_list = list(set(table_list))
item_sets = {}
for mac_address in table_list:
    mac_address = str(mac_address)
    item_sets[mac_address] = split_db.table(mac_address).all()

print('start selecting from db')

for mac_address in table_list:
    mac_address = str(mac_address)
    observations = item_sets[mac_address]
    locs = defaultdict(list)
    for item in observations:
        if item['location_id'] < 11:
            continue
        if item['signal'] < -40:
            continue
        locs[item['location_id']].append(item)
    
    if len(locs) >= 1:
        print('\n%s' % (mac_address,))
    else:
        continue

    for key in locs:
        list_ = locs[key]
        max_signal = -100
        min_signal = -0
        sum_signal = 0

        for item in list_:
            sum_signal += item['signal']
            max_signal = max(max_signal, item['signal'])
            min_signal = min(min_signal, item['signal'])

        print('  %d | %s' % (list_[0]['location_id'], int(float(sum_signal)/len(list_)),))

print('done selecting from db')
