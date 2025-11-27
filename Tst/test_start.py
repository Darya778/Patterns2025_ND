from Src.reposity_manager import reposity_manager
from Src.start_manager import start_manager
import unittest

# Набор тестов для проверки работы статового сервиса
class test_start(unittest.TestCase):

    # Проверить создание start_service и заполнение данными
    def test_notThow_start_service_load(self):
        # Подготовка
        start = start_manager()

        # Действие
        start.start()

        # Проверка
        print(start.error_message)
        assert len(start.data[ reposity_manager.range_key()]) > 0
        assert len(start.data[ reposity_manager.group_key()]) > 0
        assert len(start.data[ reposity_manager.nomenclature_key()]) > 0
        assert len(start.data[ reposity_manager.receipt_key()]) > 0
        assert len(start.data[ reposity_manager.storage_key()]) > 0
        assert len(start.data[ reposity_manager.transaction_key() ]) > 0

    # Проверить уникальность элемиентов
    def test_checkUnique_start_service_load(self):
        # Подготовка
        start = start_manager()

        # Действие
        start.start()

        # Проверка
        gramm =  list(filter(lambda x: x.name == "Грамм", start.data[ reposity_manager.range_key()])) 
        kg =  list(filter(lambda x: x.name == "Киллограмм", start.data[ reposity_manager.range_key()])) 
        assert gramm[0].unique_code == kg[0].base.unique_code


    # Проверить метод keys класса reposity_manager
    def test_any_reposity_keys(self):
        # Подготовка

        # Действие
        result = reposity_manager.keys()
        
        # Проверка
        assert len(result) > 0

    # Проверить метод initalize класса reposity 
    def test_notThrow_reposity_initialize(self):   
        # Подготовка
        repo = reposity_manager()

        # Действие
        repo.initalize() 

    # Проверить сохранение данных
    def test_true_start_service_save(self):
        # Подготовка
        start = start_manager()
        start.start()
        repo = reposity_manager()
        repo.file_name = "dump.json"

        # Действие
        result = repo.save()

        # Проверки
        assert result == True



          
if __name__ == '__main__':
    unittest.main()  