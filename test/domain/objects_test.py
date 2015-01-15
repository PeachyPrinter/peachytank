
import unittest
import sys
import os
from mock import patch
import numpy
from math import pi

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from domain.objects import Tank
from domain.conversions import Conversions


class TankTest(unittest.TestCase, Conversions):

    def setUp(self):
        pass

    def test_init_should_set_basic_info(self):
        height_mm = 100
        fluid_density = 1.0
        material_thickness_mm = 3
        inside_radius_mm = 120
        shape = 'Cylinder'

        tank = Tank(height_mm, material_thickness_mm, inside_radius_mm, fluid_density, shape)

        self.assertEquals(height_mm, tank.height_mm)
        self.assertEquals(material_thickness_mm, tank.material_thickness_mm)
        self.assertEquals(inside_radius_mm, tank.inside_radius_mm)
        self.assertEquals(inside_radius_mm, tank.inside_radius_mm)
        self.assertEquals(shape, tank.shape)

    def test_init_should_calculate_outside_radius(self):
        height_mm = 100
        fluid_density = 1.0
        material_thickness_mm = 3
        inside_radius_mm = 120
        shape = 'Cylinder'

        tank = Tank(height_mm, material_thickness_mm, inside_radius_mm, fluid_density, shape)

        self.assertEquals(inside_radius_mm + material_thickness_mm, tank.outside_radius_mm)

    def test_init_should_raise_exceptions_for_unsupported_shape(self):
        height_mm = 100
        fluid_density = 1.0
        material_thickness_mm = 3
        inside_radius_mm = 120

        with self.assertRaises(Exception):
            Tank(height_mm, material_thickness_mm, inside_radius_mm, fluid_density, 'Beer')

        Tank(height_mm, material_thickness_mm, inside_radius_mm, fluid_density, 'Cylinder')
        Tank(height_mm, material_thickness_mm, inside_radius_mm, fluid_density, 'Box')

    def test_volume_ml_should_be_calculated_correctly_for_cylinder(self):
        height_mm = 100
        fluid_density = 1.0
        material_thickness_mm = 3
        inside_radius_mm = 10
        shape = 'Cylinder'
        expected_area_mm3 = pi * pow(inside_radius_mm, 2.0) * height_mm
        expected_volume_ml = self.cubic_mm_2_cubic_cm(expected_area_mm3)

        tank = Tank(height_mm, material_thickness_mm, inside_radius_mm, fluid_density, shape)

        self.assertAlmostEquals(expected_volume_ml, tank.volume_ml)

    def test_inside_circumference_mm_should_be_calculated_for_cylinder(self):
        height_mm = 100
        fluid_density = 1.0
        material_thickness_mm = 3
        inside_radius_mm = 120
        shape = 'Cylinder'
        expected_inside_circumference_mm = pi * inside_radius_mm * 2

        tank = Tank(height_mm, material_thickness_mm, inside_radius_mm, fluid_density, shape)

        self.assertEquals(expected_inside_circumference_mm, tank.inside_circumference_mm)

    def test_inside_diameter_mm_should_be_calculated_for_cylinder(self):
        height_mm = 100
        fluid_density = 1.0
        material_thickness_mm = 3
        inside_radius_mm = 120
        shape = 'Cylinder'
        expected_inside_diameter_mm = inside_radius_mm * 2

        tank = Tank(height_mm, material_thickness_mm, inside_radius_mm, fluid_density, shape)

        self.assertEquals(expected_inside_diameter_mm, tank.inside_diameter_mm)

    def test_weight_kg_should_be_calculated_for_cylinder(self):
        height_mm = 100
        fluid_density = 1.0
        material_thickness_mm = 3
        inside_radius_mm = 120
        shape = 'Cylinder'
        expected_area_mm3 = pi * pow(inside_radius_mm, 2.0) * height_mm
        expected_area_meter3 = self.cubic_mm_2_cubic_meters(expected_area_mm3)
        expected_weight_kg = expected_area_meter3 * fluid_density

        tank = Tank(height_mm, material_thickness_mm, inside_radius_mm, fluid_density, shape)

        self.assertAlmostEquals(expected_weight_kg, tank.weight_kg)



if __name__ == '__main__':
    unittest.main()