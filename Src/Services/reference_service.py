from typing import Any, Dict, List, Type, Tuple

from Src.Core.abstract_logic import abstract_logic
from Src.Core.prototype import prototype
from Src.Core.observe_service import observe_service
from Src.Core.validator import validator, operation_exception, argument_exception

from Src.reposity_manager import reposity_manager

from Src.Dtos.nomenclature_dto import nomenclature_dto
from Src.Dtos.range_dto import range_dto
from Src.Dtos.category_dto import category_dto
from Src.Dtos.storage_dto import storage_dto
from Src.Dtos.event_dto import event_dto

from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model
from Src.Models.group_model import group_model
from Src.Models.storage_model import storage_model

class reference_factory:
    """
    Простая фабрика для создания моделей из DTO.
    Отделяет знание о типах от сервиса.
    """
    _mapping: Dict[str, Tuple[Type, Type]] = {
        "nomenclature": (nomenclature_dto, nomenclature_model),
        "range": (range_dto, range_model),
        "unit": (range_dto, range_model),
        "group": (category_dto, group_model),
        "category": (category_dto, group_model),
        "storage": (storage_dto, storage_model),
        "warehouse": (storage_dto, storage_model),
    }

    @staticmethod
    def normalize(type_name: str) -> str:
        return (type_name or "").strip().lower()

    @classmethod
    def resolve(cls, reference_type: str) -> Tuple[Type, Type]:
        norm = cls.normalize(reference_type)

        for key, pair in cls._mapping.items():
            if norm == key or norm.startswith(key):
                return pair
        raise argument_exception(f"Unknown reference_type: {reference_type}")

    @staticmethod
    def model_to_dto(model_obj: Any, dto_cls: Type):
        return dto_cls(
            **{
                field: getattr(model_obj, field)
                for field in dto_cls.__annotations__.keys()
                if hasattr(model_obj, field)
            }
        )

    @staticmethod
    def dto_to_model(dto_obj: Any, model_cls: Type):
        return model_cls(
            **{
                field: getattr(dto_obj, field)
                for field in dto_obj.__dict__.keys()
                if not field.startswith("_")
            }
        )

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
        Возвращает ключ репозитория по типу справочника
        """
        norm = reference_factory.normalize(reference_type)

        if "nomen" in norm:
            return self._repo.nomenclature_key()
        if "range" in norm or norm in ("unit", "units"):
            return self._repo.range_key()
        if "group" in norm or "category" in norm:
            return self._repo.group_key()
        if "stor" in norm or "warehouse" in norm:
            return self._repo.storage_key()

        raise argument_exception(f"Unknown reference type: {reference_type}")

    def get(self, reference_type: str, item_id: str = None, filter_dto=None) -> List[Any]:
        """
        Получение элементов справочника:
        - item_id: если указан, вернет конкретный элемент
        - filter_dto: если указан, применяет фильтр через prototype
        """
        dto_cls, _ = self._factory.resolve(reference_type)
        key = self._map_type_to_repo_key(reference_type)

        models: List[Any] = list(self._repo.data.get(key, []))
        dtos = [self._factory.model_to_dto(m, dto_cls) for m in models]

        if item_id:
            return [x for x in dtos if getattr(x, "unique_code", None) == item_id]

        if filter_dto:
            return prototype.filter(dtos, filter_dto)

        return dtos

    def add(self, reference_type: str, dto) -> Any:
        """
        Добавление нового элемента справочника
        """
        dto_cls_name, model_cls_name = self._factory.resolve(reference_type)
        dto_cls = globals().get(dto_cls_name)
        if dto_cls is None:
            raise argument_exception("DTO class not found for type")
        validator.validate(dto, dto_cls)

        repo_key = self._map_type_to_repo_key(reference_type)
        unique = getattr(dto, "unique_code", None)
        for m in self._repo.data.get(repo_key, []):
            if getattr(m, "unique_code", None) == unique:
                raise operation_exception(f"Item with unique_code '{unique}' already exists")

        model_cls = globals().get(model_cls_name)
        model_obj = self._factory.dto_to_model(dto, model_cls) if model_cls else dto

        self._repo.data.setdefault(repo_key, []).append(model_obj)

        evt = event_dto("reference_added", dto)
        self._observer.create_event(evt)
        return dto

    def update(self, reference_type: str, item_id: str, dto_updates) -> Any:
        """
        Частичное обновление элемента справочника
        """
        dto_cls, model_cls = self._factory.resolve(reference_type)
        repo_key = self._map_type_to_repo_key(reference_type)

        models = self._repo.data.get(repo_key, [])
        target = next((m for m in models if getattr(m, "unique_code", None) == item_id), None)

        if not target:
            raise operation_exception(f"Item '{item_id}' not found")

        for field, value in dto_updates.__dict__.items():
            if not field.startswith("_") and hasattr(target, field):
                setattr(target, field, value)

        updated_dto = self._factory.model_to_dto(target, dto_cls)
        self._observer.create_event("reference_updated", updated_dto)
        return updated_dto

    def delete(self, reference_type: str, item_id: str) -> bool:
        """
        Удаление элемента справочника
        Если элемент используется в других сущностях, выбрасывается ошибка
        """
        repo_key = self._map_type_to_repo_key(reference_type)
        dto_cls, _ = self._factory.resolve(reference_type)

        models = self._repo.data.get(repo_key, [])
        target = next((m for m in models if getattr(m, "unique_code", None) == item_id), None)

        if not target:
            raise operation_exception(f"Item '{item_id}' not found")

        dto_obj = self._factory.model_to_dto(target, dto_cls) if dto_cls else target

        validation_evt = event_dto("reference_delete_validation", dto_obj)
        self._observer.create_event(validation_evt)

        self._repo.data[repo_key] = [m for m in models if getattr(m, "unique_code", None) != item_id]

        deleted_evt = event_dto("reference_deleted", dto_obj)
        self._observer.create_event(deleted_evt)
        return True

