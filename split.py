from params import Params

# this function splits whole route to sub routes for each vehicle
def split(params):

    # initialization of the structures
    potential = [1e30 for _ in range(params.num_of_clients + 1)]
    pred = [-1 for _ in range(params.num_of_clients + 1)]

    potential[0] = 0

    # Bellman split algorithm
    cost = 0
    for i in range(1, params.num_of_clients + 1):
        load = 0
        for j in range(i, params.num_of_clients + 1):
            load += params.demands[j]
            if j == i:
                cost = (params.distance_matrix[0][j] +
                        params.distance_matrix[j][0])
            else:
                cost = (cost - params.distance_matrix[j-1][0] +
                        params.distance_matrix[j-1][j] +
                        params.distance_matrix[j][0])
            if (potential[i - 1] + cost < potential[j] and
                load <= params.vehicle_capacity):
                potential[j] = potential[i - 1] + cost
                pred[j] = i - 1
            if load > params.vehicle_capacity:
                break

    print(potential)
    print(pred)

    # extraction of solution
    solution = []

    j = params.num_of_clients
    while j != 0:
        route = [0]  # first node is always a depot
        for k in range(pred[j] + 1, j + 1):
            route.append(k)
        route.append(0)  # last node is also a depot

        j = pred[j]
        solution.append(route)

    print(solution)

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
split(params)
