import abc
from Src.Core.abstract_dto import abstract_dto
from Src.Core.abstact_convert import abstract_convert
from Src.Core.abstract_logic import abstract_logic
from Src.Core.common import common
from Src.Core.validator import validator, operation_exception, argument_exception
from datetime import datetime
from Src.Core.observe_service import observe_service
from Src.Core.event_type import event_type

# Подключаем dto
from Src.Dtos.category_dto import category_dto
from Src.Dtos.nomenclature_dto import nomenclature_dto
from Src.Dtos.range_dto import range_dto
from Src.Dtos.rest_dto import rest_dto
from Src.Dtos.storage_dto import storage_dto
from Src.Dtos.transaction_dto import transaction_dto


"""
Конвертация простого объекта
"""
class basic_convertor(abstract_convert):
   
   def serialize(self, field: str, object) -> dict:
      super().serialize( field, object)
      
      if not isinstance(object, (int, str, bool, float)):
          self.error_text = f"Некорректный тип данных передан для конвертации. Ожидается: (int, str, bool). Передан: {type(object)}"
          return None

      try:
            return { field: object }
      except Exception as ex:
            self.set_exception(ex)  

      return None   
   

"""
Конвертация перечисления
"""
class enum_convertor(abstract_convert):
   def serialize(self, field: str, object) -> dict:
      super().serialize( field, object)
      
      try:
            return { field: object.value }
      except Exception as ex:
            self.set_exception(ex)  

      return None   

"""
Конвертация даты
"""
class datetime_convertor(abstract_convert):

    def serialize(self, field: str,  object):
      
        super().serialize( field, object)

        if not isinstance(object, datetime):
          self.error_text = f"Некорректный тип данных передан для конвертации. Ожидается: datetime. Передан: {type(object)}"
          return None

        try:
            return {  field: object.strftime('%Y-%m-%d %H:%M') }
        except Exception as ex:
            self.set_exception(ex)    

"""
Конвертация в словарь ссылочного объекта
"""
class reference_convertor(abstract_convert):
    
    def serialize(self, field: str, object: abstract_dto) -> dict:
        super().serialize(field, object)

        factory = convert_factory()
        return factory.serialize(object)
    
"""
Фабрика для конвертиации моделей в словарь
"""    
class convert_factory(abstract_logic):
    _maps = {}
    
    def __init__(self) -> None:
        # Связка с простыми типами
        self._maps[datetime] = datetime_convertor
        self._maps[int] = basic_convertor
        self._maps[float] = basic_convertor
        self._maps[str] = basic_convertor
        self._maps[bool] = basic_convertor
        
        # Связка для всех моделей
        for  inheritor in abstract_dto.__subclasses__():
            self._maps[inheritor] = reference_convertor    

        # Ввиду наследования
        self._maps[  transaction_dto  ] =    reference_convertor 

    """
    Выполнить сериализацию модели в данные
    """    
    def serialize(self, object) -> dict:
        # Сконвертируем данные как список
        result = self.__convert_list("data", object)
        if result is not None:
            return result
        
        # Сконвертируем данные как значение
        result = {}
        fields = common.get_fields(object)
        
        for field in fields:
            attribute = getattr(object.__class__, field)
            if isinstance(attribute, property):
                value = getattr(object, field)
                
                # Сконвертируем данные как список
                dictionary =  self.__convert_list(field, value)
                if dictionary is None:

                    # Сконвертируем данные как значение
                    dictionary = self.__convert_item(field, value)
                    
                if len(dictionary) == 1:
                    result[field] =  dictionary[field]
                else:
                    result[field] = dictionary       

        # Форпмируем событие о конвертации в Json  
        observe_service.create_event( event_type.convert_to_json(), result )  
        
        return result  
    
    """
    Сконвертировать значение в словарь
    """
    def __convert_item(self, field: str,  source):
        validator.validate(field, str)
        if source is None:
            return {field: None}
        
        if type(source) not in self._maps.keys():
            self.set_exception( operation_exception(f"Не возможно подобрать конвертор для типа {type(source)}"))

        # Определим конвертор
        convertor = self._maps[ type(source)]()
        dictionary = convertor.serialize( field, source )
        
        if convertor.is_error:
            self.set_exception( operation_exception(f"Ошибка при конвертации данных {convertor.error_text}"))
        
        return  dictionary


    """
    Сконвертировать списочные значения в словарь
    """        
    def __convert_list(self, field: str,  source) -> list:
        validator.validate(field, str)
        
        # Сконвертировать список
        if isinstance(source, list):
            result = []
            for item in source:
                if isinstance(item, str | int | float | bool):
                    result.append ( item )
                else:    
                    result.append( self.__convert_item( field,  item ))  
            
            return result 
        
        # Сконвертировать в словарь
        if isinstance(source, dict):
            result = {}
            for key in source:
                object = source[key]
                value = self.__convert_item( key,  object )
                result[key] = value
                
            return result    
        

