import unittest
from units_converter.density import DensityUnit

class TestDensityUnit(unittest.TestCase):
    def setUp(self):
        """Создаем тестовые объекты"""
        self.kg_per_m3 = DensityUnit(1000, "kg_m3")  # плотность воды
        self.g_per_cm3 = DensityUnit(1, "g_cm3")     # то же самое
        self.lb_per_ft3 = DensityUnit(62.4, "lb_ft3") # примерно то же самое

    def test_base_unit_conversions(self):
        """Проверка конверсии из базовой единицы в другие единицы"""
        water_density = DensityUnit(1000, "kg_m3")  # плотность воды
        
        # Проверяем конверсию в метрические единицы
        self.assertAlmostEqual(water_density.g_cm3, 1)      # 1000 кг/м³ = 1 г/см³
        self.assertAlmostEqual(water_density.g_ml, 1)       # 1000 кг/м³ = 1 г/мл
        self.assertAlmostEqual(water_density.g_l, 1000)     # 1000 кг/м³ = 1000 г/л
        self.assertAlmostEqual(water_density.kg_l, 1)       # 1000 кг/м³ = 1 кг/л
        
        # Проверяем конверсию в имперские единицы
        self.assertAlmostEqual(water_density.lb_ft3, 62.4, places=1)  # ≈ 62.4 фунт/фут³
        self.assertAlmostEqual(water_density.lb_gal, 8.34, places=1)  # ≈ 8.34 фунт/галлон

    def test_reverse_conversions(self):
        """Проверка конверсии из других единиц в базовую"""
        # Создаем объекты с разными единицами измерения (все примерно равны плотности воды)
        g_cm3 = DensityUnit(1, "g_cm3")
        lb_ft3 = DensityUnit(62.4, "lb_ft3")
        kg_l = DensityUnit(1, "kg_l")
        
        # Проверяем, что все они равны примерно 1000 кг/м³
        self.assertAlmostEqual(g_cm3.kg_m3, 1000)
        self.assertAlmostEqual(lb_ft3.kg_m3, 1000, places=0)
        self.assertAlmostEqual(kg_l.kg_m3, 1000)

    def test_arithmetic_operations(self):
        """Проверка арифметических операций с разными единицами измерения"""
        d1 = DensityUnit(1000, "kg_m3")
        d2 = DensityUnit(0.5, "g_cm3")
        
        # Сложение
        result = d1 + d2
        self.assertAlmostEqual(result.kg_m3, 1500)  # 1000 кг/м³ + 500 кг/м³ = 1500 кг/м³
        
        # Вычитание
        result = d1 - d2
        self.assertAlmostEqual(result.kg_m3, 500)   # 1000 кг/м³ - 500 кг/м³ = 500 кг/м³
        
        # Умножение на число
        result = d1 * 2.5
        self.assertAlmostEqual(result.kg_m3, 2500)  # 1000 кг/м³ * 2.5 = 2500 кг/м³
        
        # Деление на число
        result = d1 / 2
        self.assertAlmostEqual(result.kg_m3, 500)   # 1000 кг/м³ / 2 = 500 кг/м³

if __name__ == '__main__':
    unittest.main() 