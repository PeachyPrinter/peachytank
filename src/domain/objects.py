

class Tank(object):
    shapes = ['Cylinder', 'Box']

    def __init__(
        self,
        height_mm,
        material_thickness_mm,
        inside_radius_mm,
        shape,
    ):
        self.height_mm = float(height_mm)
        self.material_thickness_mm = float(material_thickness_mm)
        self.inside_radius_mm = float(inside_radius_mm)
        if shape in self.shapes:
            self.shape = shape
        else:
            raise Exception("Unacceptable Shape Must be: %s" % ",".join(self.shapes))

    @property
    def outside_radius_mm(self):
        return self.inside_radius_mm + self.material_thickness_mm

    def get_scaled(self, max_size):
        max_detail = max(self.height_mm, self.inside_radius_mm + self.material_thickness_mm)
        return Tank(
            (self.height_mm / max_detail) * max_size,
            (self.material_thickness_mm / max_detail) * max_size,
            (self.inside_radius_mm / max_detail) * max_size,
            self.shape
            )