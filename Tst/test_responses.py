from Src.start_manager import start_manager
from Src.reposity_manager import reposity_manager
from Src.Logics.response_markdown import response_markdown
from Src.Logics.response_json import response_json
import unittest
from Src.Core.common import common

# Набор тестов для проверки формирования данных
# в разных форматах
class test_responses(unittest.TestCase):

    # Проверить формирование Markdown 
    def test_response_markdown_build(self):
        # Подготовка
        service = start_manager()
        service.start()
        response = response_markdown()
        items = service.data[ reposity_manager.nomenclature_key() ]
        data = common.models_to_dto(items)

        # Действие
        result = response.build( data )

        # Проверка
        assert len(result) > 0
        print(result)


    # Проверить формирование Json 
    def test_response_json_build(self):
        # Подготовка
        service = start_manager()
        service.start()
        response = response_json()
        items = service.data[ reposity_manager.nomenclature_key() ]
        data = common.models_to_dto(items)

        # Действие
        result = response.build( data )

        # Проверка
        assert len(result) > 0
        print(result)
    

  
if __name__ == '__main__':
    unittest.main()  