from .base import Unit, ConverstionFactor

class TimeUnit(Unit):
    default_unit = "s"
    _conversion_factors = {
        "s": ConverstionFactor(1, 0),
        "min": ConverstionFactor(60, 0),
        "h": ConverstionFactor(3600, 0),
        "d": ConverstionFactor(86400, 0),
        "y": ConverstionFactor(31536000, 0),
        "w": ConverstionFactor(604800, 0),
    }
    

