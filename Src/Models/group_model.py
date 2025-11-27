from Src.Core.entity_model import entity_model
from Src.Core.abstract_dto import abstract_dto
from Src.Dtos.category_dto import category_dto

"""
Модель группы номенклатуры
"""
class group_model(entity_model):
   

    """
    Фабричный метод из Dto
    """
    @staticmethod
    def from_dto(dto:abstract_dto, cache:dict):
        item  = group_model()
        item.name = dto.name
        item.unique_code = dto.id
        return item
    
    """
    Перевести доменную модель в Dto
    """
    def to_dto(self) -> category_dto:
        dto = category_dto()
        dto.name = self.name
        dto.id = self.unique_code
        return dto



    
    

    


    
