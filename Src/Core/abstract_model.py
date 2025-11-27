from abc import ABC
import uuid
from Src.Core.validator import validator

"""
Абстрактный класс для наследования моделей
Содержит в себе только генерацию уникального кода
"""
class abstact_model(ABC):
    __unique_code:str

    def __init__(self) -> None:
        super().__init__()
        self.__unique_code = uuid.uuid4().hex

    """
    Уникальный код
    """
    @property
    def unique_code(self) -> str:
        return self.__unique_code
    
    @unique_code.setter
    def unique_code(self, value: str):
        validator.validate(value, str)
        self.__unique_code = value.strip()

    # Отдельный общий метод для формирования Dto структуры
    def to_dto(self):
        pass

    """
    Перегрузка штатного варианта сравнения
    """
    def __eq__(self, value) -> bool:
        if value is  None: return False
        if not isinstance(value, abstact_model): return False

        return self.unique_code == value.unique_code

