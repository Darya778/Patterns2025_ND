from Src.Core.abstract_dto import abstract_dto
from Src.Core.condition_type import condition_type
from Src.Core.validator import validator

# Фильтрация
class filter_dto(abstract_dto):
    __field_name:str = ""
    __value:str = ""
    __condition:condition_type = condition_type.EQUALS


    # Поле по которому формировать фильтрацию
    @property
    def field_name(self) -> str:
        return self.__field_name
    
    @field_name.setter
    def field_name(self, value:str):
        validator.validate(value, str)
        self.__field_name = value

    # Значение фильтра
    @property
    def value(self) -> str:
        return self.__value
    
    @value.setter
    def value(self, value:str):
        self.__value = value

    # Тип сравнения
    @property
    def condition(self) -> condition_type:
        return self.__condition
    
    @condition.setter
    def condition(self, value:condition_type):
        validator.validate(value, condition_type)
        self.__condition = value


    # Фабричный метод.    
    def create_equals_filter(field_name:str, value:str) -> "filter_dto":
        dto = filter_dto()
        dto.field_name = field_name
        dto.value = value
        dto.condition = condition_type.EQUALS
        return dto


    # Фабричный метод.
    def create_less_or_equals_filter(field_name:str, value:str) -> "filter_dto":
        dto = filter_dto()
        dto.field_name = field_name
        dto.value = value
        dto.condition = condition_type.LESSOREQUALS
        return dto



