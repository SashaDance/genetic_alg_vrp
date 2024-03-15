from dataclasses import dataclass


@dataclass
class Params:
    # parameters of the vrp problem
    distance_matrix: list[list]
    vehicle_capacity: float
    demands: list
    route_time_limit: float

    def __post_init__(self):
        self.num_of_clients = len(self.demands) - 1
