
# class representing the individual (solution)

class Individual:
    def __init__(self, params):
        # list with all nodes which we will split later using split algorithm
        self.whole_route: list = []
        # routes for each vehicle (complete solution)
        self.divided_routes: list = []
        # distance for the route of each vehicle
        self.vehicle_distances: list = []
        self.cost: float = 0  # cost of the solution
        # feasibility status of solution
        self.is_feasible: bool = False
        # parameters of the problem, class Params implemented in params.py
        self.params = params
        # TODO: implement data structure which saves demand that
        #  was taken by vehicle for each node

    def evaluate_individual(self):
        for i in range(len(self.divided_routes)):
            distance = 0
            curr_route = self.divided_routes[i]
            for j in range(len(curr_route) - 1):
                curr_node = self.divided_routes[i][j]
                next_node = self.divided_routes[i][j + 1]
                distance += self.params.distance_matrix[curr_node][next_node]
            self.vehicle_distances.append(distance)
            self.is_feasible = distance <= self.params.vehicle_capacity
            self.cost += distance
