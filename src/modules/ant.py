class Ant:
    def __init__(self, num_packages):
        self.num_packages = num_packages
        self.path = []
        self.distance = 0

    def visit_package(self, package, distances):
        package = int(package)
        if self.path:
            last_package = int(self.path[-1])

            print(f"Visiting package: {package}, Last package: {last_package}")

            self.distance += distances[last_package][package]
        self.path.append(package)

    def clear(self):
        self.path = []
        self.distance = 0

    def calculate_distance(self, distances):
        total_distance = 0
        for i in range(len(self.path) - 1):
            total_distance += distances[int(self.path[i])][int(self.path[i + 1])]
        self.distance = total_distance
        return total_distance
