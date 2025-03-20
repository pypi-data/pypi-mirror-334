import unittest
from units_converter.volume import VolumeUnit

class TestVolumeUnit(unittest.TestCase):
    def setUp(self):
        """Создание тестовых объектов"""
        self.volume_m3 = VolumeUnit(1, "m3")     # 1 куб. метр
        self.volume_l = VolumeUnit(1000, "l")    # 1000 литров
        self.volume_gal = VolumeUnit(264.172, "gal")  # 1 куб. метр в галлонах
        self.volume_ft3 = VolumeUnit(35.3147, "ft3")  # 1 куб. метр в куб. футах

    def test_volume_conversions(self):
        """Проверка конверсии объема"""
        # Проверяем конверсию в кубические метры
        self.assertAlmostEqual(self.volume_l.m3, 1, places=3)
        self.assertAlmostEqual(self.volume_gal.m3, 1, places=3)
        self.assertAlmostEqual(self.volume_ft3.m3, 1, places=3)
        
        # Проверяем конверсию в литры
        self.assertAlmostEqual(self.volume_m3.l, 1000, places=0)
        self.assertAlmostEqual(self.volume_gal.l, 1000, places=0)
        
        # Проверяем конверсию в галлоны
        self.assertAlmostEqual(self.volume_m3.gal, 264.172, places=3)
        self.assertAlmostEqual(self.volume_l.gal, 264.172, places=3)

    def test_volume_arithmetic(self):
        """Проверка арифметических операций с объемом"""
        v1 = VolumeUnit(1, "m3")  # 1 куб. метр
        v2 = VolumeUnit(2, "m3")  # 2 куб. метра

        # Проверяем сложение
        result = v1 + v2
        self.assertAlmostEqual(result.m3, 3)
        self.assertAlmostEqual(result.l, 3000)
        self.assertAlmostEqual(result.gal, 792.516, places=1)

        # Проверяем вычитание
        result = v2 - v1
        self.assertAlmostEqual(result.m3, 1)
        self.assertAlmostEqual(result.l, 1000)

        # Проверяем умножение на число
        result = v1 * 2
        self.assertAlmostEqual(result.m3, 2)
        self.assertAlmostEqual(result.l, 2000)

if __name__ == '__main__':
    unittest.main() 