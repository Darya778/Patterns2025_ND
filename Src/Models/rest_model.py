from Src.Core.entity_model import entity_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.storage_model import storage_model
from Src.Models.range_model import range_model
from Src.Core.validator import validator, argument_exception
from Src.Dtos.rest_dto import rest_dto

"""
Модель остатка
"""
class rest_model(entity_model):
    
    __value:float = 0.0
    __range:range_model
    __nomenclature:nomenclature_model
    __storage:storage_model

    # Значение транзакции
    @property
    def value(self) -> float:
        return self.__value
    
    @value.setter
    def value(self, value):
        validator.validate(value, float)
        if value == 0:
            raise argument_exception("Некорректно указано значение!")
        
        self.__value = value

    # Единица измерения
    @property
    def range(self) -> range_model:
        return self.__range
    
    @range.setter
    def range(self, value:range_model):
        validator.validate(value, range_model)
        self.__range = value

    # Номенклатура
    @property
    def nomenclature(self) -> nomenclature_model:
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value):
        validator.validate(value, nomenclature_model)
        self.__nomenclature = value

    # Склад
    @property
    def storage(self) -> storage_model:
        return self.__storage
    
    @storage.setter
    def storage(self, value):
        validator.validate(value, storage_model)
        self.__storage = value


    """
    Фабричный метод из Dto
    """
    @staticmethod
    def from_dto(dto:rest_dto, cache:dict):
        validator.validate(dto, rest_dto)
        validator.validate(cache, dict)
        
        item = rest_model()
        item.range =  cache[ dto.range_id ] if dto.range_id in cache else None
        item.nomenclature =  cache[ dto.nomenclature_id ] if dto.nomenclature_id in cache else None
        item.storage =  cache[ dto.storage_id ] if dto.storage_id in cache else None
        item.value = dto.value
        item.unique_code = dto.id
        return item
    

    """
    Фабричный метод в dto
    """
    def to_dto(self) -> rest_dto:
        dto = rest_dto()
        dto.storage_id = self.storage.unique_code
        dto.nomenclature_id = self.nomenclature.unique_code
        dto.range_id = self.range.unique_code
        dto.id = self.unique_code
        return dto    