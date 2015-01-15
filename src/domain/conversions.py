
class Conversions(object):
    _cubic_mm_2_cubic_cm = 0.001
    _cubic_mm_2_cubic_meters = 0.000000001
    ml_to_kilolitre = 0.000001

    def cubic_mm_2_cubic_meters(self, mm3):
        return mm3 * self._cubic_mm_2_cubic_meters

    def ml_2_kilolitre(self, ml):
        return ml * self.ml_to_kilolitre

    def cubic_mm_2_cubic_cm(self, mm3):
        return mm3 * self._cubic_mm_2_cubic_cm
