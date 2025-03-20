import unittest
from units_converter.volume import VolumeUnit

class TestVolumeUnit(unittest.TestCase):
    def setUp(self):
        """Создаем тестовые объекты"""
        self.cubic_meter = VolumeUnit(1, "m3")
        self.liter = VolumeUnit(1000, "l")
        self.gallon = VolumeUnit(264.172, "gal")

    def test_base_unit_conversions(self):
        """Проверка конверсии из базовой единицы (кубический метр) в другие единицы"""
        one_m3 = VolumeUnit(1, "m3")
        
        # Проверяем конверсию в метрические единицы
        self.assertAlmostEqual(one_m3.cm3, 1e6, places=2)     # 1 м³ = 1,000,000 см³
        self.assertAlmostEqual(one_m3.mm3, 1e9, places=2)     # 1 м³ = 1,000,000,000 мм³
        self.assertAlmostEqual(one_m3.l, 1000, places=2)      # 1 м³ = 1000 л
        self.assertAlmostEqual(one_m3.ml, 1e6, places=2)      # 1 м³ = 1,000,000 мл
        
        # Проверяем конверсию в имперские единицы
        self.assertAlmostEqual(one_m3.gal, 264.172, places=3)   # 1 м³ ≈ 264.172 галлона
        self.assertAlmostEqual(one_m3.qt, 1056.69, places=2)    # 1 м³ ≈ 1056.69 кварт
        self.assertAlmostEqual(one_m3.pt, 2113.38, places=2)    # 1 м³ ≈ 2113.38 пинт
        self.assertAlmostEqual(one_m3.fl_oz, 33814.0, places=0) # 1 м³ ≈ 33814.0 жидких унций

    def test_reverse_conversions(self):
        """Проверка конверсии из других единиц в кубические метры"""
        # Создаем объекты с разными единицами измерения
        l1000 = VolumeUnit(1000, "l")
        cm3_1e6 = VolumeUnit(1e6, "cm3")
        gal = VolumeUnit(264.172, "gal")
        
        # Проверяем, что все они равны примерно 1 кубическому метру
        self.assertAlmostEqual(l1000.m3, 1)
        self.assertAlmostEqual(cm3_1e6.m3, 1)
        self.assertAlmostEqual(gal.m3, 1, places=5)

    def test_arithmetic_operations(self):
        """Проверка арифметических операций с разными единицами измерения"""
        m3_1 = VolumeUnit(1, "m3")
        l500 = VolumeUnit(500, "l")
        
        # Сложение
        result = m3_1 + l500
        self.assertAlmostEqual(result.m3, 1.5)  # 1м³ + 500л = 1.5м³
        
        # Вычитание
        result = m3_1 - l500
        self.assertAlmostEqual(result.m3, 0.5)  # 1м³ - 500л = 0.5м³
        
        # Умножение на число
        result = m3_1 * 2.5
        self.assertAlmostEqual(result.m3, 2.5)  # 1м³ * 2.5 = 2.5м³
        
        # Деление на число
        result = m3_1 / 2
        self.assertAlmostEqual(result.m3, 0.5)  # 1м³ / 2 = 0.5м³


if __name__ == '__main__':
    unittest.main() 