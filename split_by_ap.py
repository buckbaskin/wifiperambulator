'''Split stored observations into location pools'''

from tinydb import TinyDB, Query

observation_db = TinyDB('data/observations.json')

with open('data/split_ap.json', 'w'):
    pass

split_db = TinyDB('data/split_ap.json')

reads = observation_db.table('reads')

observations = reads.all()

print('start converting db (ap/mac_address)')

table_list = []

counter = 0
for item in observations:
    # print(item)
    location_id = 1
    location = item['location'].lower()
    if 'stage left' in location:
        if 'stage back' in location:
            location_id = 11
        else:
            location_id = 12
    elif 'stage right' in location:
        if 'stage back' in location:
            location_id = 13
        else:
            location_id = 14
    elif 'back left pillar' in location:
        if 'outside red wing' in location:
            location_id = 7
        else:
            location_id = 5
    elif 'back right pillar' in location:
        location_id = 5
    elif 'outside back pillar' in location:
        location_id = 8
    elif 'front right pillar' in location:
        location_id = 1
    elif 'front left pillar' in location:
        if 'outisde red wing' in location:
            location_id = 3
        else:
            location_id = 2
    elif 'outside front pillar' in location:
        location_id = 4
    else:
        int(input('loc? '))
    # print('matched %d' % location_id)
    item['location_id'] = location_id
    table = split_db.table(item['mac_address'])
    table_list.append(item['mac_address'])
    counter += 1
    if counter % 100 == 0:
        print('reached item %d' % (counter,))
    table.insert(item)

# print('table list: %s' % (table_list,))
result = split_db.insert({'id_': 'tables', 'tables': table_list})

Tables = Query()
print('recovered table list: len(%s)' % (len(split_db.search(Tables.id_ == 'tables')[0]['tables']),))

print('done converting db (ap/mac_address)')
