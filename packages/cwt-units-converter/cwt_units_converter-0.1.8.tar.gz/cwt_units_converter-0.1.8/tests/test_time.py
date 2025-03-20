import unittest
from units_converter.time import TimeUnit

class TestTimeUnit(unittest.TestCase):
    def setUp(self):
        """Создание тестовых объектов для разных временных интервалов"""
        self.second = TimeUnit(1, "s")
        self.minute = TimeUnit(1, "min")
        self.hour = TimeUnit(1, "h")
        self.day = TimeUnit(1, "d")
        self.week = TimeUnit(1, "w")
        self.year = TimeUnit(1, "y")

    def test_initialization(self):
        """Проверка различных способов инициализации"""
        # Инициализация с секундами
        time = TimeUnit(60, "s")
        self.assertEqual(time.s, 60)
        
        # Инициализация с минутами
        time = TimeUnit(1, "min")
        self.assertEqual(time.s, 60)

    def test_basic_conversions(self):
        """Проверка базовых конвертаций между единицами времени"""
        # Секунды в минуты
        self.assertEqual(self.minute.s, 60)
        
        # Минуты в часы
        self.assertEqual(self.hour.min, 60)
        
        # Часы в дни
        self.assertEqual(self.day.h, 24)
        
        # Дни в недели
        self.assertEqual(self.week.d, 7)
        
        # Дни в годы
        self.assertEqual(self.year.d, 365)

    def test_reverse_conversions(self):
        """Проверка обратных конвертаций"""
        # 3600 секунд = 1 час
        time = TimeUnit(3600, "s")
        self.assertEqual(time.h, 1)
        
        # 1440 минут = 1 день
        time = TimeUnit(1440, "min")
        self.assertEqual(time.d, 1)
        
        # 168 часов = 1 неделя
        time = TimeUnit(168, "h")
        self.assertEqual(time.w, 1)

    def test_arithmetic_operations(self):
        """Проверка арифметических операций"""
        # Сложение
        result = self.hour + self.minute
        self.assertEqual(result.min, 61)
        
        # Вычитание
        result = self.day - self.hour
        self.assertEqual(result.h, 23)
        
        # Умножение на число
        result = self.minute * 2
        self.assertEqual(result.s, 120)
        
        # Деление на число
        result = self.hour / 2
        self.assertEqual(result.min, 30)


    def test_complex_conversions(self):
        """Проверка сложных конвертаций"""
        time = TimeUnit(1, "d")
        
        # 1.5 дня в часах
        time.d = 1.5
        self.assertEqual(time.h, 36)
        
        # 2.5 недели в днях
        time.w = 2.5
        self.assertEqual(time.d, 17.5)
        
        # 0.5 года в днях
        time.y = 0.5
        self.assertEqual(time.d, 182.5)

if __name__ == '__main__':
    unittest.main() 