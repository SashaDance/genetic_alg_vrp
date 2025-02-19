from params import Params
from get_data import GetData
from individual import Individual
from local_search import vns
from split import split
import sys
from demands_split import split_demands

ff_id = 110

data = GetData(ff_id)
distance_matrix, demands, ind_to_sc_map = data.get_data()

vehicle_capacity = 54

params = Params(distance_matrix, vehicle_capacity, demands, 0)
indiv = Individual(params)
indiv.giant_tour = vns(params, max_iter=30)

indiv.divided_routes = split(indiv, params)
indiv.evaluate_individual()

total_distance = indiv.cost

sys.stdout = open(f'{ff_id}.txt', 'w')

print(f'FF id - {ff_id}\n')
for i, route_ in enumerate(indiv.divided_routes, start=1):
    route = route_[1:-1]
    route_distance = 0
    for j in range(len(route_) - 2):
        node = route_[j]
        next_node = route_[j + 1]
        route_distance += params.distance_matrix[node][next_node]
    print(f'Route for vehicle {i}:')
    # printing the right indices
    route_changed_sc_indices = dict()
    route_demands = 0
    for vertex in route:
        sc = ind_to_sc_map[vertex]
        if isinstance(sc, str):
            ff, sc, id = sc.split('-')
        load = demands[vertex]
        route_changed_sc_indices[sc] = load
        route_demands += demands[vertex]

    # distance from last sc to ff
    distance = distance_matrix[0][route[-1]]
    total_distance -= distance

    for index, (sc, load) in enumerate(route_changed_sc_indices.items()):
        print(f'{sc} ({load})', end='')
        if index < len(route_changed_sc_indices) - 1:
            print(' -> ', end='')

    print(f'\nRoute demands: {route_demands}')
    print(f'Route distance: {route_distance}\n')


print(f'Total route demands: {sum(demands)}\n')
print(f'Total route distance: {total_distance}\n')


