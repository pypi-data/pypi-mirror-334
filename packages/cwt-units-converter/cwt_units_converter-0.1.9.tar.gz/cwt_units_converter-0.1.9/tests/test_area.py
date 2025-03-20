import unittest
from units_converter.area import AreaUnit

class TestAreaUnit(unittest.TestCase):
    def setUp(self):
        """Создание тестовых объектов"""
        self.area_m2 = AreaUnit(1.0, "m2")      # 1 м²
        self.area_cm2 = AreaUnit(10000.0, "cm2") # 1 м²
        self.area_ha = AreaUnit(1.0, "ha")      # 1 гектар
        self.area_acre = AreaUnit(1.0, "acre")  # 1 акр

    def test_area_conversions(self):
        """Проверка конверсии площади"""
        # Проверяем конверсию в м²
        self.assertAlmostEqual(self.area_cm2.m2, 1.0, places=2)
        self.assertAlmostEqual(self.area_ha.m2, 10000.0, places=2)
        self.assertAlmostEqual(self.area_acre.m2, 4046.86, places=2)
        
        # Проверяем конверсию в см²
        self.assertAlmostEqual(self.area_m2.cm2, 10000.0, places=2)
        self.assertAlmostEqual(self.area_ha.cm2, 100000000.0, places=2)
        
        # Проверяем конверсию в гектары
        self.assertAlmostEqual(self.area_m2.ha, 0.0001, places=6)
        self.assertAlmostEqual(self.area_acre.ha, 0.404686, places=6)

    def test_area_arithmetic(self):
        """Проверка арифметических операций с площадью"""
        a1 = AreaUnit(1.0, "m2")  # 1 м²
        a2 = AreaUnit(0.5, "m2")  # 0.5 м²

        # Проверяем сложение
        result = a1 + a2
        self.assertAlmostEqual(result.m2, 1.5)
        self.assertAlmostEqual(result.cm2, 15000.0)
        self.assertAlmostEqual(result.ha, 0.00015, places=6)

        # Проверяем вычитание
        result = a1 - a2
        self.assertAlmostEqual(result.m2, 0.5)
        self.assertAlmostEqual(result.cm2, 5000.0)

        # Проверяем умножение на число
        result = a1 * 2
        self.assertAlmostEqual(result.m2, 2.0)
        self.assertAlmostEqual(result.cm2, 20000.0)


if __name__ == '__main__':
    unittest.main() 