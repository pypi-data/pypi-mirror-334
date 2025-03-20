import unittest
from units_converter.flow_rate import FlowRateUnit

class TestFlowRateUnit(unittest.TestCase):
    def setUp(self):
        """Создание тестовых объектов"""
        self.flow_m3_h = FlowRateUnit(1.0, "m3_h")    # 1 м³/ч
        self.flow_l_h = FlowRateUnit(1, "l_h")   # 1000 л/ч
        self.flow_m3_s = FlowRateUnit(1, "m3_s")  # 1 м³/с
        self.flow_l_s = FlowRateUnit(1, "l_s")  # 1000 л/с

    def test_flow_rate_conversions(self):
        """Проверка конверсии расходов"""
        # Проверяем конверсию в м³/ч
        self.assertAlmostEqual(self.flow_l_h.m3_h, 1.0/3600, places=2)
        self.assertAlmostEqual(self.flow_m3_s.m3_h, 3600.0, places=2)
        self.assertAlmostEqual(self.flow_l_s.m3_h, 3.60, places=2)
        
        # Проверяем конверсию в л/ч
        self.assertAlmostEqual(self.flow_m3_h.l_h, 1000.0, places=2)
        self.assertAlmostEqual(self.flow_m3_s.l_h, 3600000.0, places=2)
        
        # Проверяем конверсию в м³/с
        self.assertAlmostEqual(self.flow_m3_h.m3_s, 1/3600.0, places=6)
        self.assertAlmostEqual(self.flow_l_h.m3_s, 1/3600000.0, places=6)

    def test_flow_rate_arithmetic(self):
        """Проверка арифметических операций с расходами"""
        f1 = FlowRateUnit(1.0, "m3_h")  # 1 м³/ч
        f2 = FlowRateUnit(0.5, "m3_h")  # 0.5 м³/ч

        # Проверяем сложение
        result = f1 + f2
        self.assertAlmostEqual(result.m3_h, 1.5)
        self.assertAlmostEqual(result.l_h, 1500.0)
        self.assertAlmostEqual(result.m3_s, 1.5/3600.0, places=6)

        # Проверяем вычитание
        result = f1 - f2
        self.assertAlmostEqual(result.m3_h, 0.5)
        self.assertAlmostEqual(result.l_h, 500.0)

        # Проверяем умножение на число
        result = f1 * 2
        self.assertAlmostEqual(result.m3_h, 2.0)
        self.assertAlmostEqual(result.l_h, 2000.0)


if __name__ == '__main__':
    unittest.main() 