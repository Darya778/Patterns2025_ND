from Src.Core.abstract_dto import abstract_dto

# Модель транзакции (dto)
# Пример
#                "id":"adb7510f-687d-428f-a697-26e53d3f65b7",
#                "storage_id":"b4bb3bc7-1481-4485-85bf-0b1d68b76a89",
#                "nomenclature_id":"ba477cfd-a200-4b94-ab87-73bf29d37563",
#                "range_id":"43dc2db4-c4c8-4900-9b02-4355408befb4"
class rest_dto(abstract_dto):
    __storage_id:str = ""
    __range_id:str = ""
    __nomenclature_id:str = ""
    __value:float = 0.0

    # Код склада
    @property
    def storage_id(self) -> str:
        return self.__storage_id
    
    @storage_id.setter
    def storage_id(self, value:str):
        self.__storage_id = value.strip()

    # Код единицы измерения
    @property
    def range_id(self) -> str:
        return self.__range_id
    
    @range_id.setter
    def range_id(self, value:str):
        self.__range_id = value.strip()

    # Код номенклатуры
    @property
    def nomenclature_id(self) -> str:
        return self.__nomenclature_id
    
    @nomenclature_id.setter
    def nomenclature_id(self, value:str):
        self.__nomenclature_id = value.strip()

    # Значение
    @property
    def value(self) -> float:
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

