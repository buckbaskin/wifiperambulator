from kalman_filter import State
from typing import Any, List, Tuple

class MotionData(dict):
    def __init__(self, *args: Tuple[Any], **kwargs: Dict[Any, Any]) -> None:
        super(MotionData, self).__init__(*args, **kwargs)

def motion_update(motion_data: List[MotionData], state: State) -> State:
    for _item in motion_data:
        pass
    return state

def collect_motion_data() -> List[MotionData]:
    return []
