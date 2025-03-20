import unittest
from units_converter.mass import MassUnit

class TestMassUnit(unittest.TestCase):
    def setUp(self):
        """Создаем тестовые объекты"""
        self.kilogram = MassUnit(1, "kg")
        self.gram = MassUnit(1000, "g")
        self.pound = MassUnit(2.20462, "lb")

    def test_base_unit_conversions(self):
        """Проверка конверсии из базовой единицы (килограмм) в другие единицы"""
        one_kg = MassUnit(1, "kg")
        
        # Проверяем конверсию в метрические единицы
        self.assertAlmostEqual(one_kg.g, 1000)      # 1 кг = 1000 г
        self.assertAlmostEqual(one_kg.mg, 1e6)      # 1 кг = 1,000,000 мг
        self.assertAlmostEqual(one_kg.t, 0.001)     # 1 кг = 0.001 т
        
        # Проверяем конверсию в имперские единицы
        self.assertAlmostEqual(one_kg.lb, 2.20462, places=5)  # 1 кг ≈ 2.20462 фунта
        self.assertAlmostEqual(one_kg.oz, 35.274, places=3)   # 1 кг ≈ 35.274 унций

    def test_reverse_conversions(self):
        """Проверка конверсии из других единиц в килограммы"""
        # Создаем объекты с разными единицами измерения
        g1000 = MassUnit(1000, "g")
        lb = MassUnit(2.20462, "lb")
        oz = MassUnit(35.274, "oz")
        
        # Проверяем, что все они равны примерно 1 килограмму
        self.assertAlmostEqual(g1000.kg, 1)
        self.assertAlmostEqual(lb.kg, 1, places=5)
        self.assertAlmostEqual(oz.kg, 1, places=5)

    def test_arithmetic_operations(self):
        """Проверка арифметических операций с разными единицами измерения"""
        kg1 = MassUnit(1, "kg")
        g500 = MassUnit(500, "g")
        
        # Сложение
        result = kg1 + g500
        self.assertAlmostEqual(result.kg, 1.5)  # 1кг + 500г = 1.5кг
        
        # Вычитание
        result = kg1 - g500
        self.assertAlmostEqual(result.kg, 0.5)  # 1кг - 500г = 0.5кг
        
        # Умножение на число
        result = kg1 * 2.5
        self.assertAlmostEqual(result.kg, 2.5)  # 1кг * 2.5 = 2.5кг
        
        # Деление на число
        result = kg1 / 2
        self.assertAlmostEqual(result.kg, 0.5)  # 1кг / 2 = 0.5кг

    def test_invalid_operations(self):
        """Проверка некорректных операций"""
        mass = MassUnit(1, "kg")
        
        # Попытка установить значение через атрибут
        with self.assertRaises(AttributeError):
            mass.kg = 10
            
        # Попытка получить значение в несуществующей единице
        with self.assertRaises(AttributeError):
            _ = mass.invalid_unit
            
        # Некорректные арифметические операции
        with self.assertRaises(TypeError):
            mass * "2"
        with self.assertRaises(TypeError):
            mass / "2"

if __name__ == '__main__':
    unittest.main() 