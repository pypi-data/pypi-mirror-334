from .base import Unit, ConverstionFactor

class VolumeUnit(Unit):
    default_unit = "m3"  # Кубический метр как базовая единица
    _conversion_factors = {
        "m3": ConverstionFactor(1, 0),           # Кубический метр (базовая единица)
        "l": ConverstionFactor(0.001, 0),        # Литр
        "ml": ConverstionFactor(1e-6, 0),        # Миллилитр
        "gal": ConverstionFactor(0.00378541, 0), # Галлон (US)
        "ft3": ConverstionFactor(0.0283168, 0),  # Кубический фут
        "in3": ConverstionFactor(1.63871e-5, 0), # Кубический дюйм
        "bbl": ConverstionFactor(0.158987, 0),   # Баррель нефтяной
        "fl_oz": ConverstionFactor(2.95735e-5, 0), # Жидкая унция (US)
    }

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self._value}, unit={self.default_unit})" 