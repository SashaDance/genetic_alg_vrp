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
        ...
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
        pass

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