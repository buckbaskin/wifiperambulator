from kalman_filter import Position

class WallMap(object):
    def __init__(self) -> None:
        pass
    def update(self, est_pos: Position, mac_addr: str, dBm: int) -> None:
        #TODO
        pass

    def wall_likelihood(self, est_pos: Position, mac_addr: str, dBm: int) -> float:
        #TODO
        return 0.0

    def clear_likelihood(self, est_pos: Position, mac_addr: str, dBm: int) -> float:
        #TODO
        return 1.0
