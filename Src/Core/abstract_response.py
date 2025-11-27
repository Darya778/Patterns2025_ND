import abc
from Src.Core.validator import validator, operation_exception

# Абстрактный класс для фолрмирования ответов
class abstract_response(abc.ABC):
    
    # Сформировать нужный ответ
    @abc.abstractmethod
    def build(self, data: list) -> str:
        validator.validate(data, list )

        if len(data) == 0:
            raise operation_exception("Нет данных!")

        return ""