import csv
import pandas as pd

from datetime import datetime
from src.modules.truck import Truck
from src.modules.package import Package
from src.modules.hashtable import HashTable
from src.modules.matrix import Matrix
from src.modules.sim_anneal import  SimulatedAnnealing

def main():
    packages = []
    #Instantiate hashtable
    hashtable = HashTable(get_rows('./resources/Packages.csv', packages))

    #Add packages to the hashtable
    hashtable.add_packages(packages)

    #Create the distance matrix
    distance_matrix = Matrix('./resources/Distances.csv')

    #Get the headers and separate the hub name from the street address for the algorithm
    raw_headers = pd.read_csv('./resources/Distances.csv', index_col=0).columns.tolist()
    headers = [header.split('\n')[1].strip() for header in raw_headers]
    #package_to_hub = create_package_to_hub_mapping(packages, headers)

    # Initialize trucks and load packages
    trucks = [Truck(i, driver=(i % 2)) for i in range(3)]
    load_packages(trucks, packages)


    for truck in trucks:
        print(f"Truck {truck.id} initial packages: {[package.ID for package in truck.packages]}")
    print(f"Initial cost: {SimulatedAnnealing(distance_matrix, headers).cost(trucks)}")

    # Print the distance matrix for verification
    distance_matrix.print_matrix()

    # Run Simulated Annealing
    address_update_time = datetime.strptime("10:20", "%H:%M")
    sa = SimulatedAnnealing(distance_matrix, headers)

    solutions = []
    costs = []

    for _ in range(10):  # Run the algorithm 10 times
        best_solution, best_cost = sa.run(trucks, address_update_time)
        solutions.append(best_solution)
        costs.append(best_cost)
        print(f"Best solution: {[package.ID for truck in best_solution for package in truck.packages]}")
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


def load_packages(trucks, packages):
    delayed_packages = []
    special_truck_packages = {i: [] for i in range(len(trucks))}
    grouped_packages = {}

    #Process special notes for packages
    for package in packages:
        note = package.notes
        if "Can only be on truck" in note:
            truck_id = int(note.split()[-1]) - 1
            if len(special_truck_packages[truck_id]) < 16:
                special_truck_packages[truck_id].append(package)
            else:
                raise ValueError(f"Truck {truck_id + 1} can only carry a maximum of 16 packages.")
        elif "Delayed" in note:
            delayed_packages.append(package)
        elif "Must be delivered with" in note:
            group_ids = [int(id.strip()) for id in note.split("with")[-1].split(',')]
            group_ids.append(int(package.ID))
            group_ids.sort()
            group_id = tuple(group_ids)
            if group_id not in grouped_packages:
                grouped_packages[group_id] = []
            grouped_packages[group_id].append(package)

    #Assign grouped packages to the same truck
    for group_id, group_packages in grouped_packages.items():
        for truck in trucks:
            if len(truck.packages) + len(group_packages) <= 16:
                for package in group_packages:
                    truck.add_package(package)
                break
        else:
            raise ValueError(f"Group {group_id} exceeds truck capacity.")

    # Assign special truck packages first
    for truck_id, truck_packages in special_truck_packages.items():
        for package in truck_packages:
            if len(trucks[truck_id].packages) < 16:
                trucks[truck_id].add_package(package)
            else:
                raise ValueError(f"Truck {truck_id + 1} can only carry a maximum of 16 packages.")

    # Assign other packages to available trucks
    for package in packages:
        if package not in [pkg for truck in trucks for pkg in truck.packages]:
            for truck in trucks:
                if len(truck.packages) < 16:
                    truck.add_package(package)
                    break

if __name__ == '__main__':
    main()
