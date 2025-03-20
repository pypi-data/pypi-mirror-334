import unittest
from my_package_testo098 import multiply, divide


class TestModule2(unittest.TestCase):
    def test_multiply(self):
        self.assertEquals(multiply(2, 4), 8)
        self.assertEquals(multiply(5, 8), 40)

    def test_divide(self):
        self.assertEquals(divide(8, 4), 2)
        self.assertEquals(divide(24, 6), 4)


if __name__ == '__main__':
    unittest.main()
