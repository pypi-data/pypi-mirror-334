from .base import Unit, ConverstionFactor

class DensityUnit(Unit):
    default_unit = "kg_m3"
    _conversion_factors = {
        "kg_m3": ConverstionFactor(1, 0),         # килограмм на кубический метр (базовая единица)
        "g_cm3": ConverstionFactor(1000, 0),      # грамм на кубический сантиметр
        "g_ml": ConverstionFactor(1000, 0),       # грамм на миллилитр
        "g_l": ConverstionFactor(1, 0),           # грамм на литр
        "kg_l": ConverstionFactor(1000, 0),       # килограмм на литр
        "lb_ft3": ConverstionFactor(16.0185, 0),  # фунт на кубический фут
        "lb_gal": ConverstionFactor(119.826, 0),  # фунт на галлон (US)
    } 