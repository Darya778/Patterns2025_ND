from Src.Core.abstract_logic import abstract_logic
from Src.Core.observe_service import observe_service
from Src.Core.event_type import event_type

class print_service(abstract_logic):

    def __init__(self):
        super().__init__()

        # Подключение в наблюдение
        observe_service.add(self)

    """
    Обработка событий
    """
    def handle(self, event:str, params):
        super().handle(event, params)  

        if   event == event_type.convert_to_json():
            print( f"params:{ params } ")