from Src.Core.entity_model import entity_model
from Src.Core.validator import validator
from Src.Dtos.storage_dto import storage_dto


"""
Модель склада
"""
class storage_model(entity_model):
    __address:str = ""

    """
    Адрес
    """
    @property
    def address(self) -> str:
        return self.__address.strip()
    
    @address.setter
    def address(self, value:str):
        validator.validate(value, str)
        self.__address = value.strip()


    """
    Фабричный метод из Dto
    """
    @staticmethod
    def from_dto(dto:storage_dto, cache:dict):
        validator.validate(dto, storage_dto)
        validator.validate(cache, dict)
        item = storage_model()
        item.name = dto.name
        item.address = dto.address
        item.unique_code = dto.id
        return item
    

    """
    Фабричный метод для первода в dto
    """
    def to_dto(self) -> storage_dto:
        dto = storage_dto()
        dto.name = self.name
        dto.address = self.address
        dto.id = self.unique_code
        return dto

    