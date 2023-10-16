from params import Params
from individual import Individual


def initialize_split_list(individual: Individual,
                          params: Params) -> list[dict]:
    """
    initialization of list of dicts that we will need to use in split function
    that is a some kind of data structure
    :param individual:
    :param params:
    :return:
    """
    # initialization
    split_dict = {'demand': 0, 'dist_to_depot': 0, 'dist_to_next': 0}
    split_list = [split_dict for i in range(params.num_of_clients + 1)]

    # the 0'th element corresponding to the depot
    for i in range(1, params.num_of_clients + 1):
        split_dict = {'demand': 0, 'dist_to_depot': 0, 'dist_to_next': 0}
        node = individual.giant_tour[i]
        if i != params.num_of_clients:
            next_node = individual.giant_tour[i + 1]
            split_dict['dist_to_next'] = params.distance_matrix[node][
                next_node]
        else:
            split_dict['dist_to_next'] = -1

        split_dict['demand'] = params.demands[node]
        split_dict['dist_to_depot'] = params.distance_matrix[node][0]
        split_list[i] = split_dict

    return split_list


def split(individual: Individual, params: Params) -> list[list[int]]:
    """
    this function splits whole route to sub routes for each vehicle
    :param individual:
    :param params:
    :return: split route
    """
    # initialization of the structures
    destination_info = initialize_split_list(individual, params)
    potential = [1e30 for _ in range(params.num_of_clients + 1)]
    pred = [-1 for _ in range(params.num_of_clients + 1)]

    potential[0] = 0

    # Bellman split algorithm
    cost = 0
    for i in range(1, params.num_of_clients + 1):
        load = 0
        len_of_route = 0
        for j in range(i, params.num_of_clients + 1):
            len_of_route += 1
            load += destination_info[j]['demand']
            if j == i:
                cost = 2 * destination_info[j]['dist_to_depot']
            else:
                cost = (cost - destination_info[j - 1]['dist_to_depot'] +
                        destination_info[j - 1]['dist_to_next'] +
                        destination_info[j]['dist_to_depot'])
            if (potential[i - 1] + cost < potential[j] and
                    load <= params.vehicle_capacity and
                    len_of_route < 4):
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
            route.append(individual.giant_tour[k])
        route.append(0)  # last node is also a depot

        j = pred[j]
        solution.append(route)

    return solution

# TODO: use dataclass instead of initialize_split_list
