from copy import deepcopy
from data.get_data import GetData


def split_demands(distance_matrix: list[list], demands: list,
                  vehicle_capacity: int = 54) -> list:
    new_distance_matrix = deepcopy(distance_matrix)
    new_demands = deepcopy(demands)
    for i in range(len(demands)):
        if demands[i] > vehicle_capacity:
            # adding new row to distance matrix
            new_row = [0 for _ in range(len(new_distance_matrix))]
            new_distance_matrix.append(new_row)
            # adding new column to distance matrix
            for row in new_distance_matrix:
                row.append(0)

            # filling new column and new row

    return new_distance_matrix


matrix = [
    [0, 1, 2],
    [1, 0, 5],
    [2, 5, 0]
]
demands = [0, 10, 56]
GetData.print_matrix(split_demands(matrix, demands))
