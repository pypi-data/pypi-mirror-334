from dataclasses import dataclass

@dataclass
class ConverstionFactor:
    slope: float
    intercept: float

class Unit:
    default_unit = "default"
    _conversion_factors = {
        "default": ConverstionFactor(1, 0),
        "second" : ConverstionFactor(2, 0)
    }

    def __init__(self, value: float, unit: str) -> None:
        self._value = self._to_internal(value, unit)

    def _to_internal(self, value: float, unit: str) -> float:
        return value * self._conversion_factors[unit].slope + self._conversion_factors[unit].intercept

    def _from_internal(self, value: float, unit: str) -> float:
        return (value - self._conversion_factors[unit].intercept) / self._conversion_factors[unit].slope


    def __add__(self, other: "Unit") -> "Unit":
        return self.__class__(self._value + other._value, self.default_unit)

    def __sub__(self, other: "Unit") -> "Unit":
        return self.__class__(self._value - other._value, self.default_unit)
    
    def __mul__(self, other) -> "Unit":
        if isinstance(other, (int, float)):
            return self.__class__(self._value * other, self.default_unit)
        else:
            raise TypeError(f"Unsupported operand type(s) for *: '{type(self)}' and '{type(other)}'")
    
    def __truediv__(self, other) -> "Unit":
        if isinstance(other, (int, float)):
            return self.__class__(self._value / other, self.default_unit)
        else:
            raise TypeError(f"Unsupported operand type(s) for /: '{type(self)}' and '{type(other)}'")
    
    def __setattr__(self, key: str, value: float) -> None:
        if key in self._conversion_factors:
            self._value = self._to_internal(value, key)
            return
        else:
            return super().__setattr__(key, value)
    
    def __getattr__(self, key: str) -> float:
        if key in self._conversion_factors:
            return self._from_internal(self._value, key)
        else:
            return super().__getattribute__(key)

