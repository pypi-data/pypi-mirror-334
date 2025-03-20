from .base import Unit, ConverstionFactor
from math import exp

class TDSUnit(Unit):
    default_unit = "usm"  # микросименс/см
    _conversion_factors = {
            "usm": ConverstionFactor(1, 0),  # микросименс/см (базовая единица)
            "ppm": ConverstionFactor(1, 0),  # мг/л (коэффициент будет рассчитываться динамически)
        }
    def __init__(self, value: float = 0, unit: str = "usm"):
        self._conversion_factors["ppm"].slope = self._calculate_conversion_factor(value)
        super().__init__(value, unit)

    @staticmethod
    def _calculate_ionic_strength(conductivity_usm: float) -> float:
        """
        Рассчитывает ионную силу раствора на основе электропроводности.
        Эмпирическая формула, основанная на исследованиях природных вод.
        
        Args:
            conductivity_usm: электропроводность в мкСм/см
            
        Returns:
            Ионная сила раствора (безразмерная величина)
        """
        # Эмпирическая формула для расчета ионной силы
        # Для природных вод с минерализацией до 5000 мг/л
        return 1.6e-5 * conductivity_usm

    @staticmethod
    def _calculate_conversion_factor(conductivity_usm: float) -> float:
        """
        Рассчитывает коэффициент пересчета между usm и ppm по методике DuPont.
        
        Коэффициент зависит от диапазона электропроводности:
        - Для чистой воды (< 100 мкСм/см): 0.5
        - Для солоноватой воды (100-5000 мкСм/см): 0.5-0.7
        - Для морской воды (>5000 мкСм/см): 0.7-0.75
        
        Args:
            conductivity_usm: электропроводность в мкСм/см
            
        Returns:
            Коэффициент пересчета usm -> ppm
        """
        if conductivity_usm <= 100:
            return 0.5
        elif conductivity_usm <= 5000:
            # Линейная интерполяция от 0.5 до 0.7 в диапазоне 100-5000 мкСм/см
            return 0.5 + 0.2 * (conductivity_usm - 100) / 4900
        else:
            # Линейная интерполяция от 0.7 до 0.75 для значений >5000 мкСм/см
            # Максимум 0.75 для очень высоких концентраций
            factor = 0.7 + 0.05 * (conductivity_usm - 5000) / 45000
            return min(factor, 0.75)

    def _to_internal(self, value: float, unit: str) -> float:
        """
        Конвертирует значение в базовые единицы (usm).
        
        Args:
            value: значение для конвертации
            unit: единица измерения входного значения
            
        Returns:
            Значение в базовых единицах (usm)
        """
        if unit == "usm":
            return value
        elif unit == "ppm":
            # Для обратного пересчета из ppm в usm используем метод последовательных приближений
            # так как коэффициент зависит от конечного результата
            usm = value / 0.5  # Начальное приближение
            for _ in range(3):  # Обычно достаточно 3 итераций
                factor = self._calculate_conversion_factor(usm)
                usm = value / factor
            return usm
        else:
            raise ValueError(f"Неподдерживаемая единица измерения: {unit}")

    def _from_internal(self, value: float, unit: str) -> float:
        """
        Конвертирует значение из базовых единиц (usm) в требуемые.
        
        Args:
            value: значение в базовых единицах (usm)
            unit: целевая единица измерения
            
        Returns:
            Значение в требуемых единицах
        """
        if unit == "usm":
            return value
        elif unit == "ppm":
            factor = self._calculate_conversion_factor(value)
            return value * factor
        else:
            raise ValueError(f"Неподдерживаемая единица измерения: {unit}")
