from domain.objects import *


class TestHelpers(object):
    def get_tank(
            self,
            height_mm=100.0,
            material_thickness_mm=3.0,
            inside_radius_mm=100.0,
            fluid_density_kg_per_m3=9997.0,
            shape="Cylinder"
            ):
        return Tank(height_mm, material_thickness_mm, inside_radius_mm, fluid_density_kg_per_m3, shape)
