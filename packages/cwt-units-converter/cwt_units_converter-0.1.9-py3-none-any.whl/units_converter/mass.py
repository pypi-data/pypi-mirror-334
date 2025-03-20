from .base import Unit, ConverstionFactor

class MassUnit(Unit):
    default_unit = "kg"
    _conversion_factors = {
        "kg": ConverstionFactor(1, 0),       # килограмм (базовая единица)
        "g": ConverstionFactor(0.001, 0),    # грамм
        "mg": ConverstionFactor(1e-6, 0),    # миллиграмм
        "t": ConverstionFactor(1000, 0),     # тонна
        "lb": ConverstionFactor(0.45359237, 0), # фунт
        "oz": ConverstionFactor(0.0283495, 0),  # унция
    } 