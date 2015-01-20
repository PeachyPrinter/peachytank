from math import pi, atan, tan
from conversions import Conversions


class Tank(Conversions):
    shapes = ['Cylinder', 'Box']

    def __init__(
        self,
        height_mm,
        material_thickness_mm,
        inside_radius_mm,
        fluid_density_kg_per_m3,
        shape,
    ):
        self._height_mm = float(height_mm)
        self._material_thickness_mm = float(material_thickness_mm)
        self._inside_radius_mm = float(inside_radius_mm)
        self._fluid_density_kg_per_m3 = fluid_density_kg_per_m3
        if shape in self.shapes:
            self._shape = shape
        else:
            raise Exception("Unacceptable shape %s must be: %s" % (shape, ",".join(self.shapes)))

    @property
    def outside_radius_mm(self):
        return self._inside_radius_mm + self._material_thickness_mm

    @property
    def inside_radius_mm(self):
        return self._inside_radius_mm

    @property
    def inside_circumference_mm(self):
        if self._shape == 'Cylinder':
            return pi * self._inside_radius_mm * 2
        elif self._shape == 'Box':
            return self.inside_diameter_mm * 4
        else:
            raise Exception("Unknown Shape")

    @property
    def inside_diameter_mm(self):
        return self._inside_radius_mm * 2

    @property
    def height_mm(self):
        return self._height_mm

    @property
    def shape(self):
        return self._shape

    @property
    def material_thickness_mm(self):
        return self._material_thickness_mm

    @property
    def volume_ml(self):
        if self._shape == 'Cylinder':
            volume_mm3 = pi * pow(self._inside_radius_mm, 2) * self._height_mm
            return self.cubic_mm_2_cubic_cm(volume_mm3)
        elif self._shape == 'Box':
            volume_mm3 = pow(self.inside_diameter_mm, 2) * self._height_mm
            return self.cubic_mm_2_cubic_cm(volume_mm3)
        else:
            raise Exception("Unknown Shape")

    @property
    def volume_kilolitre(self):
        return self.ml_to_kilolitre(self.volume_ml)

    @property
    def weight_kg(self):
        return self.volume_kilolitre * self._fluid_density_kg_per_m3

    def get_scaled(self, scale):
        return Tank(
            self._height_mm * scale,
            self.material_thickness_mm * scale,
            self._inside_radius_mm * scale,
            self._fluid_density_kg_per_m3,
            self.shape
            )


class Printer(object):
    def __init__(self, height_mm, projection_distance, projection_radius, projection_shape, relitive_size=1.0):
        self._height_mm = float(height_mm)
        self._projection_shape = projection_shape
        self._projection_distance = float(projection_distance)
        self._projection_radius = float(projection_radius)
        self._relitive_size = relitive_size

    @property
    def height_mm(self):
        return self._height_mm

    @property
    def relitive_size(self):
        return self._relitive_size

    @property
    def deflection(self):
        return atan(self._projection_radius / self._projection_distance)

    @property
    def radius_at_base(self):
        return tan(self.deflection) * self._height_mm

    @property
    def projection_shape(self):
        return self._projection_shape

    def dpi(self, height):
        return 0

    def get_scaled(self, scale):
        return Printer(
            self._height_mm * scale,
            self._projection_distance * scale,
            self._projection_radius * scale,
            self._projection_shape,
            relitive_size=self._relitive_size * scale
            )


class PeachySetup(object):
    def __init__(self, tank, printer,):
        self._tank = tank
        self._printer = printer

    @property
    def tank(self):
        return self._tank

    @property
    def printer(self):
        return self._printer

    def get_scaled_to_fit(self, max_size):
        max_detail = max(
            self._tank.height_mm,
            self._tank.inside_radius_mm + self._tank.material_thickness_mm,
            self._printer.height_mm)
        ratio = max_size / max_detail
        return PeachySetup(self._tank.get_scaled(ratio), self._printer.get_scaled(ratio))
