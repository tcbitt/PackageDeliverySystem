from src.modules.package import Package

class HashTable:
    def __init__(self, size):
        self.size = size
        self.hashtable = [[] for _ in range(size)]

    def hashing(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        insert_index = self.hashing(key)

        if not self.hashtable[insert_index]:
            self.hashtable[insert_index] = [(key, value)]
        else:
            for index, key_value in enumerate(self.hashtable[insert_index]):
                ref_key, ref_val = key_value
                if key == ref_key:
                    self.hashtable[insert_index][index] = (key, value)
                    break
            else:
                self.hashtable[insert_index].append((key, value))

    def remove(self, key):
        remove_index = self.hashing(key)
        if self.hashtable[remove_index]:
            for index, key_value in enumerate(self.hashtable[remove_index]):
                ref_key, ref_val = key_value
                if key == ref_key:
                    del self.hashtable[remove_index][index]
                    return True
        return False

    def search(self, key):
        search_index = self.hashing(key)
        if self.hashtable[search_index] is not None:
            for ref_key, ref_val in self.hashtable[search_index]:
                if key == ref_key:
                    return ref_val
        return None

    #__getitem__ to be able to use the subscript operator for unit tests
    def __getitem__(self, key):
        return self.search(key)

    def add_packages(self, packages):
        for package in packages:
            self.insert(package.ID, package)