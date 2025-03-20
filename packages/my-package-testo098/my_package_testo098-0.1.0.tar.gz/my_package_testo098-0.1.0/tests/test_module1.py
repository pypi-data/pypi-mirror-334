import unittest
from my_package_testo098 import add, subtract


class TestModule1(unittest.TestCase):

    def test_add(self):
        self.assertEquals(add(3, 1), 4)
        self.assertEqual(add(-1, 1), 0)

    def test_subtract(self):
        self.assertEquals(subtract(5, 1), 4)
        self.assertEqual(subtract(2, 3), -1)


if __name__ == '__main__':
    unittest.main()
