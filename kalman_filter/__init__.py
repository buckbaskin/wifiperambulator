from kalman_filter.motion import collect_motion_data, motion_update
from kalman_filter.sensor import collect_sensor_data, sensor_update

def init_state():
    return {}



if __name__ == '__main__':
    state = init_state()
    while(True):
        print('motion update')
        state = motion_update(collect_motion_data(), state)
        state = sensor_update(collect_sensor_data(), state)

