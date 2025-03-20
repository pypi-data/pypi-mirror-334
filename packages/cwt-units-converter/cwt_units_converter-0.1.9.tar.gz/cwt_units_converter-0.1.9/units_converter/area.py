from .base import Unit
from .base import ConverstionFactor

class AreaUnit(Unit):
    """Класс для измерения площади"""
    
    default_unit = "m2"
    _conversion_factors = {
        "m2": ConverstionFactor(1, 0),           # квадратный метр (базовая единица)
        "cm2": ConverstionFactor(1/10000, 0),    # квадратный сантиметр
        "mm2": ConverstionFactor(1/1000000, 0),  # квадратный миллиметр
        "km2": ConverstionFactor(1000000, 0),    # квадратный километр
        "ha": ConverstionFactor(10000, 0),       # гектар
        "acre": ConverstionFactor(4046.86, 0),   # акр
        "ft2": ConverstionFactor(0.092903, 0),   # квадратный фут
        "in2": ConverstionFactor(0.00064516, 0), # квадратный дюйм
        "yd2": ConverstionFactor(0.836127, 0),   # квадратный ярд
        "a": ConverstionFactor(100, 0),          # ар
    }
    
    def __repr__(self):
        """Строковое представление объекта"""
        return f"AreaUnit(value={self.value}, unit={self.unit})" 