import unittest
from Src.Logics.response_csv import response_csv
from Src.Models.group_model import group_model
from Src.Logics.factory_entities import factory_entities
from Src.Core.response_formats import response_formats
from Src.Models.range_model import range_model

# Тесты для проверки логики 
class test_logics(unittest.TestCase):

    # Проверим формирование CSV
    def test_notNone_response_csv_buld(self):
        # Подготовка
        response = response_csv()
        data = []
        entity = group_model.create( "test" )
        data.append( entity )

        # Дейстие
        result = response.build( data)

        # Проверка
        assert result is not None


    def test_notNone_factory_create_csv(self):
        # Подготовка
        factory = factory_entities()
        data = []
        entity = group_model.create( "test" )
        data.append( entity )

        # Действие
        instance = factory.create( response_formats.csv() )

        # Проверка
        assert instance is not None
        text = instance().build(data)
        assert len(text) > 0
        print(text)


    
    def test_notNone_factory_create_markdown(self):
        # Подготовка
        factory = factory_entities()
        data = []
        entity = range_model.create( "тест", 1, None)
        data.append( entity )

        # Действие
        instance = factory.create( response_formats.markdown() )

        # Проверка
        assert instance is not None
        text = instance().build(data)
        assert len(text) > 0
        print(text)    

        
  
if __name__ == '__main__':
    unittest.main()   
