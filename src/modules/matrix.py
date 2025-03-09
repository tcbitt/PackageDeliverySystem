import pandas as pd
import math
from tabulate import tabulate


class Matrix:
    def __init__(self, csvfile):
        table = pd.read_csv(csvfile, index_col=0)
        self.matrix = table.values.tolist()
        #Set NaN values top inf for the algorithm
        self.matrix = [[float('inf') if math.isnan(value) else value for value in row] for row in self.matrix]

    def __getitem__(self, index):
        return self.matrix[index]

    def print_matrix(self):
        print(tabulate(self.matrix, headers=self.matrix.columns, tablefmt='grid'))

