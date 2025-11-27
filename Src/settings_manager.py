from Src.Models.settings_model import settings_model
from Src.Core.validator import operation_exception
from Src.Core.validator import validator
from Src.Models.company_model import company_model
from Src.Core.common import common
from Src.Core.response_formats import response_formats
import json
from datetime import datetime
from Src.Core.abstract_manager import abstract_manager

####################################################3
# Менеджер настроек. 
# Предназначен для управления настройками и хранения параметров приложения
class settings_manager(abstract_manager):

    # Настройки
    __settings:settings_model = None

    # Singletone
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance 
    
    def __init__(self):
        self.__set_default()

    # Текущие настройки
    @property
    def settings(self) -> settings_model:
        return self.__settings

    # Загрузить настройки из Json файла
    def load(self) -> bool:
        if self.file_name == "":
            raise operation_exception("Не найден файл настроек!")

        try:
            with open( self.file_name, 'r') as file_instance:
                settings = json.load(file_instance)

                # Реквизиты оргаизации
                if "company" in settings.keys():
                    data = settings["company"]
                    result = self.__deserialize(data)
                
                # Формат по умолчанию
                if "default_format" in settings.keys() and result == True:
                    data = settings["default_format"]
                    if data in response_formats.list_all_formats():
                        self.settings.default_response_format = data

                # Дата блокировки
                if "block_period" in settings.keys() and result == True:
                    data = settings["block_period"]
                    date_format = "%Y-%m-%d"
                    date = datetime.strptime(data, date_format)
                    self.__settings.block_period = date
                return result
            return False
        except:
            return False
        
    # Обработать полученный словарь    
    def __deserialize(self, data: dict) -> bool:
        validator.validate(data, dict)

        fields = common.get_fields(self.__settings.company)
        matching_keys = list(filter(lambda key: key in fields, data.keys()))

        try:
            for key in matching_keys:
                setattr(self.__settings.company, key, data[key])
        except:
            return False        

        return True

    # Параметры настроек по умолчанию
    def __set_default(self):
        company = company_model()
        company.name = "Рога и копыта"
        company.inn = -1
        
        self.__settings = settings_model()
        self.__settings.company = company

        



