from .base import Unit
from .base import ConverstionFactor

class FlowRateUnit(Unit):
    default_unit = "m3_h"
    _conversion_factors = {
            "m3_h": ConverstionFactor(1, 0),
            "l_h": ConverstionFactor(1/1000, 0),
            "m3_s": ConverstionFactor(3600, 0),
            "l_s": ConverstionFactor(3600/1000, 0),
            "gpm": ConverstionFactor(60/264.172, 0),
            "gph": ConverstionFactor(1/264.172, 0),   
            "cfm": ConverstionFactor(60/35.3147, 0),
        }