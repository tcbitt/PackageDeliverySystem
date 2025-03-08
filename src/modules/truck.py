from datetime import datetime

class Truck:
    def __init__(self, truck_id, driver):
        self.id = truck_id
        self.driver = driver
        self.packages = []
        self.current_route = []
        self.departure_time = datetime.strptime("08:00", "%H:%M")

    def add_package(self, package):
        if len(self.packages) < 16:
            self.packages.append(package)
        else:
            raise ValueError("Truck can only carry a maximum of 16 packages.")