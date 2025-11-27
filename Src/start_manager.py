from Src.reposity_manager import reposity_manager
from Src.Models.range_model import range_model
from Src.Models.group_model import group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Core.validator import validator, argument_exception, operation_exception
import json
from Src.Models.receipt_model import receipt_model
from Src.Models.receipt_item_model import receipt_item_model
from Src.Dtos.nomenclature_dto import nomenclature_dto
from Src.Dtos.range_dto import range_dto
from Src.Dtos.category_dto import category_dto
from Src.Dtos.storage_dto import storage_dto
from Src.Models.storage_model import storage_model
from Src.Models.transaction_model import transaction_model
from Src.Dtos.transaction_dto import transaction_dto
from Src.Core.abstract_manager import abstract_manager
from Src.Dtos.receipt_dto import receipt_dto

class start_manager(abstract_manager):
    # Репозиторий
    __repo: reposity_manager = reposity_manager()

    # Словарь который содержит загруженные и инициализованные инстансы нужных объектов
    # Ключ - id записи, значение - abstract_model
    __cache = {}

    # Описание ошибки
    __error_message:str = ""

    def __init__(self):
        self.__repo.initalize()

    # Singletone
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(start_manager, cls).__new__(cls)
        return cls.instance 


    # Информация об ошибке    
    @property
    def error_message(self) -> str:
        return self.__error_message    


    # Загрузить стартовые данные из файла
    def load(self) -> bool:
        if self.file_name == "":
            raise operation_exception("Не найден файл с данными по умолчанию!")

        try:
            with open( self.file_name, 'r') as file_instance:
                data = json.load(file_instance)
                return self.deserialize(data)
        except Exception as e:
            self.__error_message = str(e)
            return False
        
        
    # Сохранить элемент в репозитории
    def __save_item_to_reposity(self, key:str, dto, item):
        validator.validate(key, str)
        item.unique_code = dto.id
        self.__cache.setdefault(dto.id, item)
        self.__repo.data[ key ].append(item)

    # Загрузить единицы измерений   
    def __deserialize_ranges(self, data: dict) -> bool:
        validator.validate(data, dict)
        ranges = data['ranges'] if 'ranges' in data else []    
        if len(ranges) == 0:
            return False
         
        for range in ranges:
            dto = range_dto().create(range)
            item = range_model.from_dto(dto, self.__cache)
            self.__save_item_to_reposity( reposity_manager.range_key(), dto, item )

        return True

    # Загрузить группы номенклатуры
    def __deserialize_groups(self, data: dict) -> bool:
        validator.validate(data, dict)
        categories =  data['categories'] if 'categories' in data else []    
        if len(categories) == 0:
            return False

        for category in  categories:
            dto = category_dto().create(category)    
            item = group_model.from_dto(dto, self.__cache )
            self.__save_item_to_reposity( reposity_manager.group_key(), dto, item )

        return True
    
    # Загрузить склады
    def __deserialize_storages(self, data:dict) -> bool:
        validator.validate(data, dict)
        storages = data['storages'] if 'storages' in data else []    
        if len(storages) == 0:
            return False
        
        for storage in storages:
            dto = storage_dto().create(storage)
            item = storage_model.from_dto(dto, self.__cache )
            self.__save_item_to_reposity( reposity_manager.storage_key(), dto, item )

        return True    

    # Загрузить тестовые транзакции
    def __deserialize_transactions(self, data:list) -> bool:
        validator.validate(data, list)
        if len(data) == 0:
            return False
        
        for transaction in data:
            dto = transaction_dto().create(transaction)
            item = transaction_model.from_dto(dto, self.__cache )
            self.__save_item_to_reposity( reposity_manager.transaction_key(), dto, item )

        return True    

    # Загрузить номенклатуру
    def __deserialize_nomenclatures(   self, data: dict) -> bool:
        validator.validate(data, dict)      
        nomenclatures = data['nomenclatures'] if 'nomenclatures' in data else []   
        if len(nomenclatures) == 0:
            return False
         
        for nomenclature in nomenclatures:
            dto = nomenclature_dto().create(nomenclature)
            item = nomenclature_model.from_dto(dto, self.__cache)
            self.__save_item_to_reposity( reposity_manager.nomenclature_key(), dto, item )

        return True        

    # Обработать справочники
    def __deserialize_references(self, data:dict) -> bool:
        validator.validate(data, dict)

        try:
            self.__deserialize_ranges(data)
            self.__deserialize_groups(data)
            self.__deserialize_nomenclatures(data) 
            self.__deserialize_storages(data)       
            return True
        except Exception as e:
            self.__error_message = str(e)
            return False

    # Загрузить рецепты
    def __deserialize_receipts(self, data:list) -> bool:
        validator.validate(data, list)

        if len(data) == 0:
            return False
         
        for receipt in data:
            dto = receipt_dto().create(receipt)
            item = receipt_model.from_dto(dto, self.__cache)
            self.__save_item_to_reposity( reposity_manager.receipt_key(), dto, item )
            return True
            

    # Обработать полученный словарь    
    def deserialize(self, data: dict) -> bool:
        validator.validate(data, dict)
        loaded_references = True
        loaded_receipts = True
        loaded_transactions = True

        # Обработать справочники
        if "default_refenences" in data.keys():
                default_refenences = data["default_refenences"]
                loaded_references = self.__deserialize_references(default_refenences)

        # Обработать рецепты
        if "default_receipts" in data.keys():
                default_receipts = data["default_receipts"]
                loaded_receipts = self.__deserialize_receipts(default_receipts)  

        # Загрузить транзакции
        if "default_transactions" in data.keys():
                default_transactions = data["default_transactions"]
                loaded_transactions = self.__deserialize_transactions(default_transactions)             

        return loaded_references and loaded_receipts and loaded_transactions

    """
    Стартовый набор данных
    """
    @property
    def data(self):
        return self.__repo.data   

    """
    Основной метод для генерации эталонных данных
    """
    def start(self):
        self.file_name = "default.json"
        result = self.load()
        if result == False:
            raise operation_exception(f"Невозможно сформировать стартовый набор данных!\nОписание: {self.error_message}") 
        

