'''Split stored observations into location pools'''

from tinydb import TinyDB

split_db = TinyDB('data/split_loc.json')
item_sets = {}
for i in range(1, 1+8):
    item_sets[str(i)] = split_db.table(str(i)).all()

print('start selecting from db')

for i in range(1, 1+8):
    observations = item_sets[str(i)]
    APs = {}
    for item in observations:
        if item['mac_address'] not in APs:
            # print('new mac address %s' % item['mac_address'])
            APs[item['mac_address']] = []
        APs[item['mac_address']].append(item)

    for key in APs:
        # print('APs key %s' % APs)
        list_ = APs[key]
        max_signal = -100
        min_signal = -0
        sum_signal = 0

        for item in list_:
            sum_signal += item['signal']
            max_signal = max(max_signal, item['signal'])
            min_signal = min(min_signal, item['signal'])

        if 'MHacksGuest' not in list_[0]['ssid']:
            continue
        list_[0]['mac_address'] = list_[0]['mac_address'][-8:]
        print('%d | %s %s | %s' % (i, list_[0]['ssid'], list_[0]['mac_address'], int(float(sum_signal)/len(list_)),))
    print('')
print('done selecting from db')
