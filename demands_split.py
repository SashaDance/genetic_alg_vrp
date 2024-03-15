from copy import deepcopy


def split_demands(data=None, demands: list[float] = None,
                  distance_matrix: list[list[float]] = None,
                  vehicle_capacity: int = 54) -> tuple[list[list], list, dict]:

    """
    Our Algorithm involves this constraint:
    -each customer can be visited only once by one vehicle
    Since our some of our sorting centers have demands
    greater than vehicle capacity, we will divide those
    demands into multiple orders. We will create
    a 'new' sorting centers so that demand in each
    sorting center is less the vehicle capacity,
    example:

        vehicle_capacity = 54
        distance_matrix = [0 | 1 | 2]
                          [1 | 0 | 5]
                          [2 | 5 | 0]
        demands = [0, 56, 14]

        new_distance_matrix = [0 | 1 | 2 | 1]
                              [1 | 0 | 5 | 0]
                              [2 | 5 | 0 | 5]
                              [1 | 0 | 5 | 0]
        new_demands = [0, 54, 14, 2]

    :param data:
    :param demands:
    :param distance_matrix:
    :param vehicle_capacity:
    :return:
    """
    # checking if user wants to get solution from ff_id or
    # wants to write his own distance matrix and demands
    flag = False

    if data is not None:
        distance_matrix = data.get_distance_matrix()
        demands = data.get_demands()
        flag = True
    elif distance_matrix is not None and demands is not None:
        ind_to_sc_map = {}
        for i in range(len(demands)):
            ind_to_sc_map[i] = i
    else:
        raise ValueError('Incorrect data input')

    # ind_to_sc_map is for printing solution with the right vertex indices

    new_distance_matrix = deepcopy(distance_matrix)
    new_demands = deepcopy(demands)
    for i, demand in enumerate(demands):
        iteration = 0
        while demand > vehicle_capacity:
            iteration += 1
            if flag:
                sc = data.ind_to_sc_map[i]
            else:
                sc = ind_to_sc_map[i]
            # adding new row to distance matrix
            new_row = deepcopy(new_distance_matrix[i]) + [0]
            new_distance_matrix.append(new_row)
            # adding new column to distance matrix
            for ind, row in enumerate(new_distance_matrix[:-1]):
                row.append(new_row[ind])
            # adding new demand
            new_demands[i] = vehicle_capacity
            demand = demand - vehicle_capacity
            if demand <= vehicle_capacity:
                new_demands.append(demand)
            else:
                new_demands.append(vehicle_capacity)
            # updating index to sc map, like '110-52-1'
            if flag:
                data.ind_to_sc_map[len(new_distance_matrix) - 1] = (
                    f'{data.ff}-{sc}-{iteration}'
                )
            else:

                ind_to_sc_map[len(new_distance_matrix) - 1] = (
                    f'{0}-{sc}-{iteration}'
                )

    if flag:
        return new_distance_matrix, new_demands, data.ind_to_sc_map
    else:
        return new_distance_matrix, new_demands, ind_to_sc_map

# TODO: try to split demands randomly

