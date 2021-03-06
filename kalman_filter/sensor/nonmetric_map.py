from collections import namedtuple, defaultdict
from kalman_filter.sensor import SensorData
from typing import Any, Dict, List, Set, Tuple

Annotation = namedtuple('Annotation', ['occurences', 'av_dBm'])

APInfo = Dict[str, Annotation]
ForwardMap = Dict[str, APInfo]
BackwardMap = Dict[str, Set[str]]

class _MapRepr(object):
    _forward = None  # type: ForwardMap
    _backward = None # type: BackwardMap
    
    def __init__(self, *args: Tuple[Any], **kwargs: Dict[Any, Any]) -> None:
        self._forward = defaultdict(dict)
        self._backward = defaultdict(set)

    def add_pair(self, mac1: str, mac2: str, dBm2: int) -> None:
        if mac1 == mac2:
            return None
        if mac2 not in self._forward[mac1]:
            self._forward[mac1][mac2] = Annotation(occurences=0, av_dBm=0.0)
        old_count = self._forward[mac1][mac2][0]
        old_avg = self._forward[mac1][mac2][1]
        new_avg = (old_avg*old_count + dBm2)/(old_count+1)
        new_count = old_count + 1
        self._forward[mac1][mac2] = Annotation(occurences=new_count, av_dBm=new_avg)
        self._backward[mac2].add(mac1)

    @property
    def forward(self) -> ForwardMap:
        return self._forward

    @property
    def back(self) -> BackwardMap:
        return self._backward

    @property
    def backward(self) -> BackwardMap:
        return self._backward

class NonMetricMap(object): 
    '''
    Make a map that represents spaces based on their strongest AP
    '''
    def __init__(self, database=None) -> None:
        self.map_repr = _MapRepr()
        if database is not None:
            self.load_from_database(database)

    def load_from_database(self, database):
        data = database.table('data').all()
        for data_list in data:
            sensor_data = []
            data_list = data_list['data']
            for item in data_list:
                inter = SensorData(item['mac_address'], item['signal'])
                sensor_data.append(inter)
            self.update(sensor_data)

    def update(self, sensor_data: List[SensorData]) -> None:
        if len(sensor_data) <= 0:
            return None
        sensor_data = sorted(sensor_data)
        base = sensor_data[0]
        for reading in sensor_data:
            if reading['mac_address'] == base['mac_address']:
                continue
            self.map_repr.add_pair(base['mac_address'], reading['mac_address'], reading['signal'])
        old_estimate = self.get_space(sensor_data)
        print('k/s/n: old %s' % (old_estimate,))
        if old_estimate[1] < .5:
            self.create_space(sensor_data)
    
    def create_space(self, sensor_data: List[SensorData]) -> None:
        sensor_data = sorted(sensor_data)
        base = sensor_data[0]
        for index, new_base in enumerate(sensor_data):
            if new_base['mac_address'] not in self.map_repr.forward:
                base = sensor_data[index]
                break

        for reading in sensor_data:
            self.map_repr.add_pair(base['mac_address'], reading['mac_address'], reading['signal'])

    def get_space(self, sensor_data: List[SensorData]) -> Tuple[str, float]:
        max_probability = 0.0
        max_base = sensor_data[0]['mac_address']
        for base_candidate in sensor_data:
            base_addr = base_candidate['mac_address']
            probability = 1
#            max_likelihood_base, probability = self._max_likelihood_base(sensor_data)
            existing_space = self.map_repr.forward[base_addr]
            # update for previously not seen data
            for reading in sensor_data:
                mac_addr = reading['mac_address']
                if mac_addr != base_addr and mac_addr not in existing_space:
                    probability *= self._probability_found(base_addr, mac_addr, reading['signal'])
            # update for data that was supposed to be there but isn't
            for old_mac in existing_space:
                for reading in sensor_data:
                    if reading['mac_address'] == old_mac:
                        break
                else:
                    probability *= self._probabilty_missing(base_addr, old_mac)
            print('%s -> %4.4f' % (base_addr, probability,))
            if probability > max_probability:
                max_probability = probability
                max_base = base_addr
        return max_base, max_probability

    def _probability_found(self, base: str, not_prev_seen_mac: str, dBm: int) -> float:
        '''probability that a new mac address was actually there originally'''
        # dBm == 0 -> 0.0
        # dBm <= -100 -> 1.0
        if not_prev_seen_mac in self.map_repr.forward[base]:
            return 1.0
        return min(1., max(0., dBm / -100.))

    def _probabilty_missing(self, base: str, prev_seen_mac: str) -> float:
        '''probability that a previously seen mac address is okay to not be there'''
        old_avg_dBm = self.map_repr.forward[base][prev_seen_mac][1]
        return min(1., max(0., old_avg_dBm / -100.))

    def _max_likelihood_base(self, sensor_data: List[SensorData]) -> Tuple[str, float]:
        maxDBm = -101
        maxIndex = 0
        for i in range(0, len(sensor_data)):
            reading = sensor_data[i]
            if reading['signal'] > maxDBm:
                maxDBm = reading['signal']
                maxIndex = i+0

        maxProb = 0.0
        maxIndex = 0
        
        for i in range(0, len(sensor_data)):
            reading = sensor_data[i]
            prob = self._probability_base_unit(reading['mac_address'], reading['signal'], maxDBm)
            if prob > maxProb:
                maxProb = prob + 0.0
                maxIndex = i

        return sensor_data[maxIndex]['mac_address'], maxProb

    def _probability_base_unit(self, mac_addr: str, dBm: int, minDBm: int) -> float:
        # this is the base to at most 1 existing base
        if mac_addr not in self.map_repr.forward:
            return 0.0
        # this may be contained in as many bases are there are backrefs
        num_contained = len(self.map_repr.back[mac_addr])
        if num_contained == 0:
            prior = 1.0
        else:
            prior = 1./num_contained # ratio of base spaces to all containing spaces

        # "min" 0, dBm -100 -> 0.0
        # "min" -50, dBm -100 -> 0.5
        # "min" -100, dBm -100 -> 1.0
        if minDBm < dBm:
            update = float(minDBm)/dBm # ratio of this dBm to the min
        else:
            update = 1.0

        return prior*update

