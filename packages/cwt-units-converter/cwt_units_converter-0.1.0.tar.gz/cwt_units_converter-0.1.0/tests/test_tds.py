import unittest
from units_converter.tds import TDSUnit

class TestTDSUnit(unittest.TestCase):
    def setUp(self):
        # Создаем тестовые экземпляры для разных диапазонов минерализации
        self.pure_water = TDSUnit()  # Чистая вода
        self.pure_water.usm = 50
        self.brackish_water = TDSUnit()  # Солоноватая вода
        self.brackish_water.usm = 1000
        self.seawater = TDSUnit()  # Морская вода
        self.seawater.usm = 10000

    def test_initialization(self):
        """Проверка различных способов инициализации"""
        # Инициализация без параметров
        tds = TDSUnit()
        self.assertEqual(tds.usm, 0)
        
        # Инициализация с usm
        tds = TDSUnit()
        tds.usm = 100
        self.assertEqual(tds.usm, 100)
        
        # Инициализация с ppm
        tds = TDSUnit()
        tds.ppm = 50
        self.assertAlmostEqual(tds.usm, 100, places=0)

    def test_conversion_factors(self):
        """Проверка коэффициентов пересчета для разных диапазонов"""
        # Чистая вода
        self.assertAlmostEqual(TDSUnit._calculate_conversion_factor(50), 0.5)
        self.assertAlmostEqual(TDSUnit._calculate_conversion_factor(100), 0.5)

        # Солоноватая вода
        self.assertAlmostEqual(TDSUnit._calculate_conversion_factor(1000), 0.537, places=3)
        self.assertAlmostEqual(TDSUnit._calculate_conversion_factor(5000), 0.7)

        # Морская вода
        self.assertAlmostEqual(TDSUnit._calculate_conversion_factor(10000), 0.711, places=1)
        self.assertAlmostEqual(TDSUnit._calculate_conversion_factor(50000), 0.75)

    def test_usm_to_ppm_conversion(self):
        """Проверка конвертации из usm в ppm"""
        # Чистая вода
        self.assertAlmostEqual(self.pure_water.ppm, 25)  # 50 * 0.5

        # Солоноватая вода
        self.assertAlmostEqual(self.brackish_water.ppm, 537, places=0)  # 1000 * 0.537

        # Морская вода
        self.assertAlmostEqual(abs(self.seawater.ppm-7110)/200, 0, places=0)  # 10000 * 0.711

    def test_ppm_to_usm_conversion(self):
        """Проверка конвертации из ppm в usm"""
        # Чистая вода
        pure = TDSUnit()
        pure.ppm = 25
        self.assertAlmostEqual(pure.usm, 50, places=0)

        # Солоноватая вода
        brackish = TDSUnit()
        brackish.ppm = 537
        self.assertAlmostEqual(brackish.usm, 1000, places=0)

        # Морская вода
        seawater = TDSUnit()
        seawater.ppm = 7110
        self.assertAlmostEqual(abs(seawater.usm-10000)/200,0, places=0)

    def test_arithmetic_operations(self):
        """Проверка арифметических операций"""
        # Сложение
        result = self.pure_water + self.brackish_water
        self.assertAlmostEqual(result.usm, 1050)
        
        # Вычитание
        result = self.seawater - self.brackish_water
        self.assertAlmostEqual(result.usm, 9000)
        
        # Умножение на число
        result = self.brackish_water * 2
        self.assertAlmostEqual(result.usm, 2000)
        
        # Деление на число
        result = self.seawater / 2
        self.assertAlmostEqual(result.usm, 5000)

    def test_invalid_operations(self):
        """Проверка недопустимых операций"""
        # Отрицательные значения
        with self.assertRaises(ValueError):
            tds = TDSUnit()
            tds.usm = -100

        with self.assertRaises(ValueError):
            tds = TDSUnit()
            tds.ppm = -50

        # Некорректные арифметические операции
        with self.assertRaises(TypeError):
            result = self.pure_water + 100

        with self.assertRaises(TypeError):
            result = self.pure_water * self.brackish_water

        # Деление на ноль
        with self.assertRaises(ZeroDivisionError):
            result = self.pure_water / 0

if __name__ == '__main__':
    unittest.main() 