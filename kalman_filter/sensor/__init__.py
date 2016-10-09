from kalman_filter import State
from typing import Any, Dict, List, Tuple

class SensorData(dict):
    def __init__(self, mac_address, signal, *args: Tuple[Any], **kwargs: Dict[Any, Any]) -> None:
        super(SensorData, self).__init__(*args, **kwargs)
        self['mac_address'] = mac_address
        self['signal'] = signal

    def __lt__(self, other: 'SensorData') -> None:
        return not (self['signal'] < other['signal'])
    

def sensor_update(sensor_data: List[SensorData], state: State) -> State:
    for unit_sense in sensor_data:
        pass
    return state

def collect_sensor_data() -> List[SensorData]:
    return []
