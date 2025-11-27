from Src.Core.abstract_dto import abstract_dto

# Модель 
class receipt_item_dto(abstract_dto):
    __nomenclature_id:str = ""
    __range_id:str = ""
    __value:int = 0

    @property
    def nomenclature_id(self) -> str:
        return self.__nomenclature_id
    
    @nomenclature_id.setter
    def nomenclature_id(self, value:str):
        self.__nomenclature_id = value

    @property
    def range_id(self) -> str:
        return self.__range_id
    
    @range_id.setter
    def range_id(self, value:str):
        self.__range_id = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value:int):
        self.__value = value