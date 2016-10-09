from kalman_filter import State
from typing import Any, Dict, List

class SensorData(dict):
    def __init__(self) -> None:
        pass

    def __lt__(self, other: SensorData) -> None:
        return self['signal'] < other['signal']
    

def sensor_update(sensor_data: List[SensorData], state: State) -> State:
    for unit_sense in sensor_data:
        pass
    return state

def collect_sensor_data() -> List[SensorData]:
    return []
