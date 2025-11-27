from Src.reposity_manager import reposity_manager
from Src.Models.settings_model import settings_model
from Src.settings_manager import settings_manager
from datetime import datetime
from Src.Core.prototype import prototype


# Сервис для расчета остатков
class rest_service:
    # Репозиторий
    __repo: reposity_manager = reposity_manager()

    # Текущие настройки
    __settings:settings_model = settings_manager().settings

    # Рассчитать остатки
    def calc(self) -> list:
        transactions = self.__repo.data[ reposity_manager.transaction_key() ]
        for storage in self.__repo.data[  reposity_manager.storage_key()  ]:
            items = prototype.clone(      )



