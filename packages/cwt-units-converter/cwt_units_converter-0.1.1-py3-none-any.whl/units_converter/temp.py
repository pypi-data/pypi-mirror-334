from .base import Unit, ConverstionFactor

class TemperatureUnit(Unit):
    default_unit = "K"
    _conversion_factors = {
        "K": ConverstionFactor(1, 0),
        "C": ConverstionFactor(1, 273.15),
        "F": ConverstionFactor(5/9, 255.372),
    }
