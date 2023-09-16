from params import Params


# class representing the individual (solution)

class Individual:
    def __init__(self, params: Params):
        # list with all nodes which we will split later using split algorithm
        self.whole_route: list = []
        # routes for each vehicle (complete solution)
        self.divided_route: list = []
        # distance for the route of each vehicle
        self.vehicle_distances: list = []
        self.cost: float = 0  # cost of the solution
        # feasibility status of solution
        self.is_feasible: bool = False
        self.params = params  # parameters of the problem

    def calculate_cost(self):
        pass
