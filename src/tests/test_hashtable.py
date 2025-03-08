import unittest
from src.modules.package import Package
from src.modules.hashtable import HashTable

#Unit tests to ensure the hashmap functions work correctly.
class TestHashTable(unittest.TestCase):

    def setUp(self):
        self.hash_table = HashTable(size=10)

    def test_insert(self):
        self.hash_table.insert("microsoft", 1)
        self.hash_table.insert("apple", 2)
        self.hash_table.insert("samsung", 3)

        self.assertEqual(self.hash_table["microsoft"], 1)
        self.assertEqual(self.hash_table["apple"], 2)
        self.assertEqual(self.hash_table["samsung"], 3)
        self.assertIsNone(self.hash_table["sony"])

    def test_search(self):
        self.hash_table.insert("microsoft", 1)
        self.hash_table.insert("apple", 2)
        self.hash_table.insert("samsung", 3)

        self.assertEqual(self.hash_table.search("microsoft"), 1)
        self.assertEqual(self.hash_table.search("apple"), 2)
        self.assertEqual(self.hash_table.search("samsung"), 3)
        self.assertEqual(self.hash_table.search("sony"), None)

    def test_delete(self):
        self.hash_table.insert("microsoft", 1)
        self.hash_table.insert("apple", 2)
        self.hash_table.insert("samsung", 3)

        self.assertTrue(self.hash_table.remove("apple"))
        self.assertFalse(self.hash_table.remove("apple"))
        self.assertTrue(self.hash_table.remove("samsung"))
        self.assertFalse(self.hash_table.remove("sony"))

    def test_add_packages(self):
        package1 = Package("1", "123 Test Drive", "State", "NY", "14444", "EOD", "10", "", "Pending")
        package2 = Package("5", "321 Test Drive", "State", "NY", "14434", "EOD", "10", "", "Pending")
        package3 = Package("7", "355 Test Drive", "State", "NY", "14445", "EOD", "10", "", "Pending")

        packages = [package1, package2, package3]

        self.hash_table.add_packages(packages)

        self.assertTrue(self.hash_table.search("1"))
        self.assertTrue(self.hash_table.remove("1"))
        self.assertFalse(self.hash_table.search("22"))
        self.assertNotEqual(self.hash_table.search("1"), self.hash_table.search("5"))

if __name__ == '__main__':
    unittest.main()