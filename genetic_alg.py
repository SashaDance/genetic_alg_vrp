from local_search import local_search
from split import split
from individual import Individual


class GeneticAlg:
    def __init__(self, max_iter: int, population_size: int,
                 params):
        # algorithm parameters
        self.max_iter = max_iter
        self.population_size = population_size
        ...
        self.population: list = []
        self.params = params

    def generate_initial_population(self) -> list[Individual]:
        population = []
        for i in range(self.population_size):
            indiv = Individual(self.params)
            indiv.random_init()
            indiv.divided_routes = split(indiv, self.params)
            indiv.evaluate_individual()

            population.append(indiv)

        return population

    def crossover(self, parent_1: Individual, parent_2: Individual) -> list:
        pass

    def select_parents(self) -> tuple[list, list]:
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



