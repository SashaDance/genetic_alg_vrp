import random
# from split import split

# class representing the individual (solution)

class Individual:
    def __init__(self, params):
        # list with all nodes which we will split later using split algorithm
        self.giant_tour: list = []
        # routes for each vehicle (complete solution)
        self.divided_routes: list[list] = []
        # distance for the route of each vehicle
        self.vehicle_distances: list = []
        # # loads that was taken by each vehicle to each node
        # self.node_loads: list = []  # 2d list
        self.cost: float = 0  # cost of the solution
        # feasibility status of solution
        self.is_feasible: bool = False
        # parameters of the problem, class Params implemented in params.py
        self.params = params

        '''
        len(self.divided_routes) == len(self.vehicle_distances) ==
        == len(self.node_loads) == num of vehicle in the route
        '''

    def create_random_individual(self) -> None:
        for i in range(1, self.params.num_of_clients + 1):
            self.giant_tour.append(i)
        random.shuffle(self.giant_tour)
        # first node is always the depot
        self.giant_tour = [0] + self.giant_tour
        # split(self.whole_route)
        # self.evaluate_individual()

    def evaluate_individual(self) -> None:
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
