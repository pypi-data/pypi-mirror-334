import unittest

from reStructuredText.example import add_one


class TestExample(unittest.TestCase):
    def test_add_one(self):
        self.assertEqual(add_one(3), 4)


if __name__ == '__main__':
    unittest.main()
