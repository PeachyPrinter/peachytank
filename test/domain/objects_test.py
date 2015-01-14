
import unittest
import sys
import os
from mock import patch
import numpy
from math import pi

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from domain.objects import Tank


class TankTest(unittest.TestCase):
    def test_init_should_set_basic_info(self):
        height_mm = 100
        material_thickness_mm = 3
        inside_radius_mm = 120
        shape = 'Cylinder'

        tank = Tank(height_mm, material_thickness_mm, inside_radius_mm, shape)

        self.assertEquals(height_mm, tank.height_mm)
        self.assertEquals(material_thickness_mm, tank.material_thickness_mm)
        self.assertEquals(inside_radius_mm, tank.inside_radius_mm)
        self.assertEquals(shape, tank.shape)

    def test_init_should_calculate_outside_radius(self):
        height_mm = 100
        material_thickness_mm = 3
        inside_radius_mm = 120
        shape = 'Cylinder'

        tank = Tank(height_mm, material_thickness_mm, inside_radius_mm, shape)

        self.assertEquals(inside_radius_mm + material_thickness_mm, tank.outside_radius_mm)


    def test_init_should_raise_exceptions_for_unsupported_shape(self):
        height_mm = 100
        material_thickness_mm = 3
        inside_radius_mm = 120

        with self.assertRaises(Exception):
            Tank(height_mm, material_thickness_mm, inside_radius_mm, 'Beer')

        Tank(height_mm, material_thickness_mm, inside_radius_mm, 'Cylinder')
        Tank(height_mm, material_thickness_mm, inside_radius_mm, 'Box')

    def test_volume_l_should_be_calculated_correctly_for_cylinder(self):
        height_mm = 100
        material_thickness_mm = 3
        inside_radius_mm = 10
        shape = 'Cylinder'
        expected_volume = pi * pow(inside_radius_mm, 2.0) * height_mm

        tank = Tank(height_mm, material_thickness_mm, inside_radius_mm, shape)

        self.assertAlmostEquals(expected_volume, tank.volume_ml)

if __name__ == '__main__':
    unittest.main()