from Src.Dtos.rest_dto import rest_dto

# Модель транзакции (dto)
# Пример
#                "id":"adb7510f-687d-428f-a697-26e53d3f65b7",
#                "period":"2025-10-01",
#                "storage_id":"b4bb3bc7-1481-4485-85bf-0b1d68b76a89",
#                "nomenclature_id":"ba477cfd-a200-4b94-ab87-73bf29d37563",
#                "range_id":"43dc2db4-c4c8-4900-9b02-4355408befb4"
class transaction_dto(rest_dto):
    __period:str = ""

    @property
    def period(self) -> str:
        return self.__period

    @period.setter
    def period(self, value:str):
        self.__period = value.strip()



