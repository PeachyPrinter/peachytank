# Resolution Calculator
from math import pi, tan, atan
import numpy as np


class PeachyCalculator(object):
    def __init__(self, depth, in_low_amplitude, in_high_amplitude, print_area_height):
        self._linear_posisitions = self._possible_linear_posisitions(depth, in_low_amplitude, in_high_amplitude)
        self._print_area_height = print_area_height

    def _possible_linear_posisitions(self, depth, in_low_amplitude, in_high_amplitude):
        positions = pow(2, 16)
        percentage_of_amplitude = 1.0 - in_high_amplitude - in_low_amplitude
        usable_positions = (positions / 2) * percentage_of_amplitude
        return usable_positions

    def possible_linear_posisitions(self):
        return self._linear_posisitions

    def print_area_width(self, height_of_printer, deflection):
        distance_to_print_area = height_of_printer - self._print_area_height
        theta = deflection / 2
        half_width = tan(theta) * distance_to_print_area
        width = half_width * 2.0
        return width

    def required_deflection(self, height_of_printer, width):
        distance_to_print_area = height_of_printer - self._print_area_height
        half_width = width / 2.0
        deflection = atan(half_width/distance_to_print_area) * 2
        return deflection

    def pos_at_height(self, height, deflection, width):
        theta = deflection / 2.0
        half_width = width / 2.0
        tri_height = self._print_area_height - height
        over_hang = tan(theta) * tri_height
        usable_percent = 1.0 - (over_hang / (half_width + over_hang))
        linear_pos_per_mm = (self._linear_posisitions * usable_percent) / width
        return linear_pos_per_mm

    def resolutions_at_heights(self, height_of_mirror, width_of_print_area):
        deflection = self.required_deflection(height_of_mirror, width_of_print_area)
        print("Deflection %2f" % (deflection / (pi / 180)))
        heights = np.linspace(0.0, self._print_area_height)
        return [(height, pow(self.pos_at_height(height, deflection, width_of_print_area), 2)) for height in heights]


def dpmm2dpi(value):
    return value / 0.0393700787401575


def convert(values):
    return [(h, dpmm2dpi(dpmm)) for (h, dpmm) in values]


if __name__ == '__main__':
    in_depth = 16
    in_low_amplitude = 0.25
    in_high_amplitude = 0.05

    print_area_mm = 700
    print_area_height = 1800


    pc = PeachyCalculator(in_depth, in_low_amplitude, in_high_amplitude, print_area_height)
    positions = pc.possible_linear_posisitions()
    mega_pixels = pow(positions, 2) / 1000000

    print("{0:7,.0f} Posisitions per axis".format(positions))
    print("{0:7,.0f} Mega Pixels".format(mega_pixels))

    deflection_min_rad = pi / 16  #11.25 degrees
    deflection_max_rad = pi / 4  #45 degrees

    # deflections = np.linspace(deflection_min_rad, deflection_max_rad)
    # for deflect in deflections:
    #     print("{0:.2f}\xc2\xb0 : {1:.0f} mm".format((deflect / (pi / 180)), pc.print_area_width(print_area_height + 200.0, deflect)))

    # heights = np.linspace(1000.0, 2000.0)
    # for height in heights:
    #     height_from_base = print_area_height + height
    #     deflection = pc.required_deflection(height_from_base, print_area_mm)
    #     print("{0:.0f} mm : {1:.2f}\xc2\xb0  ".format(height_from_base, (deflection / (pi / 180)), ))

    print("PrintArea : %s" % print_area_height)
    print("PrintWidth : %s" % print_area_mm)
    result = pc.resolutions_at_heights(2540, print_area_mm)
    resolutions = convert(result)
    for resolution in resolutions:
        print("{0:6,.0f} mm {1:8,.0f} dpi".format(*resolution))