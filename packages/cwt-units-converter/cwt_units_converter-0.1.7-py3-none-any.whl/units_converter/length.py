from .base import Unit, ConverstionFactor

class LengthUnit(Unit):
    default_unit = "m"
    _conversion_factors = {
        "m": ConverstionFactor(1, 0),
        "km": ConverstionFactor(1000, 0),
        "cm": ConverstionFactor(0.01, 0),
        "mm": ConverstionFactor(0.001, 0),
        "um": ConverstionFactor(1e-6, 0),
        "nm": ConverstionFactor(1e-9, 0),
        "ft": ConverstionFactor(0.3048, 0),
        "in": ConverstionFactor(0.0254, 0),
        "mi": ConverstionFactor(1609.34, 0),
        "yd": ConverstionFactor(0.9144, 0),
        "ft": ConverstionFactor(0.3048, 0),
        "inch": ConverstionFactor(0.0254, 0),
    }

