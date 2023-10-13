import pandas as pd
import numpy as np
import pickle

VEHICLE_CAPACITY = 54


class GetData:
    def __init__(self):
        self.sc_to_sc_distances = pd.read_csv('Data/sc_to_sc_updated.csv')
        self.ff_to_sc_distances = pd.read_csv('Data/ff_to_sc_updated.csv')
        self.sc_indices = dict()

        with open('Data/demands.pickle', 'rb') as f:
            self.demands_dict = pickle.load(f)

    def get_distance_matrix(self, ff: int) -> list[list]:
        sort_centers = self.demands_dict[ff].keys()
        # initializing the array with n + 1 rows
        # where n is number of sort centers and 1 is ff
        distance_matrix = np.zeros(
            shape=((len(sort_centers) + 1), (len(sort_centers) + 1))
        ).tolist()
        '''
        filling the distances from ff to sort centers 
        (first row and first column)
        '''
        for i, sc in enumerate(sort_centers):
            sc = str(sc)  # type of 'Код СЦ' column is object
            distance_matrix[0][i + 1] = self.ff_to_sc_distances[
                (self.ff_to_sc_distances['Код ФФ'] == ff)
                & (self.ff_to_sc_distances['Код СЦ'] == sc)
            ]['Distance'].values[0]
            distance_matrix[i + 1][0] = distance_matrix[0][i + 1]

        # filling the distances from sort center to sort center
        for i, sc1 in enumerate(sort_centers, start=1):
            for j, sc2 in enumerate(sort_centers, start=1):
                sc1 = str(sc1)  # type of 'Код СЦ' column is object
                sc2 = str(sc2)
                distance_matrix[i][j] = self.sc_to_sc_distances[
                    (self.sc_to_sc_distances['Код СЦ1'] == sc1)
                    & (self.sc_to_sc_distances['Код СЦ2'] == sc2)
                ]['Distance'].values[0]

        return distance_matrix

    def get_demands(self, ff: int) -> list:
        '''
        initializing the array with zero
        where zero is the demand for ff from ff
        '''

        demands = [0]

        for ind, item in enumerate(self.demands_dict[ff].items(), start=1):
            key, demand = item
            demands.append(demand)
            self.sc_indices[ind] = key

        return demands

    @staticmethod
    def print_matrix(matrix: list) -> None:

        if not all(isinstance(row, list) for row in matrix):
            raise ValueError("Input must be a 2D list (matrix).")

        max_element_length = max(
            len(str(element)) for row in matrix for element in row)

        for row in matrix:
            row_str = " | ".join(
                f"{element:>{max_element_length}}" for element in row)
            print("[" + row_str + "]")
