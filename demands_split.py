from copy import deepcopy


def split_demands(data,
                  vehicle_capacity: int = 54) -> tuple[list[list], list]:

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
    :param vehicle_capacity:
    :return: new distance matrix and demands of the divided route
    """
    distance_matrix = data.get_distance_matrix()
    demands = data.get_demands()

    new_distance_matrix = deepcopy(distance_matrix)
    new_demands = deepcopy(demands)
    for i, demand in enumerate(demands):
        iteration = 0
        while demand > vehicle_capacity:
            iteration += 1
            sc = data.ind_to_sc_map[i]
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
            data.ind_to_sc_map[len(new_distance_matrix) - 1] = (
                f'{data.ff}-{sc}-{iteration}'
            )

    return new_distance_matrix, new_demands

