from math import pi
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
            raise Exception("Unacceptable Shape Must be: %s" % ",".join(self.shapes))

    @property
    def outside_radius_mm(self):
        return self._inside_radius_mm + self._material_thickness_mm

    @property
    def inside_radius_mm(self):
        return self._inside_radius_mm

    @property
    def inside_circumference_mm(self):
        return pi * self._inside_radius_mm * 2

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
        volume_mm3 = pi * pow(self._inside_radius_mm, 2) * self._height_mm
        return self.cubic_mm_2_cubic_cm(volume_mm3)

    @property
    def volume_kilolitre(self):
        return self.ml_to_kilolitre(self.volume_ml)

    @property
    def weight_kg(self):
        return self.volume_kilolitre * self._fluid_density_kg_per_m3

    def get_scaled(self, max_size):
        max_detail = max(self._height_mm, self._inside_radius_mm + self._material_thickness_mm)
        return Tank(
            (self._height_mm / max_detail) * max_size,
            (self.material_thickness_mm / max_detail) * max_size,
            (self._inside_radius_mm / max_detail) * max_size,
            self._fluid_density_kg_per_m3,
            self.shape
            )