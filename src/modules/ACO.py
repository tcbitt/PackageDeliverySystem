import random
from datetime import datetime
from src.modules.truck import Truck
from src.modules.ant import Ant

class ACO:
    def __init__(self, num_ants, num_packages, distances, package_to_hub, packages, alpha=1.0, beta=2.0, evap_rate=0.5, q=10):
        self.num_ants = num_ants
        self.num_packages = num_packages
        self.distances = distances
        self.package_to_hub = package_to_hub
        self.alpha = alpha
        self.beta = beta
        self.evap_rate = evap_rate
        self.q = q
        self.pheromones = [[1.0 for _ in range(self.num_packages)] for _ in range(self.num_packages)]
        self.trucks = [Truck(i, driver=(i % 2)) for i in range(3)]

    def load_packages(self, packages):
        package_list = packages
        for truck in self.trucks:
            while package_list and len(truck.packages) < 16:
                truck.add_package(package_list.pop(0))

    def update_package_address(self, package_id, new_address):
        for truck in self.trucks:
            for package in truck.packages:
                if package.id == package_id:
                    package.address = new_address

    def run(self, iterations, packages):
        best_solution = None
        best_cost = float('inf')
        address_update_time = datetime.strptime("10:20", "%H:%M")

        for _ in range(iterations):
            current_time = self.trucks[0].departure_time
            if current_time >= address_update_time:
                self.update_package_address(9, "410 S. State St., Salt Lake City, UT 84111")

            solutions = []
            for _ in range(self.num_ants):
                ant = Ant(self.num_packages)
                solution = self.construct_solution(ant, packages)
                cost = ant.calculate_distance(self.distances)
                solutions.append((ant.path, cost))

                if cost < best_cost:
                    best_solution = ant.path
                    best_cost = cost

            self.update_pheromones(solutions)

        return best_solution, best_cost

    def construct_solution(self, ant, packages):
        solution = []
        visited = [False] * self.num_packages

        for _ in range(self.num_packages):
            next_package_index = self.choose_next_package(solution, visited)
            if next_package_index is None:
                raise ValueError("next_package_index is None")
            package = packages[next_package_index]
            hub_index = self.package_to_hub[package.ID]
            ant.visit_package(hub_index, self.distances)
            visited[next_package_index] = True
            solution.append(package)

        return solution

    def choose_next_package(self, solution, visited):
        current_package = solution[-1] if solution else None
        current_package_index = int(current_package.ID) if current_package else -1
        probabilities = []

        print(f"current_package_index: {current_package_index}")
        print(f"pheromones dimensions: {len(self.pheromones)}x{len(self.pheromones[0])}")
        print(f"distances dimensions: {len(self.distances)}x{len(self.distances[0])}")

        for i in range(self.num_packages):
            if not visited[i]:
                if current_package_index == -1:
                    tau = 1.0
                    eta = 1.0
                else:
                    if 0 <= current_package_index < len(self.pheromones) and 0 <= i < len(
                            self.pheromones[current_package_index]):
                        tau = self.pheromones[current_package_index][i]
                        if 0 <= current_package_index < len(self.distances) and 0 <= i < len(
                                self.distances[current_package_index]):
                            if self.distances[current_package_index][i] != 0:
                                eta = 1.0 / self.distances[current_package_index][i]
                            else:
                                eta = float('inf')  # Assign a large value if distance is zero
                            print(f"tau: {tau}, eta: {eta}, i: {i}")
                        else:
                            raise IndexError(
                                f"distances Index out of range: current_package_index={current_package_index}, i={i}")
                    else:
                        raise IndexError(
                            f"pheromones Index out of range: current_package_index={current_package_index}, i={i}")

                probabilities.append((tau ** self.alpha) * (eta ** self.beta))
            else:
                probabilities.append(0)

        sum_probabilities = sum(probabilities)
        if sum_probabilities == 0:
            return random.choice([i for i, v in enumerate(visited) if not v])

        probabilities = [p / sum_probabilities for p in probabilities]
        chosen_index = random.choices(range(self.num_packages), probabilities)[0]

        if chosen_index < 0 or chosen_index >= self.num_packages:
            raise ValueError(f"Chosen index {chosen_index} is out of the valid range.")

        print(f"Chosen package index: {chosen_index}")

        return chosen_index

    def update_pheromones(self, solutions):
        for i in range(len(self.pheromones)):
            for j in range(len(self.pheromones[i])):
                self.pheromones[i][j] *= (1 - self.evap_rate)

        for solution, cost in solutions:
            for i in range(len(solution) - 1):
                self.pheromones[solution[i]][solution[i + 1]] += self.q