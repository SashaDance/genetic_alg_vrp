import random

from local_search import local_search
from split import split
from individual import Individual
from params import Params


class Population:
    def __init__(self, population_size: int,
                 elite_size: int,
                 params):
        self.population_size = population_size
        self.population: dict[int, Individual] = {}
        self.elite_size = elite_size
        self.params = params

    def generate_initial_population(self) -> None:
        for i in range(self.population_size):
            indiv = Individual(self.params)
            indiv.random_init()
            indiv.divided_routes = split(indiv, self.params)
            indiv.evaluate_individual()

            self.population[i] = indiv

    def rank_population(self):
        # sorting list by descending of fitness
        self.population = sorted(
            self.population,
            key=lambda item: item[1]._fitness,
            reverse=True
        )

    def selection(self) -> list[int]:
        """
        Fitness proportionate selection
        :return: keys of selected individuals
        """
        fitness_sum = 0
        for indiv in self.population.values():
            fitness_sum += indiv._fitness

        cum_sum_prob = {}
        cum_sum = 0
        for key, indiv in self.population.items():
            cum_sum += indiv._fitness
            prob = cum_sum / fitness_sum
            cum_sum_prob[key] = prob

        # saving indices of elite members of population
        selection_res = [
            key for key in self.population.keys()[:self.elite_size]
        ]

        # selection of other members
        for key in self.population.keys()[self.elite_size:]:
            rand_prob = random.random()
            if cum_sum_prob[key] >= rand_prob:
                selection_res.append(key)

        return selection_res

    @staticmethod
    def crossover(parent_1: list, parent_2: list) -> list:
        """
        OX crossover operator to breed parents
        :param parent_1:
        :param parent_2:
        :return: a child (i.e. a solution)
        """
        first_cut_point = random.randint(1, len(parent_1))
        second_cut_point = random.randint(first_cut_point, len(parent_1))

        slice_ = parent_1[first_cut_point:second_cut_point]
        print(first_cut_point, second_cut_point, slice_)
        other_nodes = [node for node in parent_2 if node not in slice_]

        child = (
                other_nodes[:first_cut_point] +
                slice_ +
                other_nodes[first_cut_point:]
        )

        return child

    def produce_offspring(self, selection_res: list[int]) -> list[Individual]:
        children = []

        # retain elite individuals from the current population
        children = [
            self.population[ind] for ind in selection_res[:self.elite_size]
        ]

        breeding_pool = random.sample(
            selection_res, len(selection_res) - self.elite_size
        )
        for i in range(len(breeding_pool) // 2):
            child_route = Population.crossover(
                breeding_pool[i], breeding_pool[len(breeding_pool) - i - 1]
            )
            # creating new instance of Individual class
            child = Individual(self.params)
            child.giant_tour = child_route
            child.divided_routes = split(child, self.params)
            child.evaluate_individual()

            children.append(child)

        return children

    def add_individual(self, offspring: list) -> None:
        # calculating fields of that individual
        ...
        self.population.append(offspring)

    def select_survivors(self) -> None:
        pass

# distance_matrix = [
#     [0, 1, 5, 4, 20],
#     [1, 0, 8, 10, 15],
#     [5, 8, 0, 9, 10],
#     [4, 10, 9, 0, 11],
#     [20, 15, 10, 11, 0]
# ]
#
# demands = [0, 1, 3, 4, 34]
# params = Params(distance_matrix, 54, demands, 0)
# instance = Population(1000, 20, params)
# instance.generate_initial_population()
# print(len(instance.population))

# l1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# l2 = [0, 9, 8, 7, 6, 5, 4, 3, 2, 1]
#
# res = Population.crossover(l1, l2)
# print(res, len(res))