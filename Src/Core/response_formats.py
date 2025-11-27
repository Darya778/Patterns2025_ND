

"""
Типы форматов данных для вывода данных Api
"""
class response_formats:

    """
    Формат ответа csv
    """
    @staticmethod
    def csv() -> str:
        return "csv"
    

    """
    Формат ответа json
    """
    @staticmethod
    def json() -> str:
        return "json"
    
    """
    Формат ответа markdown
    """
    @staticmethod
    def markdown() -> str:
        return "markdown"
    
    
    """
    Статический метод возвращает список всех поддерживаемых форматов данных
    """
    @staticmethod
    def list_all_formats():
        # Получаем имена всех методов класса
        methods = dir(response_formats)
        
        # Фильтруем методы, выбирая только нужные (начинающиеся с имени метода)
        formats = []
        for method_name in methods:
            if not method_name.startswith('__') and method_name != 'list_all_formats':
                format_value = getattr(response_formats, method_name)()
                formats.append(format_value)
                
        return formats
