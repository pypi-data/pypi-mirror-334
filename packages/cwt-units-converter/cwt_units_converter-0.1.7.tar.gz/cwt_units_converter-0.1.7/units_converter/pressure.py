from .base import Unit, ConverstionFactor

class PressureUnit(Unit):
    default_unit = "pa"  # Паскаль как базовая единица
    _conversion_factors = {
        "pa": ConverstionFactor(1, 0),           # Паскаль (базовая единица)
        "bar": ConverstionFactor(1e5, 0),        # Бар
        "atm": ConverstionFactor(101325, 0),     # Атмосфера
        "psi": ConverstionFactor(6894.76, 0),    # Фунт на квадратный дюйм
        "mmhg": ConverstionFactor(133.322, 0),   # Миллиметр ртутного столба
        "mbar": ConverstionFactor(100, 0),       # Миллибар
        "kpa": ConverstionFactor(1000, 0),       # Килопаскаль
        "mpa": ConverstionFactor(1e6, 0),        # Мегапаскаль
    }

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self._value}, unit={self.default_unit})" 