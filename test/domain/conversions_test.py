
import unittest
import sys
import os
from math import pi

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from domain.conversions import Conversions


class ConversionsTest(unittest.TestCase, Conversions):

    def setUp(self):
        pass

    def test_ml_2_kilolitre(self):
        self.assertEquals(self.ml_2_kilolitre(1),       0.000001)
        self.assertEquals(self.ml_2_kilolitre(1000),    0.001)
        self.assertEquals(self.ml_2_kilolitre(1000000), 1)

    def test_cubic_mm_2_cubic_meters(self):
        self.assertAlmostEquals(self.cubic_mm_2_cubic_meters(1),       0.000000001)
        self.assertAlmostEquals(self.cubic_mm_2_cubic_meters(1000),    0.000001)
        self.assertAlmostEquals(self.cubic_mm_2_cubic_meters(1000000), 0.001)

    def test_cubic_mm_2_cubic_cm(self):
        self.assertAlmostEquals(self.cubic_mm_2_cubic_cm(1),       0.001)
        self.assertAlmostEquals(self.cubic_mm_2_cubic_cm(1000),    1.0)
        self.assertAlmostEquals(self.cubic_mm_2_cubic_cm(1000000), 1000.0)


if __name__ == '__main__':
    unittest.main()