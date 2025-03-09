import random
import math

from datetime import datetime, timedelta
from src.modules.truck import Truck

class SimulatedAnnealing:
    def __init__(self, distances, headers, initial_temp=100.0, cooling_rate=0.99, min_temp=1e-3, max_iterations=1000):
        self.distances = distances
        self.headers = headers
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp
        self.max_iterations = max_iterations

    def cost(self, trucks):
        total_distance = 0
        for truck in trucks:
            address_groups = {}
            for package in truck.packages:
                address = package.address
                if address not in address_groups:
                    address_groups[address] = []
                address_groups[address].append(package)

            addresses = list(address_groups.keys())
            for i in range(len(addresses) - 1):
                id1 = addresses[i]
                id2 = addresses[i + 1]

                # Get the index for the addresses
                index1 = self.headers.index(id1)
                index2 = self.headers.index(id2)
                total_distance += self.distances[index1][index2]

        return total_distance

    def generate_neighbor(self, trucks):
        new_trucks = [Truck(truck.id, truck.driver) for truck in trucks]
        all_packages = [package for truck in trucks for package in truck.packages]
        random.shuffle(all_packages)

        package_index = 0
        for truck in new_trucks:
            while package_index < len(all_packages) and len(truck.packages) < 16:
                truck.add_package(all_packages[package_index])
                package_index += 1

        return new_trucks

    def run(self, trucks, address_update_time):
        current_solution = trucks
        best_solution = [Truck(truck.id, truck.driver) for truck in trucks]
        best_cost = self.cost(current_solution)
        current_temp = self.initial_temp
        current_time = datetime.strptime("08:00", "%H:%M")

        for i in range(self.max_iterations):
            if current_temp < self.min_temp:
                break

            new_solution = self.generate_neighbor(current_solution)
            delta_e = self.cost(new_solution) - self.cost(current_solution)

            if delta_e < 0 or random.random() < math.exp(-delta_e / current_temp):
                current_solution = new_solution

                if self.cost(new_solution) < best_cost:
                    best_solution = new_solution
                    best_cost = self.cost(new_solution)

            current_temp *= self.cooling_rate

            # Check for address update
            if current_time >= address_update_time:
                for truck in best_solution:
                    for package in truck.packages:
                        if package.ID == '9':
                            package.address = "410 S. State St., Salt Lake City, UT 84111"

            current_time += timedelta(minutes=1)  # Increment time (example)

        return best_solution, best_cost
