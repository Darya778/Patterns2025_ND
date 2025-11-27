import abc
import os
from Src.Core.validator import validator, argument_exception

# Абстрактный класс предназначен для инкапсулирования логики сохранения и восстановления данных
class abstract_manager(abc.ABC):
    # Наименование файла (полный путь)
    __full_file_name:str = ""

    
    # Загрузить данные
    @abc.abstractmethod
    def load(self) -> bool:
        pass

    # Сохранить данные    
    def save(self) -> bool:
        pass

    # Текущий файл
    @property
    def file_name(self) -> str:
        return self.__full_file_name

    # Полный путь к файлу настроек
    @file_name.setter
    def file_name(self, value:str):
        validator.validate(value, str)
        full_file_name = os.path.abspath(value)        
        if os.path.exists(full_file_name):
            self.__full_file_name = full_file_name.strip()
        else:
            raise argument_exception(f'Не найден указанный файл {full_file_name}')