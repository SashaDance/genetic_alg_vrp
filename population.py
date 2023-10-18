from local_search import local_search
from split import split
from individual import Individual


class Population:
    def __init__(self, population_size: int,
                 elite_size: int,
                 params):
        self.population_size = population_size
        ...
        self.population: list[Individual] = []
        self.elite_size = elite_size
        self.params = params

    def generate_initial_population(self) -> None:
        for i in range(self.population_size):
            indiv = Individual(self.params)
            indiv.random_init()
            indiv.divided_routes = split(indiv, self.params)
            indiv.evaluate_individual()

            self.population.append(indiv)

    def rank_population(self):
        # sorting list by descending of fitness
        self.population = sorted(
            self.population,
            key=lambda x: x._fitness,
            reverse=True
        )

    def selection(self) -> list[Individual]:
        selection_res = []

        return selection_res

    def crossover(self, parent_1: Individual, parent_2: Individual) -> list:
        pass

    def add_individual(self, offspring: list) -> None:
        # calculating fields of that individual
        ...
        self.population.append(offspring)

    def select_survivors(self) -> None:
        pass
