import unittest
import Calc


class CalcTest(unittest.TestCase):
    def test_add(self):
        self.assertEqual(Calc.Calc.add(self, 1, 2), 3)

    def test_sub(self):
        self.assertEqual(Calc.Calc.sub(self, 4, 2), 2)

if __name__ == '__main__':
    unittest.main()
