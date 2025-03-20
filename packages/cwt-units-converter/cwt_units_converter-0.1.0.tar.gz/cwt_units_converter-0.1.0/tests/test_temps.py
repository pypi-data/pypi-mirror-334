import unittest
from units_converter.base import Unit, ConverstionFactor
from units_converter.temp import TemperatureUnit

class TestTemperatureUnit(unittest.TestCase):
    def setUp(self):
        self.temp = TemperatureUnit(273.15, "K")

    def test_temperature_conversions(self):
        """Проверка конверсии температур"""
        # Проверяем конверсию в Цельсии
        self.assertAlmostEqual(self.temp.C, 0, places=2)
        # Проверяем конверсию в Фаренгейты
        self.assertAlmostEqual(self.temp.F, 32, places=2)

    def test_temperature_arithmetic(self):
        """Проверка арифметических операций с температурами"""
        t1 = TemperatureUnit(273.15, "K")  # 0°C
        t2 = TemperatureUnit(283.15, "K")  # 10°C

        # Проверяем разницу температур
        result = t2 - t1
        self.assertAlmostEqual(result.K, 10)

        # Проверяем умножение на коэффициент
        result = t1 * 2
        self.assertAlmostEqual(result.K, 546.3, places=1)

if __name__ == '__main__':
    unittest.main() 