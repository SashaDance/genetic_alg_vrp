from params import Params
from individual import Individual


# initialization of list of dicts that we will need to use in split function
def initialize_split_list(individual: Individual,
                          params: Params) -> list[dict]:
    # initialization
    split_dict = {'demand': 0, 'dist_to_depot': 0, 'dist_to_next': 0}
    split_list = [split_dict for i in range(params.num_of_clients + 1)]

    # the 0'th element corresponding to the depot
    for i in range(1, params.num_of_clients + 1):
        split_dict = {'demand': 0, 'dist_to_depot': 0, 'dist_to_next': 0}
        node = individual.giant_tour[i]
        if i != params.num_of_clients:
            next_node = individual.giant_tour[i + 1]
            split_dict['dist_to_next'] = params.distance_matrix[node][next_node]
        else:
            split_dict['dist_to_next'] = -1

        split_dict['demand'] = params.demands[node]
        split_dict['dist_to_depot'] = params.distance_matrix[node][0]
        split_list[i] = split_dict

    return split_list


# this function splits whole route to sub routes for each vehicle
def split(individual: Individual, params: Params) -> list[list[int]]:
    # initialization of the structures
    destination_info = initialize_split_list(individual, params)
    potential = [1e30 for _ in range(params.num_of_clients + 1)]
    pred = [-1 for _ in range(params.num_of_clients + 1)]

    potential[0] = 0

    # Bellman split algorithm
    cost = 0
    for i in range(1, params.num_of_clients + 1):
        load = 0
        for j in range(i, params.num_of_clients + 1):
            load += destination_info[j]['demand']
            if j == i:
                cost = 2 * destination_info[j]['dist_to_depot']
            else:
                cost = (cost - destination_info[j - 1]['dist_to_depot'] +
                        destination_info[j - 1]['dist_to_next'] +
                        destination_info[j]['dist_to_depot'])
            if (potential[i - 1] + cost < potential[j] and
                    load <= params.vehicle_capacity):
                potential[j] = potential[i - 1] + cost
                pred[j] = i - 1
            if load > params.vehicle_capacity:
                break

    # extraction of solution
    solution = []

    j = params.num_of_clients
    while j != 0:
        route = [0]  # first node is always a depot
        for k in range(pred[j] + 1, j + 1):
            route.append(indiv.giant_tour[k])
        route.append(0)  # last node is also a depot

        j = pred[j]
        solution.append(route)

    return solution


distance_matrix = [
    [0, 20, 25, 30, 40, 35],
    [20, 0, 10, 0, 0, 0],
    [25, 10, 0, 30, 0, 0],
    [30, 0, 30, 0, 25, 0],
    [40, 0, 0, 25, 0, 15],
    [35, 0, 0, 0, 15, 0]
]
vehicle_capacity = 10
demands = [0, 5, 4, 4, 2, 7]
time_limit = 0
params = Params(distance_matrix, vehicle_capacity, demands, time_limit)

indiv = Individual(params)
indiv.giant_tour = [0, 1, 2, 3, 4, 5]

print(split(indiv, params))