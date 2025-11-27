import unittest
from Src.Dtos.nomenclature_dto import nomenclature_dto
from Src.Dtos.range_dto import range_dto
from Src.start_manager import start_manager
from Src.reposity_manager import reposity_manager

# Набор тестов для работы с Dto
class test_dtos(unittest.TestCase):

    # Проверить фабричный метод и загрузку данных в dto
    def test_notThrow_nomenclature_dto_create(self):
        # Подготовка
        data = { "name": "Пшеничная мука", "range_id":"a33dd457-36a8-4de6-b5f1-40afa6193346", "category_id":"7f4ecdab-0f01-4216-8b72-4c91d22b8918", "id":"0c101a7e-5934-4155-83a6-d2c388fcc11a"}
        dto = nomenclature_dto()

        # Действие
        result = dto.create(data)

        # Проверка
        assert result is not None
        assert len(dto.name) > 0


    # Проверить фабричный метод и загрузку данных в dto
    def test_notThrow_range_dto_create(self):
        # Подготовка
        data = { "name":"Грамм", 
                "id":"adb7510f-687d-428f-a697-26e53d3f65b7",
                "base_id":None,
                "value":1 }
        dto = range_dto()

        # Действие
        result = dto.create(data)

        # Проверка
        assert result is not None
        assert len(dto.name) > 0    

    # Проверить фабричный метод перевода в dto
    def test_notThrow_nomenclature_model_to_dto(self):
        # Подготовка
        start = start_manager()
        start.start()    
        item = start.data[  reposity_manager.nomenclature_key() ][0]

        # Действие
        result = item.to_dto()

        # Проверка
        assert result is not None

    # Проверить фабричный метод перевода в dto
    def test_notThrow_range_model_to_dto(self):
        # Подготовка
        start = start_manager()
        start.start()    
        item = start.data[  reposity_manager.range_key() ][0]

        # Действие
        result = item.to_dto()

        # Проверка
        assert result is not None    

    # Проверить фабричный метод перевода в dto
    def test_notThrow_group_model_to_dto(self):
        # Подготовка
        start = start_manager()
        start.start()    
        item = start.data[  reposity_manager.group_key() ][0]

        # Действие
        result = item.to_dto()

        # Проверка
        assert result is not None        

          

        


  
if __name__ == '__main__':
    unittest.main()  