import unittest
from units_converter.length import LengthUnit

class TestLengthUnit(unittest.TestCase):
    def setUp(self):
        """Создаем тестовые объекты"""
        self.meter = LengthUnit(1, "m")
        self.kilometer = LengthUnit(1, "km")
        self.centimeter = LengthUnit(100, "cm")


    def test_base_unit_conversions(self):
        """Проверка конверсии из базовой единицы (метр) в другие единицы"""
        one_meter = LengthUnit(1, "m")
        
        # Проверяем конверсию в основные единицы
        self.assertAlmostEqual(one_meter.km, 0.001)    # 1 м = 0.001 км
        self.assertAlmostEqual(one_meter.cm, 100)      # 1 м = 100 см
        self.assertAlmostEqual(one_meter.mm, 1000)     # 1 м = 1000 мм
        self.assertAlmostEqual(one_meter.um, 1e6)      # 1 м = 1,000,000 мкм


    def test_reverse_conversions(self):
        """Проверка конверсии из других единиц в метры"""
        # Создаем объекты с разными единицами измерения
        km = LengthUnit(1, "km")
        cm = LengthUnit(100, "cm")
        mm = LengthUnit(1000, "mm")
        ft = LengthUnit(3.28084, "ft")
        
        # Проверяем, что все они равны примерно 1 метру
        self.assertAlmostEqual(km.m, 1000)
        self.assertAlmostEqual(cm.m, 1)
        self.assertAlmostEqual(mm.m, 1)
        self.assertAlmostEqual(ft.m, 1, places=5)

    def test_arithmetic_operations(self):
        """Проверка арифметических операций с разными единицами измерения"""
        m1 = LengthUnit(1, "m")
        cm100 = LengthUnit(100, "cm")
        
        # Сложение
        result = m1 + cm100
        self.assertAlmostEqual(result.m, 2)  # 1м + 100см = 2м
        
        # Вычитание
        result = m1 - LengthUnit(50, "cm")
        self.assertAlmostEqual(result.m, 0.5)  # 1м - 50см = 0.5м
        
        # Умножение на число
        result = m1 * 2.5
        self.assertAlmostEqual(result.m, 2.5)  # 1м * 2.5 = 2.5м
        
        # Деление на число
        result = m1 / 2
        self.assertAlmostEqual(result.m, 0.5)  # 1м / 2 = 0.5м

if __name__ == '__main__':
    unittest.main() 