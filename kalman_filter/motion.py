from kalman_filter import State
from typing import List, Any

class MotionData(object):
    pass

def motion_update(motion_data: List[MotionData], state: State) -> State:
    return state

def collect_motion_data() -> List[MotionData]:
    return []
