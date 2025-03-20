import unittest
from units_converter.humidity import HumidityUnit

class TestHumidityUnit(unittest.TestCase):
    def setUp(self):
        """Создание тестовых объектов"""
        self.humidity_ratio = HumidityUnit(0.5, "ratio")      # 50% относительной влажности
        self.humidity_perc = HumidityUnit(10, "perc")  # 10 г/м³

    def test_humidity_conversions(self):
        """Проверка конверсии влажности"""
        # Проверяем конверсию в относительную влажность
        self.assertAlmostEqual(self.humidity_perc.ratio, 0.1, places=2)
        self.assertAlmostEqual(self.humidity_ratio.perc, 50, places=2)

    def test_humidity_arithmetic(self):
        """Проверка арифметических операций с влажностью"""
        h1 = HumidityUnit(50, "perc")  # 50% относительной влажности
        h2 = HumidityUnit(30, "perc")  # 30% относительной влажности

        # Проверяем сложение
        result = h1 + h2
        self.assertAlmostEqual(result.perc, 80)
        self.assertAlmostEqual(result.ratio, 0.8)

        # Проверяем вычитание
        result = h1 - h2
        self.assertAlmostEqual(result.perc, 20)
        self.assertAlmostEqual(result.ratio, 0.2)

        # Проверяем умножение на число
        result = h1*2
        self.assertAlmostEqual(result.perc, 100)
        self.assertAlmostEqual(result.ratio, 1)


if __name__ == '__main__':
    unittest.main() 