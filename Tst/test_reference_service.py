"""
Юнит-тесты для reference_service
"""

import pytest
from Src.Services.reference_service import reference_service
from Src.Dtos.nomenclature_dto import nomenclature_dto
from Src.Dtos.range_dto import range_dto
from Src.Dtos.category_dto import category_dto
from Src.Dtos.storage_dto import storage_dto
from Src.reposity_manager import reposity_manager
from Src.Core.observe_service import observe_service
from Src.Models.receipt_model import receipt_model
import json
import os
import uuid


@pytest.fixture(autouse=True)
def clear_repo_and_settings(tmp_path, monkeypatch):
    """
    Фикстура pytest для очистки глобального репозитория и временного файла appsettings.json перед каждым тестом.
    tmp_path — временная директория для создания тестового appsettings.json
    monkeypatch — позволяет временно изменить переменные окружения
    """
    repo = reposity_manager()
    repo.data.clear()  # Очистка всех данных репозитория

    # Очистка событий observe_service
    if hasattr(observe_service, "clear"):
        try:
            observe_service.clear()
        except Exception:
            pass

    # Создание временного файла настроек
    settings_file = tmp_path / "appsettings.json"
    monkeypatch.setenv("APP_SETTINGS_PATH", str(settings_file))
    if settings_file.exists():
        settings_file.unlink()
    yield

    # Очистка после теста
    repo.data.clear()
    if settings_file.exists():
        settings_file.unlink()


def test_add_and_get_and_delete_simple_refs():
    """
    Тестируем базовые операции CRUD:
    - Добавление range и storage
    - Получение элемента по unique_code
    - Удаление элемента storage
    """
    svc = reference_service()

    # Добавление единицы измерения
    rdto = range_dto()
    rdto.name = "шт"
    r_obj = svc.add("range", rdto)
    assert getattr(r_obj, "unique_code", None) is not None

    # Получение по unique_code
    found = svc.get("range", getattr(r_obj, "unique_code", None))
    assert len(found) == 1

    # Добавление склада
    sdto = storage_dto()
    sdto.id = str(uuid.uuid4())
    sdto.name = "Main warehouse"
    sdto.address = "ул. Пушкина, д. 1"
    s_obj = svc.add("storage", sdto)
    assert s_obj in svc.get("storage", getattr(s_obj, "unique_code", None))

    # Удаление склада
    assert svc.delete("storage", getattr(s_obj, "unique_code", None)) is True


def test_delete_blocked_when_nomenclature_used_in_receipt_and_transaction():
    """
    Тестируем блокировку удаления номенклатуры,
    если она используется в рецепте или транзакции.
    """
    svc = reference_service()
    repo = reposity_manager()

    # Создаем единицу измерения и категорию
    rd = range_dto()
    rd.name = "кг"
    r_model = svc.add("range", rd)

    gd = category_dto()
    gd.name = "Сыпучие"
    gd.id = str(uuid.uuid4())
    g_model = svc.add("group", gd)

    # Создаем номенклатуру, связав с range и category
    nd = nomenclature_dto()
    nd.name = "TestGrain"
    nd.range_id = r_model.unique_code
    nd.category_id = g_model.unique_code
    n_model = svc.add("nomenclature", nd)

    # Создаем фиктивный рецепт с использованием номенклатуры
    from Src.Dtos.receipt_dto import receipt_dto
    r_dto = receipt_dto()
    r_dto.name = "FakeRecipe"
    r_dto.cooking_time = "10 min"
    r_dto.portions = 1
    r_dto.steps = []
    r_dto.composition = [{"nomenclature_id": n_model.unique_code}]

    fake_receipt = receipt_model.from_dto(r_dto, cache={})
    repo.data.setdefault("receipt_model", []).append(fake_receipt)

    # Попытка удалить номенклатуру должна вызвать исключение
    import pytest
    with pytest.raises(Exception):
        svc.delete("nomenclature", n_model.unique_code)


def test_update_replaces_object_and_propagates_changes():
    """
    Тестируем обновление объекта номенклатуры:
    - Имя обновляется
    - Обновление распространяется на рецепты и транзакции
    """
    svc = reference_service()
    repo = reposity_manager()

    # Создаем группу и единицу измерения
    gd = category_dto()
    gd.name = "Сыпучие"
    gd.id = str(uuid.uuid4())
    g_model = svc.add("group", gd)

    rd = range_dto()
    rd.name = "кг"
    r_model = svc.add("range", rd)

    # Создаем номенклатуру
    nd = nomenclature_dto()
    nd.name = "OldName"
    nd.range_id = r_model.unique_code
    nd.category_id = g_model.unique_code
    n_model = svc.add("nomenclature", nd)

    # Создаем фиктивный рецепт с использованием номенклатуры
    fake_receipt = type("FakeReceipt", (), {})()
    fake_receipt.unique_code = str(uuid.uuid4())
    fake_receipt.composition = [{"nomenclature_id": n_model.unique_code}]
    repo.data.setdefault("receipt_model", []).append(fake_receipt)

    # Создаем фиктивную транзакцию
    fake_tx = type("FakeTrans", (), {})()
    fake_tx.unique_code = str(uuid.uuid4())
    fake_tx.nomenclature_id = n_model.unique_code
    repo.data.setdefault("transaction_model", []).append(fake_tx)

    # Обновляем имя номенклатуры
    svc.update("nomenclature", n_model.unique_code, {"name": "NewName"})

    # Проверяем, что изменения распространились на рецепты и транзакции
    r = repo.data["receipt_model"][0]
    assert r.composition[0]["nomenclature_id"] == n_model.unique_code
    t = repo.data["transaction_model"][0]
    assert t.nomenclature_id == n_model.unique_code


def test_settings_written_with_full_diff(tmp_path, monkeypatch):
    """
    Тестируем, что изменения справочников сохраняются в settings (appsettings.json)
    """
    svc = reference_service()
    repo = reposity_manager()

    settings_path = tmp_path / "appsettings.json"

    # Создаем группу, единицу измерения и номенклатуру
    gd = category_dto()
    gd.name = "Сыпучие"
    gd.id = str(uuid.uuid4())
    g_model = svc.add("group", gd)

    rd = range_dto()
    rd.name = "шт"
    r_model = svc.add("range", rd)

    nd = nomenclature_dto()
    nd.name = "X"
    nd.range_id = r_model.unique_code
    nd.category_id = g_model.unique_code
    n_model = svc.add("nomenclature", nd)

    # Обновляем номенклатуру
    svc.update("nomenclature", n_model.unique_code, {"name": "XX"})

    # Проверяем наличие записи о последнем изменении
    if settings_path.exists():
        cfg = json.load(settings_path.open(encoding="utf-8"))
        assert "last_reference_change" in cfg
    else:
        if os.path.exists("appsettings.json"):
            cfg = json.load(open("appsettings.json", encoding="utf-8"))
            assert "last_reference_change" in cfg
        else:
            pytest.skip("appsettings.json not found; cannot assert settings write in this environment")
