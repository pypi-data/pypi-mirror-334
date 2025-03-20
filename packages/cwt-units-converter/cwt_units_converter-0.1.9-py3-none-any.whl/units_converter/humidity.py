from .base import Unit, ConverstionFactor

class HumidityUnit(Unit):
    default_unit = "ratio"  # Относительная влажность как базовая единица
    _conversion_factors = {
        "ratio": ConverstionFactor(1, 0),           # Относительная влажность (базовая единица)
        "perc": ConverstionFactor(0.01, 0),         # Грамм на кубический метр
    }

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self._value}, unit={self.default_unit})" 