import csv

import pandas as pd

from src.modules.package import Package
from src.modules.hashtable import HashTable
from src.modules.matrix import Matrix
from src.modules.ACO import ACO

def main():
    packages = []
    #Instantiate hashtable
    hashtable = HashTable(get_rows('./resources/Packages.csv', packages))

    #Add packages to the hashtable
    hashtable.add_packages(packages)

    #Create the distance matrix
    distance_matrix = Matrix('./resources/Distances.csv')
    headers = pd.read_csv('./resources/Distances.csv', index_col=0).columns.tolist()
    package_to_hub = create_package_to_hub_mapping(packages, headers)

    aco = ACO(num_ants=10, num_packages=len(packages), distances=distance_matrix.matrix, package_to_hub=package_to_hub, packages=packages)
    aco.load_packages(hashtable.hashtable)

    best_solution, best_cost = aco.run(iterations=100, packages=packages)

    print(f"Best solution: {best_solution}")
    print(f"Best cost: {best_cost}")

def get_rows(csvfile, packages) -> int:
    i = 0
    #Read through the package file and create a list of Packages to be added to the hashtable, also get the size iterating through the rows for the hashtable
    with open(csvfile) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            package = Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], "At the hub")
            packages.append(package)
            i += 1

        return i

def create_package_to_hub_mapping(packages, hubs):
    package_to_hub = {}
    for package in packages:
        for index, hub in enumerate(hubs):
            hub_address = hub.split('\n')[1].strip()
            if hub_address == package.address:
                package_to_hub[package.ID] = index
                break
    return package_to_hub

if __name__ == '__main__':
    main()
