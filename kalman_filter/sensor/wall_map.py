from kalman_filter import Position

class WallMap(object):
    def __init__(self) -> None:
        pass
    def update(est_pos: Position, mac_addr: str, dBm: int) -> None:
        pass

    def wall_likelihood(est_pos: Position, mac_addr: str, dBm: int) -> float:
        return 0.0

    def clear_likelihood(est_pos: Position, mac_addr: str, dBm: int) -> float:
        return 1.0
