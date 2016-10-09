from collections import namedtuple, defaultdict
from kalman_filter.sensor import SensorData
from typing import Any, Dict, Tuple

Annotation = namedtuple('Annotation', ['occurences', 'av_dBm'])

class _MapRepr(object):
    def __init__(self):
        self._repr = defaultdict(dict)

    def add_pair(self, mac1: str, mac2: str, dBm2: int) -> None:
        if mac1 == mac2:
            return None
        if mac2 not in self._repr[mac1]:
            self._repr[mac1][mac2] = Annotation(occurences=0, av_dBm=0.0)
        old_count = self._repr[mac1][mac2]['occurences']
        old_avg = self._repr[mac1][mac2]['av_dBm']
        new_avg = (old_avg*old_count + dBm2)/(old_count+1)
        new_count = old_count + 1
        self._repr[mac1][mac2] = Annotation(occurences=new_count, av_dBm=new_avg)

class NonMetricMap(object): 
    '''
    Make a map that represents spaces based on their strongest AP
    '''
    def __init__(self):
       self.map_repr = _MapRepr()

    def update(self, sensor_data: List[SensorData]) -> None:
        if len(sensor_data) <= 0:
            return None
        sensor_data = sorted(sensor_data)
        base = sensor_data[0]
        for reading in sensor_data:
            if reading['mac_address'] == base['mac_address']:
                continue
            self.map_repr.add_pair(base['mac_address'], reading['mac_address'], reading['signal'])
        if self.get_space(sensor_data)[1] < .5:
            self.create_space(sensor_data)
    
    def create_space(self, sensor_data: List[SensorData]) -> None:
        sensor_data = sorted(sensor_data)
        base = sensor_data[0]
        for reading in sensor_data:
            self.map_repr.add_pair(base['mac_address'], reading['mac_address'], reading['signal'])

    def get_space(self, sensor_data: List[SensorData]) -> Tuple[str, float]:
        max_likelihood_base, probability = self._max_likelihood_base(sensor_data)
        existing_space = self.map_repr[max_likelihood_base]
        # update for previously not seen data
        for reading in sensor_data:
            mac_addr = reading['mac_address']
            if mac_addr != max_likelihood_base and mac_addr not in existing_space:
                probability *= self._probability_found(max_likelihood_base, mac_addr, reading['signal'])
        # update for data that was supposed to be there but isn't
        for old_mac in existing_space:
            for reading in sensor_data:
                if reading['mac_address'] == old_mac:
                    break
            else:
                probability *= self._probabilty_missing(max_likelihood_base, old_mac)
        return max_likelihood_base, probability

    def _probability_found(self, base: str, not_prev_seen_mac: str, dBm: int) -> float:
        '''probability that a new mac address was actually there originally'''
        #TODO
        return 0.1

    def _probabilty_missing(self, base: str, prev_seen_mac: str) -> float:
        '''probability that a previously seen mac address is okay to not be there'''
        #TODO
        return 0.1

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
        #TODO
        prior = 0.5 # ratio of base spaces to all containing spaces
        update = float(minDBm)/dBm # ratio of this dBm to the min
        return prior*update

