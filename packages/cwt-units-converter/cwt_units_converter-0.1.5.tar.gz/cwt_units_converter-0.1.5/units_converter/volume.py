from .base import Unit, ConverstionFactor

class VolumeUnit(Unit):
    default_unit = "m3"
    _conversion_factors = {
        "m3": ConverstionFactor(1, 0),           # кубический метр (базовая единица)
        "cm3": ConverstionFactor(1e-6, 0),       # кубический сантиметр
        "mm3": ConverstionFactor(1e-9, 0),       # кубический миллиметр
        "l": ConverstionFactor(0.001, 0),        # литр
        "ml": ConverstionFactor(1e-6, 0),        # миллилитр
        "gal": ConverstionFactor(0.00378541, 0), # галлон (US)
        "qt": ConverstionFactor(0.000946353, 0), # кварта (US)
        "pt": ConverstionFactor(0.000473176, 0), # пинта (US)
        "fl_oz": ConverstionFactor(2.95735e-5, 0) # жидкая унция (US)
    } 