'''
Kalman Filter for State estimation with wifi
'''

from collections import namedtuple

Position = namedtuple('Position', ['x', 'y', 'z'])

class State(object):
    def __init__(self) -> None:
        self.p = Position(x=0.0, y=0.0, z=0.0)

    def update(self, p: Position):
        self.p = p

    @property
    def state(self):
        return self.p

def init_state() -> State:
    return State()



if __name__ == '__main__':
    from kalman_filter.motion import collect_motion_data, motion_update
    from kalman_filter.sensor import collect_sensor_data, sensor_update
 
    state = init_state()
    while True:
        print('motion update')
        state = motion_update(collect_motion_data(), state)
        state = sensor_update(collect_sensor_data(), state)
