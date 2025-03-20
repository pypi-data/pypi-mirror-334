from .base import Unit, ConverstionFactor

class TemperatureUnit(Unit):
    default_unit = "k"
    _conversion_factors = {
        "k": ConverstionFactor(1, 0),
        "c": ConverstionFactor(1, 273.15),
        "f": ConverstionFactor(5/9, 255.372),
    }

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self._value}, unit={self.default_unit})"
