from Src.Core.abstract_response import abstract_response
from Src.Core.common import common


"""
Класс для формирования данных в формате Csv
"""
class response_csv(abstract_response):

    # Сформировать
    def build(self, data: list) -> str:
        text = super().build( data)

        # Шапка
        item = data [ 0 ]
        fields = common.get_fields( item )
        for field in fields:
            text += f"{field};"

        text = text[:-1] + '\n'
        
        # Данные
        for obj in data:
            for field in fields:
                value = getattr(obj, field)
                text += f"{value};"
            text = text[:-1] + '\n'

        return text.strip() 

