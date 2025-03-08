import pandas as pd
from tabulate import tabulate


class Matrix:
    def __init__(self, csvfile):
        table = pd.read_csv(csvfile, index_col=0)
        self.matrix = table.values.tolist()

    def print_matrix(self):
        print(tabulate(self.matrix, headers=self.matrix.columns, tablefmt='grid'))
