import unittest
from Src.Core.common import common

# Тут указать любую модель
from Src.Models.company_model import company_model

# Набор тестов для основных методов
class test_common(unittest.TestCase):

    # Проверить работу метода get_models класса common
    def test_any_common_get_models(self):
        # Подготовка

        # Действие
        result = common.get_models()

        # Проверка
        assert len(result) > 0

    # Проверить работу метода get_fields класса common
    def test_any_common_get_fields(self):
        # Подготовка
        company = company_model()

        # Действие
        result = common.get_fields(company)

        # Проверка
        assert len(result) > 0


  
if __name__ == '__main__':
    unittest.main()  