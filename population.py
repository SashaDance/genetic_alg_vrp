import random
from copy import deepcopy

from local_search import local_search
from split import split
from individual import Individual
from params import Params
from get_data import GetData



class Population:
    def __init__(self, params,
                 population_size: int,
                 elite_size: int,
                 mut_rate: float = 0.01):
        self.population_size = population_size
        self.population: dict[int, Individual] = {}
        self.elite_size = elite_size
        self.mut_rate = mut_rate
        self.params = params

    def generate_initial_population(self) -> None:
        """
        generating population with random giant tour
        :return:
        """
        for i in range(self.population_size):
            indiv = Individual(self.params)
            indiv.random_init()
            indiv.divided_routes = split(indiv, self.params)
            indiv.evaluate_individual()

            self.population[i] = indiv

    def rank_population(self) -> None:
        """
        sorting list by increasing of fitness
        :return:
        """
        self.population = dict(sorted(
            self.population.items(),
            key=lambda item: item[1]._fitness
        ))

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

        elite_ind = self.population_size- self.elite_size
        # saving indices of elite members of population
        selection_res = [
            key for key in list(self.population.keys())[elite_ind:]
        ]

        """
        selection of other members
        we need len(selection_res) to be = population_size, so do the i loop
        in each iteration of i loop there will be chosen one of indices, since
        probability of the last element (with the highest fitness score) is
        always 1
        """
        for i in range(elite_ind):
            rand_prob = random.random()
            for key in self.population.keys():
                if cum_sum_prob[key] >= rand_prob:
                    selection_res.append(key)
                    break

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
        other_nodes = [node for node in parent_2 if node not in slice_]

        child = (
                other_nodes[:first_cut_point] +
                slice_ +
                other_nodes[first_cut_point:]
        )

        return child

    def mutate(self, indiv: Individual) -> Individual:
        """
        this method implements mutation of individual
        with prob = mut_rate 2 nodes will be swapped in giant tour
        mutation is needed for exploration to avoid local extrema
        :param indiv:
        :param mut_rate: mutation rate
        :return: mutated individual
        """
        mut_indiv = deepcopy(indiv)
        for i in range(1, len(mut_indiv.giant_tour)):
            if random.random() < self.mut_rate:
                j = random.randint(1, len(mut_indiv.giant_tour) - 1)

                _ = mut_indiv.giant_tour[i]
                mut_indiv.giant_tour[i] = mut_indiv.giant_tour[j]
                mut_indiv.giant_tour[j] = _

        # updating divided routes
        mut_indiv.divided_routes = split(mut_indiv, self.params)

        return mut_indiv

    def produce_offspring(self,
                          selection_res: list[int]) -> dict[int, Individual]:

        # retain elite individuals from the current population
        offspring = [
            self.population[ind] for ind in selection_res[:self.elite_size]
        ]
        breeding_pool = random.sample(
            selection_res, len(selection_res) - self.elite_size
        )
        """
        you may think that there will be child duplicates, since from 
        i = len(breeding_pool) we won't get new pairs of parents, but
        we have crossover function which is stochastic, so
        there is no problems with that
        """
        for i in range(len(breeding_pool)):
            ind_1 = breeding_pool[i]
            ind_2 = breeding_pool[len(breeding_pool) - ind_1 - 1]
            parent_1_route = self.population[ind_1]
            parent_2_route = self.population[ind_2]
            child_route = Population.crossover(
                parent_1_route.giant_tour, parent_2_route.giant_tour
            )
            # creating new instance of Individual class
            child = Individual(self.params)
            child.giant_tour = child_route
            child.divided_routes = split(child, self.params)
            child.evaluate_individual()

            child = self.mutate(child)
            offspring.append(child)

        # creating dict of list
        offspring = dict(((i, offspring[i]) for i in range(len(offspring))))
        return offspring

# TODO: implement changing population size


if __name__ == '__main__':

    data = GetData(110)
    distance_matrix, demands, ind_to_sc_map = data.get_data()
    params = Params(distance_matrix, 54, demands, 0)
    instance = Population(params, 100, 10)
    instance.generate_initial_population()
    for i in range(200):
        print(i)
        instance.rank_population()
        selection_res = instance.selection()
        last_key = list(instance.population.keys())[-1]
        print(instance.population[last_key].cost)
        instance.population = instance.produce_offspring(selection_res)

    instance.rank_population()
    last_key = list(instance.population.keys())[-1]
    print(instance.population[last_key].cost)
    print(instance.population[last_key].giant_tour)


