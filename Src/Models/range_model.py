from Src.Core.entity_model import entity_model
from Src.Core.validator import validator, argument_exception
from Src.Dtos.range_dto import range_dto

"""
Модель единицы измерения
"""
class range_model(entity_model):
    __value:int = 1
    __base:'range_model' = None

    """
    Значение коэффициента пересчета
    """
    @property
    def value(self) -> int:
        return self.__value
    
    @value.setter
    def value(self, value: int):
        validator.validate(value, int)
        if value <= 0:
             raise argument_exception("Некорректный аргумент!")
        self.__value = value


    """
    Базовая единица измерения
    """
    @property
    def base(self):
        return self.__base
    
    @base.setter
    def base(self, value):
        self.__base = value

    """
    Киллограмм
    """
    @staticmethod
    def create_kill():
        inner_gramm = range_model.create_gramm()
        return range_model.create(  "киллограмм", inner_gramm)

    """
    Грамм
    """
    @staticmethod
    def create_gramm():
        return range_model.create("грамм")
     
    """
    Универсальный метод - фабричный
    """
    @staticmethod
    def create(name:str, value:int, base ):
        validator.validate(name, str)
        validator.validate(value, int)

        inner_base = None
        if not base is None: 
            validator.validate(base, range_model)
            inner_base = base
        item = range_model()
        item.name = name
        item.base = inner_base
        item.value = value
        return item
    
    """
    Фабричный метод из Dto
    """
    @staticmethod
    def from_dto(dto:range_dto, cache:dict):
        validator.validate(dto, range_dto)
        validator.validate(cache, dict)
        base  = cache[ dto.base_id ] if dto.base_id in cache else None
        item = range_model.create(dto.name, dto.value, base)
        return item
    

    """
    Фабричный метод для первода в dto
    """
    def to_dto(self) -> range_dto:
        dto = range_dto()
        dto.name = self.name
        dto.value = self.value
        dto.id = self.unique_code
        if self.base is not None:
            dto.base_id = self.base.unique_code
        return dto


    