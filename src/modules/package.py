class Package:
    def __init__(self, pkg_id, address, city, state, zip_code, deadline, weight_kg, notes, status):
        self.ID = pkg_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight_kg = weight_kg
        self.notes = notes
        self.status = status

    def print_info(self):
        print(f"Package ID: {self.ID}\n"
              f"Delivery Address: "f"{self.address}\n"
              f"City: {self.city}\n"
              f"Zip Code: {self.zip_code}\n"
              f"Deadline: {self.deadline}\n"
              f"Weight (KG): {self.weight_kg}\n"
              f"Notes: {self.notes}\n"
              f"Status: {self.status}")

