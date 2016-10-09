from typing import List, Any

class MotionData(object):
    pass

def motion_update(motion_data: List[MotionData], state: Dict[str, Any]) -> Dict[str, Any]:
    return state

def collect_motion_data() -> List[MotionData]:
    return []
