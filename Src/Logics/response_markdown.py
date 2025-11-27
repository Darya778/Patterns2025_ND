from Src.Core.abstract_response import abstract_response
from Src.Core.common import common


"""
Сформировать ответ в виде Markdown формата
"""
class response_markdown(abstract_response):

    # Сформировать 
    def build(self, data: list) -> str:
        text = super().build( data )

        # Получаем первое значение для составления заголовков
        first_item = data[0]
        type_name = first_item.__class__.__name__
        text += f"#{type_name}\n"        
        fields = common.get_fields(first_item)

        # Формирование шапки таблицы
        text += "| "
        text += " | ".join(fields)
        text += " |\n"

        # Разделительная линия под шапкой
        text += "|-" * len(fields) + "|\n"

        # Перебор данных и построение тела таблицы
        for item in data:
            row_values = [str(getattr(item, field)) for field in fields]
            text += "| " + " | ".join(row_values) + " |\n"

        return text