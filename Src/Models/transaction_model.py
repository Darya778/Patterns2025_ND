from datetime import datetime
from Src.Core.validator import validator
from Src.Dtos.transaction_dto import transaction_dto
from Src.Models.rest_model import rest_model

"""
Модель складской транзакции
"""
class transaction_model(rest_model):
    __period:datetime = datetime.now

    # Период
    @property
    def period(self) -> datetime :
        return self.__period

    @period.setter
    def period(self, value):
        validator.validate(value, datetime)
        self.__period = value


    """
    Фабричный метод из Dto
    """
    @staticmethod
    def from_dto(dto:transaction_dto, cache:dict):
        validator.validate(dto, transaction_dto)
        validator.validate(cache, dict)

        item = transaction_model()
        item.period =  datetime.strptime(dto.period, "%Y-%m-%d")
        item.range =  cache[ dto.range_id ] if dto.range_id in cache else None
        item.nomenclature =  cache[ dto.nomenclature_id ] if dto.nomenclature_id in cache else None
        item.storage =  cache[ dto.storage_id ] if dto.storage_id in cache else None
        item.value = dto.value
        item.unique_code = dto.id
        return item
    

    """
    Фабричный метод в dto
    """
    def to_dto(self) -> transaction_dto:
        dto = transaction_dto()
        dto.period = self.period.strftime("%Y-%m-%d")
        dto.storage_id = self.storage.unique_code
        dto.nomenclature_id = self.nomenclature.unique_code
        dto.range_id = self.range.unique_code
        dto.id = self.unique_code
        dto.value = self.value
        return dto    