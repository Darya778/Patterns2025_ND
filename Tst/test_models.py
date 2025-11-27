from Src.settings_manager import settings_manager
from Src.Models.company_model import company_model
import unittest
from Src.Models.storage_model import storage_model
import uuid
from Src.Models.nomenclature_model import nomenclature_model

class test_models(unittest.TestCase):

    # Провери создание основной модели
    # Данные после создания должны быть пустыми
    def test_empty_createmodel_companymodel(self):
        # Подготовка
        model = company_model()

        # Действие

        # Проверки
        assert model.name == ""


    # Проверить создание основной модели
    # Данные меняем. Данные должны быть
    def test_notEmpty_createmodel_companymodel(self):
        # Подготовка
        model = company_model()
        
        # Действие
        model.name = "test"
        
        # Проверки
        assert model.name != ""

    # Проверить создание основной модели
    # Данные загружаем через json настройки
    def test_load_createmodel_companymodel(self):
        # Подготовка
       file_name = "settings.json"
       manager = settings_manager()
       manager.file_name = file_name
       
       # Действие
       result = manager.load()
            
       # Проверки
       print(manager.file_name)
       assert result == True


    # Проверить создание основной модели
    # Данные загружаем. Проверяем работу Singletone
    def test_loadCombo_createmodel_companymodel(self):
        # Подготовка
        file_name = "./Tst/settings.json"
        manager1 = settings_manager()
        manager1.file_name = file_name
        manager2 = settings_manager()
        check_inn = 123456789
      

        # Действие
        manager1.load()

        # Проверки
        assert manager1.settings == manager2.settings
        print(manager1.file_name)
        assert(manager1.settings.company.inn == check_inn )
        print(f"ИНН {manager1.settings.company.inn}")

    # Проверка на сравнение двух по значению одинаковых моделей
    def test_equals_storage_model_create(self):
        # Подготовка
        id = uuid.uuid4().hex
        storage1 = storage_model()
        storage1.unique_code = id
        storage2 = storage_model()   
        storage2.unique_code = id

        # Действие 

        # Проверки
        assert storage1 == storage2

    # Проверить создание номенклатуры и присвоение уникального кода
    def test_equals_nomenclature_model_create(self):
        # Подготовка
        id = uuid.uuid4().hex
        item1 = nomenclature_model()
        item1.unique_code = id
        item2 = nomenclature_model()
        item2.unique_code = id

        # Действие

        # Проверки
        assert item1 == item2

    
  
if __name__ == '__main__':
    unittest.main()   
