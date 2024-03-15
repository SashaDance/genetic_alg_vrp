import random
from get_data import GetData
from params import Params

"""
implementation of Variable Neighborhood Search
This algorithm basicly reshuffles the giant tour to minimize its distance
Giant tour is just an array of all nodes that are needed to be visited
in our case it is a list of all sort centers
"""


def calc_distance(giant_tour: list[int],
                  distance_matrix: list[list[float]]) -> float:
    """
    just calculating the distance of the route

    :param giant_tour:
    :param distance_matrix:
    :return: distance of that route
    """
    sum_ = 0

    for i in range(len(giant_tour) - 1):
        cur_node = giant_tour[i]
        next_node = giant_tour[i + 1]
        sum_ += distance_matrix[cur_node][next_node]

    return sum_


def two_opt(giant_tour: list[int], i: int, j: int) -> list[int]:
    """
    this a 2-opt heuristic defining the neighborhood
    you just select two edges and reversing the route between them

    :param giant_tour:
    :param i:
    :param j:
    :return: processed route
    """
    new_tour = giant_tour[:i] + giant_tour[i:j + 1][::-1] + giant_tour[j + 1:]

    return new_tour


def local_search(giant_tour: list[int],
                 distance_matrix: list[list[float]]) -> list[int]:
    """
    searching for the best solution in the neighborhood of giant_tour
    By neighborhood we understand routes that can be obtained with two-opt
    doing operator on giant_tour

    :param giant_tour:
    :param distance_matrix:
    :return: local optimum in the neighborhood
    """
    better_solution_found = True
    while better_solution_found:
        better_solution_found = False
        for i in range(1, len(giant_tour) - 1):
            for j in range(i + 1, len(giant_tour)):
                if j - i == 1:
                    continue
                new_tour = two_opt(giant_tour, i, j)
                if (calc_distance(new_tour, distance_matrix) <
                        calc_distance(giant_tour, distance_matrix)):
                    giant_tour = new_tour
                    better_solution_found = True

    return giant_tour


def shaking(giant_tour: list[int], k: int) -> list[int]:
    """
    this adds randomness to the algorithm to 'escape' local optimum
    :param giant_tour:
    :param k:
    :return: shaked tour
    """
    new_tour = giant_tour.copy()
    for _ in range(k):
        i, j = sorted(random.sample(range(1, len(giant_tour)), 2))
        new_tour = two_opt(new_tour, i, j)

    return new_tour


def vns(params: Params, max_iter=100) -> list[int]:
    distance_matrix = params.distance_matrix
    giant_tour = list(range(params.num_of_clients + 1))
    """
    the main alg
    :param params: look at the Params class
    :param max_iter: max iterations without improvement
    :return: optimized giant tou
    """
    i = 1
    while i <= max_iter:
        k_tour = shaking(giant_tour, i)
        new_tour = local_search(k_tour, distance_matrix)
        new_tour_dist = calc_distance(new_tour, distance_matrix)
        if new_tour_dist < calc_distance(giant_tour, distance_matrix):
            giant_tour = new_tour
            i = 1
        else:
            i += 1

    return giant_tour


if __name__ == '__main__':
    data = GetData(110)
    distance_matrix, demands, ind_to_sc_map = data.get_data()
    params = Params(distance_matrix, 54, demands, 0)
    res = vns(params)
    print(calc_distance(res, distance_matrix))
    print(res)
