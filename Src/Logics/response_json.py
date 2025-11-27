from Src.Core.abstract_response import abstract_response
from Src.Logics.convert_factory import convert_factory

# Преобразовать список в Json
class response_json(abstract_response):
    
    # Сформировать 
    def build(self, data: list) -> str:
        text = super().build( data )
        factory = convert_factory()
        result = factory.serialize(data)
        return result
