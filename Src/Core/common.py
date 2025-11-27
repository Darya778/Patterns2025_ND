from Src.Core.entity_model import entity_model
from Src.Core.abstract_model import abstact_model
from Src.Core.validator import argument_exception

# Набор статических общих методов
class common:

    """
    Получить список наименований всех моделей
    """
    @staticmethod
    def get_models() -> list:
        result = []
        for  inheritor in entity_model.__subclasses__():
            result.append(inheritor.__name__)

        return result  

    """
    Получить полный список полей любой модели
        - is_common = True - исключить из списка словари и списки
    """
    @staticmethod
    def get_fields(source, is_common: bool = False) -> list:
        if source is None:
            raise argument_exception("Некорректно переданы аргументы!")

        items = list(filter(lambda x: not x.startswith("_") , dir(source))) 
        result = []

        for item in items:
            attribute = getattr(source.__class__, item)
            if isinstance(attribute, property):
                value = getattr(source, item)

                # Флаг. Только простые типы и модели включать
                if is_common == True and (isinstance(value, dict) or isinstance(value, list) ):
                    continue

                result.append(item)

        return result
   

    """
    Сконвертировать список моделей в dto
    """
    @staticmethod
    def models_to_dto(items:list) -> list:
        result = []
        for item in items:
            if isinstance(item, abstact_model):
                result.append(  item.to_dto() )

        return result        
