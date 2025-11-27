from Src.Core.abstract_model import abstact_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model

# Модель элемента рецепта
class receipt_item_model(abstact_model):
    __nomenclature:nomenclature_model
    __range:range_model
    __value:int

    # Фабричный метод
    def create(nomenclature:nomenclature_model, range:range_model,  value:int):
        item = receipt_item_model()
        item.__nomenclature = nomenclature
        item.__range = range
        item.__value = value


    # TODO: Внимание! Тут нужно добавить свойства