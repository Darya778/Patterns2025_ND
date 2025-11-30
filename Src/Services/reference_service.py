import json
from datetime import datetime
from typing import Any, Dict, List, Optional

from Src.Core.abstract_logic import abstract_logic
from Src.Core.prototype import prototype
from Src.Core.observe_service import observe_service
from Src.reposity_manager import reposity_manager
from Src.Core.validator import validator, operation_exception, argument_exception

from Src.Dtos.nomenclature_dto import nomenclature_dto
from Src.Dtos.range_dto import range_dto
from Src.Dtos.category_dto import category_dto
from Src.Dtos.storage_dto import storage_dto

from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model
from Src.Models.group_model import group_model
from Src.Models.storage_model import storage_model

SETTINGS_FILE = "appsettings.json"

class reference_factory:
    """
    Простая фабрика для создания моделей из DTO.
    Отделяет знание о типах от сервиса.
    """
    mapping = {
        "nomenclature": (nomenclature_dto, nomenclature_model),
        "range": (range_dto, range_model),
        "unit": (range_dto, range_model),
        "group": (category_dto, group_model),
        "category": (category_dto, group_model),
        "storage": (storage_dto, storage_model),
        "warehouse": (storage_dto, storage_model)
    }

    @staticmethod
    def normalise_type(reference_type: str) -> str:
        return (reference_type or "").strip().lower()

    @classmethod
    def resolve(cls, reference_type: str):
        t = cls.normalise_type(reference_type)
        for k in cls.mapping:
            if t == k or t.startswith(k):
                return cls.mapping[k]
        return None

class reference_service(abstract_logic):
    """
    Сервис для работы со справочниками:
    - nomenclature (номенклатура)
    - range (единицы измерения)
    - group (группы/категории)
    - storage (склады)

    Функциональность:
    - Добавление, изменение, удаление элементов
    - Получение списка или отдельного элемента
    - Использует prototype для фильтрации
    - Логирует изменения в settings (appsettings.json)
    - Отправляет события через observe_service
    """

    def __init__(self, repo: reposity_manager = None, observer=observe_service, factory: reference_factory = None):
        self._repo = repo or reposity_manager()
        self._observer = observer
        self._factory = factory or reference_factory()

    def _map_type_to_repo_key(self, reference_type: str) -> str:
        """
        Определяет ключ репозитория по типу справочника
        """
        t = reference_factory.normalise_type(reference_type)
        rm = self._repo

        if "nomen" in t:
            return rm.nomenclature_key()
        if "range" in t or t in ("unit", "units"):
            return rm.range_key()
        if "group" in t or "category" in t:
            return rm.group_key()
        if "stor" in t or "warehouse" in t:
            return rm.storage_key()

        raise argument_exception(f"Unknown reference type: {reference_type}")

    def get(self, reference_type: str, item_id: str = None, filter_dto=None) -> List[Any]:
        """
        Получение элементов справочника:
        - item_id: если указан, вернет конкретный элемент
        - filter_dto: если указан, применяет фильтр через prototype
        """
        key = self._map_type_to_repo_key(reference_type)
        data = list(self._repo.data.get(key, []))

        if item_id:
            return [x for x in data if getattr(x, "unique_code", None) == item_id]

        if filter_dto is not None:
            return prototype.filter(data, filter_dto)

        return data

    def add(self, reference_type: str, dto) -> Any:
        """
        Добавление нового элемента справочника
        """
        validator.validate(dto, object)
        resolved = self._factory.resolve(reference_type)
        if not resolved:
            raise argument_exception("Unsupported reference type")
        dto_cls, model_cls = resolved
        validator.validate(dto, dto_cls)

        key = self._map_type_to_repo_key(reference_type)

        instance = model_cls(**{k: getattr(dto, k) for k in dto.__dict__ if not k.startswith('_')})
        self._repo.data.setdefault(key, []).append(instance)

        payload = {
            "type": reference_type,
            "action": "add",
            "id": getattr(instance, "unique_code", None),
            "ts": datetime.utcnow().isoformat()
        }

        try:
            self._observer.create_event("reference_added", {"type": reference_type, "item": instance, "meta": payload})
        except Exception:
            pass

        return instance

    def update(self, reference_type: str, item_id: str, partial_payload: Dict[str, Any]) -> Any:
        """
        Частичное обновление элемента справочника
        """
        key = self._map_type_to_repo_key(reference_type)
        arr = self._repo.data.get(key, [])
        target = next((x for x in arr if getattr(x, "unique_code", None) == item_id), None)

        if target is None:
            raise operation_exception(f"Item {item_id} not found in {reference_type}")

        for k, v in (partial_payload or {}).items():
            if hasattr(target, k):
                setattr(target, k, v)

        payload = {
            "type": reference_type,
            "action": "update",
            "id": item_id,
            "payload": partial_payload,
            "ts": datetime.utcnow().isoformat()
        }

        try:
            self._observer.create_event("reference_updated", {"type": reference_type, "id": item_id,
                                                              "payload": partial_payload, "meta": payload})
        except Exception:
            pass

        return target

    def delete(self, reference_type: str, item_id: str) -> bool:
        """
        Удаление элемента справочника
        Если элемент используется в других сущностях, выбрасывается ошибка
        """
        key = self._map_type_to_repo_key(reference_type)
        arr = self._repo.data.get(key, [])
        target = next((x for x in arr if getattr(x, "unique_code", None) == item_id), None)

        if target is None:
            raise operation_exception(f"Item {item_id} not found in {reference_type}")

        if key == reposity_manager.nomenclature_key():
            for r in self._repo.data.get(reposity_manager.receipt_key(), []):
                try:
                    for comp in getattr(r, "composition", []):
                        if comp.get("nomenclature_id") == item_id:
                            raise operation_exception(
                                f"Cannot delete nomenclature {item_id}: used in receipt {getattr(r, 'unique_code', None)}"
                            )
                except Exception:
                    pass

            for t in self._repo.data.get(reposity_manager.transaction_key(), []):
                if getattr(t, "nomenclature_id", None) == item_id:
                    raise operation_exception(
                        f"Cannot delete nomenclature {item_id}: used in transaction {getattr(t, 'unique_code', None)}"
                    )

        self._repo.data[key] = [x for x in arr if getattr(x, "unique_code", None) != item_id]

        payload = {
            "type": reference_type,
            "action": "delete",
            "id": item_id,
            "ts": datetime.utcnow().isoformat()
        }

        try:
            self._observer.create_event("reference_deleted",
                                        {"type": reference_type, "id": item_id, "meta": payload})
        except Exception:
            pass

        return True

