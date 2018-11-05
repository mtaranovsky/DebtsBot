import unittest
import Calc


class CalcTest(unittest.TestCase):
    def test_add(self):
        self.assertEqual(Calc.Calc.add(self, 1, 2), 3)

    def test_sub(self):
        self.assertEqual(Calc.Calc.sub(self, 4, 2), 2)

    def test_mul(self):
        self.assertEqual(Calc.Calc.mul(self, 2, 5), 10)

    def test_div(self):
        self.assertEqual(Calc.Calc.div(self, 8, 2), 4)




if __name__ == '__main__':
    unittest.main()
