from Src.Core.entity_model import entity_model
from Src.Core.validator import validator
from Src.Dtos.receipt_dto import receipt_dto

# Модель рецепта
class receipt_model(entity_model):
    # Количество порций
    __portions:int = 1

    # Шаги приготовления
    __steps:list = []

    # Состав
    __composition:list = []

    # Время приготовления
    __cooking_time:str = ""


    # Количество порций
    @property
    def portions(self) -> int:
        return self.__portions
    
    @portions.setter
    def portions(self, value:int):
        validator.validate(value, int)
        self.__portions = value

    # Шаги приготовления
    @property
    def steps(self) -> list:
        return self.__steps
    
    @steps.setter
    def steps(self, value:list):
        validator.validate(value, list)
        self.__steps = value
    
    # Состав
    @property
    def composition(self) -> list:
        return self.__composition
    
    # Время приготовления
    @property
    def cooking_time(self) -> str:
        return self.__cooking_time

    @cooking_time.setter
    def cooking_time(self, value:str):
        validator.validate(value, str)
        self.__cooking_time = value.strip()


    # Фабричный метод для создания нового рецепта
    # Состав и шаги уже созданы. Будут пустыми
    @staticmethod
    def create(name:str,cooking_time:str, portions:int ) -> "receipt_model":
        item = receipt_model()
        item.name = name
        item.cooking_time = cooking_time
        item.portions = portions
        return item    
    
    """
    Фабричный метод из Dto
    """
    @staticmethod
    def from_dto(dto:receipt_dto, cache:dict):
        validator.validate(dto, receipt_dto)
        validator.validate(cache, dict)

        item = receipt_model()
        item.cooking_time = dto.cooking_time
        item.portions = dto.portions
        item.steps = dto.steps

        
        return item
