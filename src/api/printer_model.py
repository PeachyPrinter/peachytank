from domain.conversions import Conversions


class PrinterModelApi(Conversions):
    def __init__(self):
        self._tank = None

    def set_tank(self, tank):
        self._tank = tank

    def get_tank_info(self):
        if self._tank:
            return {
            'Inside Radius': self.mm_to_best_unit(self._tank.inside_radius_mm),
            'Outside Radius': self.mm_to_best_unit(self._tank.outside_radius_mm),
            'Height': self.mm_to_best_unit(self._tank.height_mm),
            'Material Thickness': self.mm_to_best_unit(self._tank.material_thickness_mm),
            'Inside Diameter': self.mm_to_best_unit(self._tank.inside_diameter_mm),
            'Inside Circumfrence': self.mm_to_best_unit(self._tank.inside_circumference_mm),
            'Shape': (self._tank.shape, ''),
            'Volume': self.ml_to_best_unit(self._tank.volume_ml),
            'Fluid Density': (self._tank._fluid_density_kg_per_m3, u'kg/m\u00B3'),
            'Weight': (self._tank.weight_kg, 'kg'),
            }
        else:
            return {}

    def getPrinterInfo(self):
        return {
            'DPI': '1234.312',
            'Deflection': '45 degrees',
            'Height': '12 Lbs',
            }
