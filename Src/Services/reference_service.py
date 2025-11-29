import json
from datetime import datetime
from typing import Any, Dict, List

from Src.Core.abstract_logic import abstract_logic
from Src.Core.prototype import prototype
from Src.Core.observe_service import observe_service
from Src.reposity_manager import reposity_manager
from Src.Core.validator import validator, operation_exception, argument_exception
from Src.Logics.rest_service import rest_service

from Src.Dtos.nomenclature_dto import nomenclature_dto
from Src.Dtos.range_dto import range_dto
from Src.Dtos.category_dto import category_dto
from Src.Dtos.storage_dto import storage_dto

from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model
from Src.Models.group_model import group_model
from Src.Models.storage_model import storage_model

try:
    from Src.Models.receipt_model import receipt_model
except Exception:
    receipt_model = None
try:
    from Src.Models.transaction_model import transaction_model
except Exception:
    transaction_model = None

SETTINGS_FILE = "appsettings.json"


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

    __repo: reposity_manager = reposity_manager()

    def __init__(self):
        observe_service.add(self)

    @staticmethod
    def _normalise_type(reference_type: str) -> str:
        return (reference_type or "").strip().lower()

    def _map_type_to_repo_key(self, reference_type: str) -> str:
        """
        Определяет ключ репозитория по типу справочника
        """
        t = self._normalise_type(reference_type)
        if t in ("nomenclature", "nomenclature_model", "nomenclatures", "nomen"):
            return reposity_manager.nomenclature_key() if hasattr(reposity_manager,
                                                                  "nomenclature_key") else "nomenclature_model"
        if t in ("range", "range_model", "unit", "units"):
            return reposity_manager.range_key() if hasattr(reposity_manager, "range_key") else "range_model"
        if t in ("group", "category", "group_model", "category_model"):
            return reposity_manager.group_key() if hasattr(reposity_manager, "group_key") else "group_model"
        if t in ("storage", "warehouse", "storage_model", "warehouse_model"):
            return reposity_manager.storage_key() if hasattr(reposity_manager, "storage_key") else "storage_model"
        raise argument_exception(f"Unknown reference type: {reference_type}")

    def _all_possible_repo_keys(self) -> List[str]:
        """
        Возвращает все возможные ключи репозиториев,
        включая рецепты, транзакции, балансы и обороты
        """
        keys = []
        if hasattr(reposity_manager, "receipt_key"):
            keys.append(reposity_manager.receipt_key())
        else:
            keys.extend(["receipt_model", "receipts", "recipe_model"])
        if hasattr(reposity_manager, "transaction_key"):
            keys.append(reposity_manager.transaction_key())
        else:
            keys.extend(["transaction_model", "transactions", "saved_turnovers"])
        keys.extend(["balance_model", "turnover_model", "saved_turnover", "balances", "turnovers"])
        # Убираем дубликаты
        seen = set()
        out = []
        for k in keys:
            if k not in seen:
                seen.add(k)
                out.append(k)
        return out

    def _save_settings(self, payload: Dict[str, Any]) -> None:
        """
        Сохраняет информацию о последнем изменении справочника
        в appsettings.json или через settings_manager, если он доступен
        """
        try:
            from Src.settings_manager import settings_manager
            sm = settings_manager()
            sm.settings.last_reference_change = payload
            if hasattr(sm, "save_to_file"):
                try:
                    sm.save_to_file(SETTINGS_FILE)
                    return
                except Exception:
                    pass
        except Exception:
            pass

        try:
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
            except Exception:
                cfg = {}
            cfg["last_reference_change"] = payload
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(cfg, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _get_repo_list(self, key: str) -> List[Any]:
        # Возвращает список элементов репозитория по ключу
        return self.__repo.data.get(key, [])

    def _is_used_elsewhere(self, item_id: str, exclude_repo_key: str = None) -> List[Dict[str, Any]]:
        """
        Проверяет, используется ли элемент в других сущностях
        exclude_repo_key — ключ репозитория, который нужно игнорировать
        """
        found = []
        for key, arr in list(self.__repo.data.items()):
            if exclude_repo_key and key == exclude_repo_key:
                continue
            for obj in arr:
                candidate_attrs = ["nomenclature", "nomenclature_id", "item", "unit", "range", "range_id",
                                   "category", "category_id", "group", "storage", "storage_id"]
                candidate_attrs += [a for a in dir(obj) if
                                    a in ("composition", "items", "composition_list", "_composition")]
                for attr in candidate_attrs:
                    if not hasattr(obj, attr):
                        continue
                    try:
                        val = getattr(obj, attr)
                        if val is None:
                            continue
                        if isinstance(val, (list, tuple)):
                            for sub in val:
                                if isinstance(sub, dict):
                                    if sub.get("nomenclature_id") == item_id:
                                        found.append({"repo_key": key, "container": obj, "attr": attr, "matched": sub})
                                else:
                                    if getattr(sub, "unique_code", None) == item_id:
                                        found.append({"repo_key": key, "container": obj, "attr": attr, "matched": sub})
                        else:
                            if getattr(val, "unique_code", None) == item_id or val == item_id:
                                found.append({"repo_key": key, "container": obj, "attr": attr, "matched": val})
                    except Exception:
                        continue
        return found

    def _update_dependencies_on_change(self, reference_type: str, item_id: str, updated_obj: Any) -> None:
        """
        Обновляет все ссылки на элемент в других моделях после его изменения
        Например, если изменился объект номенклатуры, обновляем все транзакции, рецепты и балансы
        """
        repo_keys = self._all_possible_repo_keys()
        receipt_keys = [k for k in repo_keys if "receipt" in k or "recipe" in k or "receipts" in k]
        transaction_keys = [k for k in repo_keys if
                            "transaction" in k or "transactions" in k or "saved_turnover" in k or "turnover" in k]

        # Обновляем состав рецептов
        for rk in receipt_keys:
            receipts = self.__repo.data.get(rk, [])
            for r in receipts:
                comp = getattr(r, "composition", None) or getattr(r, "_composition", None) or getattr(r, "items",
                                                                                                      None) or []
                if not comp:
                    continue
                for item in comp:
                    try:
                        nom = getattr(item, "nomenclature", None)
                        if nom and getattr(nom, "unique_code", None) == item_id:
                            item.nomenclature = updated_obj
                        if getattr(item, "unit", None) and getattr(item.unit, "unique_code", None) == item_id:
                            item.unit = updated_obj
                        if getattr(item, "storage", None) and getattr(item.storage, "unique_code", None) == item_id:
                            item.storage = updated_obj
                    except Exception:
                        continue

        # Обновляем транзакции
        for tk in transaction_keys:
            trans = self.__repo.data.get(tk, [])
            for t in trans:
                try:
                    if getattr(t, "nomenclature", None) and getattr(t.nomenclature, "unique_code", None) == item_id:
                        t.nomenclature = updated_obj
                    if getattr(t, "nomenclature_id", None) and t.nomenclature_id == item_id:
                        try:
                            t.nomenclature = updated_obj
                            if hasattr(t, "nomenclature_id"):
                                try:
                                    t.nomenclature_id = getattr(updated_obj, "unique_code", None)
                                except Exception:
                                    pass
                        except Exception:
                            pass
                    if getattr(t, "unit", None) and getattr(t.unit, "unique_code", None) == item_id:
                        t.unit = updated_obj
                    if getattr(t, "storage", None) and getattr(t.storage, "unique_code", None) == item_id:
                        t.storage = updated_obj
                except Exception:
                    continue

        # Обновляем балансы и обороты
        for k in self._all_possible_repo_keys():
            if "balance" in k or "turnover" in k or "saved_turnover" in k:
                arr = self.__repo.data.get(k, [])
                for entry in arr:
                    try:
                        if getattr(entry, "nomenclature", None) and getattr(entry.nomenclature, "unique_code",
                                                                            None) == item_id:
                            entry.nomenclature = updated_obj
                        if getattr(entry, "nomenclature_id", None) and entry.nomenclature_id == item_id:
                            entry.nomenclature = updated_obj
                        if getattr(entry, "unit", None) and getattr(entry.unit, "unique_code", None) == item_id:
                            entry.unit = updated_obj
                        if getattr(entry, "storage", None) and getattr(entry.storage, "unique_code", None) == item_id:
                            entry.storage = updated_obj
                    except Exception:
                        continue


    def get(self, reference_type: str, item_id: str = None, filter_dto=None) -> List[Any]:
        """
        Получение элементов справочника:
        - item_id: если указан, вернет конкретный элемент
        - filter_dto: если указан, применяет фильтр через prototype
        """
        key = self._map_type_to_repo_key(reference_type)
        data = list(self.__repo.data.get(key, []))
        if item_id:
            found = [x for x in data if getattr(x, "unique_code", None) == item_id]
            return found
        if filter_dto is None:
            return data
        return prototype.filter(data, filter_dto)

    def add(self, reference_type: str, dto) -> Any:
        """
        Добавление нового элемента справочника
        """
        key = self._map_type_to_repo_key(reference_type)
        validator.validate(dto, object)

        # Кэш существующих элементов для ссылки на них
        cache = {}
        for arr in self.__repo.data.values():
            for itm in arr:
                uid = getattr(itm, "unique_code", None)
                if uid:
                    cache[uid] = itm

        model_instance = None
        t = self._normalise_type(reference_type)
        if t.startswith("nomen"):
            validator.validate(dto, nomenclature_dto)
            model_instance = nomenclature_model.from_dto(dto, cache)
        elif t.startswith("range") or t in ("unit", "units"):
            validator.validate(dto, range_dto)
            model_instance = range_model.from_dto(dto, cache)
        elif t.startswith("group") or t in ("category",):
            validator.validate(dto, category_dto)
            model_instance = group_model.from_dto(dto, cache)
        elif t.startswith("storage") or t in ("warehouse",):
            validator.validate(dto, storage_dto)
            model_instance = storage_model.from_dto(dto, cache)
        else:
            raise argument_exception("Unsupported reference type")

        if key not in self.__repo.data:
            self.__repo.data[key] = []
        self.__repo.data[key].append(model_instance)

        # Логируем изменение
        payload = {
            "type": reference_type,
            "action": "add",
            "id": getattr(model_instance, "unique_code", None),
            "ts": datetime.utcnow().isoformat()
        }
        self._save_settings(payload)

        # Отправляем событие
        observe_service.create_event("reference_added", {"type": reference_type, "item": model_instance})
        return model_instance

    def update(self, reference_type: str, item_id: str, partial_payload: Dict[str, Any]) -> Any:
        """
        Частичное обновление элемента справочника
        """
        key = self._map_type_to_repo_key(reference_type)
        data = self.__repo.data.get(key, [])
        target = next((x for x in data if getattr(x, "unique_code", None) == item_id), None)
        if target is None:
            raise operation_exception(f"Item {item_id} not found in {reference_type}")

        # Обновляем поля объекта
        for k, v in (partial_payload or {}).items():
            try:
                if hasattr(target, k):
                    setattr(target, k, v)
                else:
                    setter_name = f"set_{k}"
                    if hasattr(target, setter_name) and callable(getattr(target, setter_name)):
                        getattr(target, setter_name)(v)
            except Exception:
                continue

        # Обновляем зависимости
        try:
            self._update_dependencies_on_change(reference_type, item_id, target)
        except Exception:
            pass

        # Пересчитываем данные через rest_service
        try:
            rest_service().calc()
        except Exception:
            pass

        # Логируем изменение
        payload = {
            "type": reference_type,
            "action": "update",
            "id": item_id,
            "payload": partial_payload,
            "ts": datetime.utcnow().isoformat()
        }
        self._save_settings(payload)

        observe_service.create_event("reference_updated",
                                     {"type": reference_type, "id": item_id, "payload": partial_payload})
        return target

    def delete(self, reference_type: str, item_id: str) -> bool:
        """
        Удаление элемента справочника
        Если элемент используется в других сущностях, выбрасывается ошибка
        """
        key = self._map_type_to_repo_key(reference_type)
        data = self.__repo.data.get(key, [])
        target = next((x for x in data if getattr(x, "unique_code", None) == item_id), None)
        if target is None:
            raise operation_exception(f"Item {item_id} not found in {reference_type}")

        # Проверка на зависимости
        deps = self._is_used_elsewhere(item_id, exclude_repo_key=key)
        if deps:
            examples = []
            for d in deps[:3]:
                rk = d.get("repo_key")
                attr = d.get("attr")
                cont = d.get("container")
                examples.append(f"repo={rk}, attr={attr}, container_id={getattr(cont, 'unique_code', repr(cont))}")
            raise operation_exception(
                f"Cannot delete {reference_type} {item_id}: used in other entities. Examples: {examples}")

        # Удаляем элемент
        self.__repo.data[key] = [x for x in data if getattr(x, "unique_code", None) != item_id]

        # Логируем удаление
        payload = {
            "type": reference_type,
            "action": "delete",
            "id": item_id,
            "ts": datetime.utcnow().isoformat()
        }
        self._save_settings(payload)

        observe_service.create_event("reference_deleted", {"type": reference_type, "id": item_id})
        return True

    def handle(self, event: str, params: Dict[str, Any]):
        """
        Обработка событий от observe_service
        Например, при изменении даты блокировки пересчитываем rest_service
        """
        if event == "lock_date_changed":
            try:
                rest_service().calc()
            except Exception:
                pass
