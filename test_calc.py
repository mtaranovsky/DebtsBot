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

    def test_mul(self):
        self.assertEqual(Calc.Calc.mul(self, 2, 5), 10)

    def test_div(self):
        self.assertEqual(Calc.Calc.div(self, 8, 4), 2)

    def test_mod(self):
        self.assertEqual(Calc.Calc.mod(self, 16, 5), 1)

    def test_pow(self):
        self.assertEqual(Calc.Calc.pow(self, 2, 5), 32)



if __name__ == '__main__':
    unittest.main()
