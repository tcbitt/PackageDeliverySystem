import unittest
from src.modules.package import Package

#Unit test to ensure package functions work correctly.
class TestPackage(unittest.TestCase):
    def setUp(self):
        self.package = Package(pkg_id=25, address="123 Test Lane", city="Test City", zip_code="12345-0111", deadline="2:30 PM", weight_kg=5, notes="Handle with care!", status="at the Hub")

    def test_print_func(self):
        self.assertEqual(self.package.ID, 25)
        self.assertEqual(self.package.address, "123 Test Lane")
        self.assertEqual(self.package.city, "Test City")
        self.assertEqual(self.package.zip_code, 12345)
        self.assertEqual(self.package.deadline, "2:30 PM")
        self.assertEqual(self.package.weight_kg, 5)
        self.assertEqual(self.package.notes, "Handle with care!")
        self.assertEqual(self.package.status, "at the Hub")
        self.package.print_info()