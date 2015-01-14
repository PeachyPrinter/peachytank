from math import pi

class Tank(object):
    shapes = ['Cylinder', 'Box']

    def __init__(
        self,
        height_mm,
        material_thickness_mm,
        inside_radius_mm,
        shape,
    ):
        self._height_mm = float(height_mm)
        self._material_thickness_mm = float(material_thickness_mm)
        self._inside_radius_mm = float(inside_radius_mm)
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
        return pi * pow(self._inside_radius_mm, 2) * self._height_mm
    

    def get_scaled(self, max_size):
        max_detail = max(self._height_mm, self._inside_radius_mm + self._material_thickness_mm)
        return Tank(
            (self._height_mm / max_detail) * max_size,
            (self.material_thickness_mm / max_detail) * max_size,
            (self._inside_radius_mm / max_detail) * max_size,
            self.shape
            )