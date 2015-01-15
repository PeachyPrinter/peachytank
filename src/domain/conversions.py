
class Conversions(object):
    _cubic_mm_2_cubic_cm = 0.001
    _cubic_mm_2_cubic_meters = 0.000000001
    _ml_to_kilolitre = 0.000001

    def cubic_mm_2_cubic_meters(self, mm3):
        return mm3 * self._cubic_mm_2_cubic_meters

    def cubic_mm_2_cubic_cm(self, mm3):
        return mm3 * self._cubic_mm_2_cubic_cm

    def ml_to_um(self, ml):
        return ml * 1000

    def ml_to_litre(self, ml):
        return ml * 0.001

    def ml_to_kilolitre(self, ml):
        return ml * self._ml_to_kilolitre

    def ml_to_best_unit(self, ml):
        if ml < 1.0:
            return(self.ml_to_um(ml), u'\u03BCl')
        elif ml < 1000:
            return(ml, u'ml')
        elif ml < 1000000:
            return(self.ml_to_litre(ml), u'l')
        else:
            return(self.ml_to_kilolitre(ml), u'kl')

    def mm_to_um(self, mm):
        return mm * 10

    def mm_to_cm(self, mm):
        return mm * 0.1

    def mm_to_m(self, mm):
        return mm * 0.001

    def mm_to_best_unit(self, mm):
        if mm < 1.0:
            return(self.mm_to_um(mm), u'\u03BCm')
        elif mm < 10:
            return(mm, u'mm')
        elif mm < 1000:
            return(self.mm_to_cm(mm), u'cm')
        else:
            return(self.mm_to_m(mm), u'm')
