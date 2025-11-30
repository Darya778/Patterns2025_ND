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
    @staticmethod
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
    @staticmethod
    def rest_key():
        return "rest_key"
    
    """
    Получить список всех ключей
    Источник: https://github.com/Alyona1619
    """
    @staticmethod
    def keys() -> list:
        result = []
        methods = [
            method for method in dir(reposity_manager)
            if callable(getattr(reposity_manager, method)) and method.endswith("_key")
        ]

        for method in methods:
            key = getattr(reposity_manager, method)()
            result.append(key)

        return result
    
    """
    Инициализация
    """
    def initalize(self):
        for key in reposity_manager.keys():
            self.__data[key] = []


    """
    Загрузить данные
    """
    def load(self) -> bool:
        if getattr(self, "file_name", "") == "":
            raise operation_exception("Не найден файл настроек!")

        try:
            with open(self.file_name, "r", encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            self.initalize()
            return False

        try:
            raw_data = json.loads(text)
        except Exception:
            raise operation_exception("Ошибка чтения JSON из файла!")

        for key in reposity_manager.keys():
            self.data[key] = raw_data.get(key, [])

        return True

    """
    Сохранить данные
    """
    def save(self) -> bool:
        if getattr(self, "file_name", "") == "":
            raise operation_exception("Не найден файл настроек!")

        factory = convert_factory()
        result = {}

        for key in reposity_manager.keys():
            models = self.__data.get(key, [])
            dto_objects = common.models_to_dto(models)
            result[key] = factory.serialize(dto_objects)

        text = json.dumps(result, ensure_ascii=False, indent=4)

        try:
            with open(self.file_name, "w", encoding="utf-8") as f:
                f.write(text)
            return True
        except Exception:
            return False
