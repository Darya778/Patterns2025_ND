import unittest
from Src.start_manager import start_manager
from Src.reposity_manager import reposity_manager
from Src.Logics.convert_factory import convert_factory
from Src.Core.common import common
from Src.Dtos.range_dto import range_dto
from Src.Logics.print_service import print_service

# Тесты для проверки конвертации данных (сериализация / десериализация) 
class test_convert(unittest.TestCase):

    # Проверить сериализация одного элемента
    def test_convert_factory_serialize_range(self):
        # Подготовка
        service = start_manager()
        service.start()
        items = reposity_manager().data[  reposity_manager.range_key() ]
        data = common.models_to_dto( items )
        item = data[0]
        factory = convert_factory()

        # Действие
        result = factory.serialize(item)

        # Проверки
        assert result is not None
        assert len(result) > 0
        print(result)


    # Проверить сериализация списка единиц измерения
    def test_convert_factory_serialize_ranges(self):
        # Подготовка
        print_service()
        service = start_manager()
        service.start()
        items = reposity_manager().data[  reposity_manager.range_key() ]
        data = common.models_to_dto( items )

        factory = convert_factory()

        # Действие
        result = factory.serialize(data)

        # Проверки
        assert result is not None
        assert len(result) > 0
        print(result)    

    # Проверить сериализация списка номенклатуры
    def test_convert_factory_serialize_nomenclatures(self):
        # Подготовка
        service = start_manager()
        service.start()
        items = reposity_manager().data[  reposity_manager.nomenclature_key() ]
        data = common.models_to_dto( items )

        factory = convert_factory()

        # Действие
        result = factory.serialize(data)

        # Проверки
        assert result is not None
        assert len(result) > 0
        print(result)    

    # Проверить десериализацию одного элемента
    def test_deserialize_range(self):
        # Подготовка
        service = start_manager()
        service.start()
        data =  {
                "name":"Грамм",
                "id":"adb7510f-687d-428f-a697-26e53d3f65b7",
                "base_id":None,
                "value":1
            }

        # Действие
        result = range_dto().create( data ) 

        # Проверки
        assert result is not None
        assert result.id == "adb7510f-687d-428f-a697-26e53d3f65b7"


    

