from Src.Core.abstract_manager import abstract_manager
from Src.Logics.convert_factory import convert_factory
from Src.Core.validator import operation_exception
from Src.Core.common import common
import json

"""
Репозиторий данных
"""
class reposity_manager(abstract_manager):
    __data = {}

    @property
    def data(self):
        return self.__data
    
    """
    Ключ для единц измерений
    """
    @staticmethod
    def range_key():
        return "range_model"
    

    """
    Ключ для категорий
    """
    @staticmethod
    def group_key():
        return "group_model"
    
    """
    Ключ для склада
    """
    @staticmethod
    def storage_key():
        return "storage_key"
        
    """
    Ключ для транзакций
    """    
    def transaction_key():
        return "transaction_key"    
    

    """
    Ключ для номенклатуры
    """
    @staticmethod
    def nomenclature_key():
        return "nomenclature_model"
    

    """
    Ключ для рецептов
    """
    @staticmethod
    def receipt_key():
        return "receipt_model"
    
    """
    Ключ для остатков
    """
    def rest_key():
        return "rest_key"
    
    """
    Получить список всех ключей
    Источник: https://github.com/Alyona1619
    """
    @staticmethod
    def keys() -> list:
        result = []
        methods = [method for method in dir(reposity_manager) if
                    callable(getattr(reposity_manager, method)) and method.endswith('_key')]
        for method in methods:
            key = getattr(reposity_manager, method)()
            result.append(key)

        return result

    
    """
    Инициализация
    """
    def initalize(self):
        keys = reposity_manager.keys()
        for key in keys:
            self.__data[ key ] = []


    """
    Загрузить данные
    """
    def load(self) -> bool:
        pass

    """
    Сохранить данные
    """
    def save(self) -> bool:
        if self.file_name == "":
            raise operation_exception("Не найден файл настроек!")

        result = {}
        factory = convert_factory() 
        
        # Формируем общий словарь
        for key in reposity_manager.keys():
            models = self.data[ key  ]
            dtos = common.models_to_dto( models)
            data = factory.serialize( dtos )
            result[ key ] = data

        # Сохраняю полученные данные
        text = json.dumps(result, ensure_ascii=False, indent=4)
        try:
            with open( self.file_name, 'w', encoding='utf-8') as file_instance:
                file_instance.write(text)
            return True
        except:
            return False    