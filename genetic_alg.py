from local_search import local_search
from split import split
from individual import Individual


class GeneticAlg:
    def __init__(self, max_iter: int, max_population_size: int):
        # algorithm parameters
        self.max_iter = max_iter
        self.max_population_size = max_population_size
        ...
        self.population: list = []

    def generate_initial_population(self) -> list:
        pass

    # generating an offspring
    def crossover(self, parent_1: list, parent_2: list) -> list:
        pass

    def select_parents(self) -> (list, list):
        pass

    def add_individual(self, offspring: list) -> None:
        # calculating fields of that individual
        ...
        self.population.append(offspring)

    def select_survivors(self) -> None:
        pass

    def run(self) -> None:
        self.population = self.generate_initial_population()
        for i in range(self.max_iter):
            parent_1, parent_2 = self.select_parents()
            offspring = self.crossover(parent_1, parent_2)
            offspring = local_search(offspring)
            self.add_individual(offspring)
            if len(self.population) == self.max_population_size:
                self.select_survivors()
        min_cost = 10e10
        best_solution: Individual
        for solution in self.population:
            if solution.cost < min_cost:
                min_cost = solution.cost
                best_solution = solution

        # printing best solution



