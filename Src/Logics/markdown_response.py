from Src.Core.abstract_response import abstract_response
from Src.Core.validator import  argument_exception
from Src.Core.common import common

class markdown_response(abstract_response):

    """
    Сформитровать данные в формате markdown
    """
    def build(self,  data: list) -> str:
        if len(data) == 0:
            raise argument_exception("Некоррекно переданы параметры!")

        result = ""
        for item in data:
            result = self.__build_item(item)

        return result    


    """
    Сформировать данные по одному элементу
    """
    def __build_item(self, item) -> str:
        if item is None:   
            return ""
        
        # Заголовок
        caption = type(item).__name__
        result = f"#{caption}"
        fields = common.get_fields(item)

        # Формирование заголовков столбцов таблицы
        headers_row = "|".join(fields)
        result += f"|{headers_row}|\n"

        # Добавляем разделительную линию
        separator_line = ":-" * len(fields)
        result += f"|{separator_line}|\n"

        # Заполняем строки значениями полей
        values_row = []
        for field in fields:
            value = getattr(item, field)
            values_row.append(str(value))
        
        values_row_str = "|".join(values_row)
        result += f"|{values_row_str}|\n"
        return result


        