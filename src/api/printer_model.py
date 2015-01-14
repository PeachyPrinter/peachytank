class PrinterModelApi(object):
    def __init__(self):
        pass

    def getTankInfo(self):
        return {
            'Volume': '1234.312 Liters',
            'Weight': '123 Lbs',
            'Salt Weight': '12 Lbs',
            'Inside Diameter': '727 mm',
            'Outside Diameter': '730 mm',
            'Some Crap I made up t': '3 out of 4 nine',
            }

    def getPrinterInfo(self):
        return {
            'DPI': '1234.312',
            'Deflection': '45 degrees',
            'Height': '12 Lbs',

            }
