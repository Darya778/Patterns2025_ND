from Src.Core.abstract_logic import abstract_logic
from Src.Core.validator import operation_exception
from Src.reposity_manager import reposity_manager
from Src.Dtos.event_dto import event_dto
import json


class reference_handler(abstract_logic):
    """Обработчик событий справочников
    Реагирует на:
    - reference_delete_validation -> _validate_delete (может бросить operation_exception)
    - reference_updated -> _propagate_update
    - reference_added / deleted -> _write_settings (логирование в appsettings.json)
    """

    def __init__(self, repo: reposity_manager):
        self._repo = repo

    def handle(self, evt: event_dto):
        if not isinstance(evt, event_dto):
            return
        t = evt.event_type
        payload = evt.payload
        if t == "reference_delete_validation":
            self._validate_delete(payload)
        elif t == "reference_updated":
            self._propagate_update(payload)
        elif t in ("reference_added", "reference_deleted"):
            self._write_settings(payload, t)

    def _validate_delete(self, dto):
        ref_id = getattr(dto, "unique_code", None)
        for r in self._repo.data.get("receipts", []):
            for comp in getattr(r, "composition", []):
                if comp.get("nomenclature_id") == ref_id:
                    raise operation_exception(
                        f"Cannot delete item {ref_id}: used in receipt {getattr(r, 'unique_code', None)}"
                    )

    def _propagate_update(self, dto):
        ref_id = getattr(dto, "unique_code", None)
        for r in self._repo.data.get("receipts", []):
            for comp in getattr(r, "composition", []):
                if comp.get("nomenclature_id") == ref_id:
                    comp["nomenclature_name"] = getattr(dto, "name", None)

    def _write_settings(self, dto, event_type: str):
        try:
            with open("appsettings.json", "r", encoding="utf-8") as f:
                settings = json.load(f)
        except Exception:
            settings = {}
        settings.setdefault("audit", []).append({
            "event": event_type,
            "id": getattr(dto, "unique_code", None),
            "name": getattr(dto, "name", None)
        })
        with open("appsettings.json", "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)
        return True
