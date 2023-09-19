
# parameters of the vrp problem

class Params:
    def __init__(self,
                 distance_matrix: list,
                 vehicle_capacity: float,
                 demands: list,
                 route_time_limit: float):
        self.distance_matrix = distance_matrix  # 0 node is the depot
        self.vehicle_capacity = vehicle_capacity
        self.demands = demands  # firs demand is always 0
        self.route_time_limit = route_time_limit
        self.num_of_nodes = len(demands)
