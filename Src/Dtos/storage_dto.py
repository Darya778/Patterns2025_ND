from Src.Core.abstract_dto import abstract_dto
from Src.Core.validator import validator


# Модель склада (dto)
# Пример
#                "name":"Грамм",
#                "id":"adb7510f-687d-428f-a697-26e53d3f65b7",
#                "address":"ИГУ"
class storage_dto(abstract_dto):
    __address:str = ""


    @property
    def address(self) -> str:
        return self.__address
    
    @address.setter
    def address(self, value:str):
        validator.validate(value, str)
        self.__address = value.strip()


