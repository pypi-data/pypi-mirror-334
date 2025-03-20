import unittest
from units_converter.pressure import PressureUnit

class TestPressureUnit(unittest.TestCase):
    def setUp(self):
        """Создание тестовых объектов"""
        self.pressure_pa = PressureUnit(101325, "pa")  # 1 атм
        self.pressure_bar = PressureUnit(1, "bar")     # 1 бар
        self.pressure_atm = PressureUnit(1, "atm")     # 1 атм
        self.pressure_psi = PressureUnit(14.696, "psi") # 1 атм

    def test_pressure_conversions(self):
        """Проверка конверсии давления"""
        # Проверяем конверсию в Паскали
        self.assertAlmostEqual(self.pressure_bar.pa, 100000, places=0)
        self.assertAlmostEqual(self.pressure_atm.pa, 101325, places=0)
        self.assertAlmostEqual(self.pressure_psi.pa, 101325, places=0)
        
        # Проверяем конверсию в бары
        self.assertAlmostEqual(self.pressure_pa.bar, 1.01325, places=4)
        self.assertAlmostEqual(self.pressure_atm.bar, 1.01325, places=4)
        
        # Проверяем конверсию в атмосферы
        self.assertAlmostEqual(self.pressure_pa.atm, 1, places=4)
        self.assertAlmostEqual(self.pressure_bar.atm, 0.986923, places=4)

    def test_pressure_arithmetic(self):
        """Проверка арифметических операций с давлением"""
        p1 = PressureUnit(101325, "pa")  # 1 атм
        p2 = PressureUnit(202650, "pa")  # 2 атм

        # Проверяем сложение
        result = p1 + p2
        self.assertAlmostEqual(result.pa, 303975)
        self.assertAlmostEqual(result.atm, 3, places=2)
        self.assertAlmostEqual(result.bar, 3.03975, places=4)

        # Проверяем вычитание
        result = p2 - p1
        self.assertAlmostEqual(result.pa, 101325)
        self.assertAlmostEqual(result.atm, 1, places=2)

        # Проверяем умножение на число
        result = p1 * 2
        self.assertAlmostEqual(result.pa, 202650)
        self.assertAlmostEqual(result.atm, 2, places=2)


if __name__ == '__main__':
    unittest.main() 