import unittest
from units_converter.temp import TemperatureUnit

class TestTemperatureUnit(unittest.TestCase):
    def setUp(self):
        """Создание тестовых объектов"""
        self.temp_k = TemperatureUnit(273.15, "k")  # 0°C
        self.temp_c = TemperatureUnit(0, "c")       # 0°C
        self.temp_f = TemperatureUnit(32, "f")      # 0°C

    def test_temperature_conversions(self):
        """Проверка конверсии температур"""
        # Проверяем конверсию в Кельвины
        self.assertAlmostEqual(self.temp_c.k, 273.15, places=2)
        self.assertAlmostEqual(self.temp_f.k, 273.15, places=2)
        
        # Проверяем конверсию в Цельсии
        self.assertAlmostEqual(self.temp_k.c, 0, places=2)
        self.assertAlmostEqual(self.temp_f.c, 0, places=2)
        
        # Проверяем конверсию в Фаренгейты
        self.assertAlmostEqual(self.temp_k.f, 32, places=2)
        self.assertAlmostEqual(self.temp_c.f, 32, places=2)

    def test_temperature_arithmetic(self):
        """Проверка арифметических операций с температурами"""
        t1 = TemperatureUnit(273.15, "k")  # 0°C
        t2 = TemperatureUnit(283.15, "k")  # 10°C

        # Проверяем разницу температур
        result = t2 - t1
        self.assertAlmostEqual(result.k, 10)

        # Проверяем умножение на коэффициент
        result = t1 * 2
        self.assertAlmostEqual(result.k, 546.3, places=1)
        self.assertAlmostEqual(result.c, 273.15, places=1)
        self.assertAlmostEqual(result.f, 523.67, places=1)


if __name__ == '__main__':
    unittest.main() 