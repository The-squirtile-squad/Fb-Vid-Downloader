import unittest
from unittest import TestCase


class Testing(unittest, TestCase):
    def test_login(self):
        a = 'oopsie'
        b = 'oopsie'
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()