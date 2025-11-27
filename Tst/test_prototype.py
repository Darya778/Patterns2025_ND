import unittest
from Src.Core.prototype import prototype
from Src.Logics.prototype_report import prototype_report
from Src.start_manager import start_manager
from Src.reposity_manager import reposity_manager
from Src.Core.validator import operation_exception
from Src.Dtos.filter_dto import filter_dto

class test_prototype(unittest.TestCase):

    def test_any_prototype_filter(self):
        # Подготовка
        start = start_manager()
        start.start()
        start_prototype = prototype_report(  start.data [ reposity_manager.transaction_key() ] )
        nomenclatures = start.data [ reposity_manager.nomenclature_key() ]
        if len(nomenclatures) == 0:
            raise operation_exception("List is empty!")
        first_nomenclature = nomenclatures[0]

        # Действие
        next_prototype = start_prototype.filter_by_nomenclature( start_prototype, first_nomenclature )

        # Проверка
        assert len(next_prototype.data) > 0
        assert len(start_prototype.data) > 0
        assert len(start_prototype.data)  >= len(next_prototype.data)

    def test_any_prototype_universal_filter(self):
        # Подготовка
        start = start_manager()
        start.start()
        start_prototype = prototype_report(  start.data [ reposity_manager.nomenclature_key() ] )
        nomenclatures =  start_prototype.data
        if len(nomenclatures) == 0:
            raise operation_exception("List is empty!")

        first_nomenclature = nomenclatures[0]
        dto = filter_dto()
        dto.field_name = "name"
        dto.value = first_nomenclature.name

        # Действие
        next_prototype = start_prototype.filter( start_prototype, dto )

        # Проверка
        assert len(next_prototype.data) == 1 


     
  
if __name__ == '__main__':
    unittest.main()  