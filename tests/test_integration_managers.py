import json
from pathlib import Path

import pytest

import src.core.ecu_manager as ecu_module
import src.core.rollback_manager as rollback_module
from src.core.ecu_manager import ECUManager
from src.core.profile_manager import ProfileManager
from src.core.rollback_manager import RollbackManager
from src.tuning.validators import validate_map_name, validate_numeric_map


def test_profile_manager_round_trip_and_safe_names(tmp_path: Path) -> None:
    manager = ProfileManager(base_dir=tmp_path / "profiles")
    saved = manager.save_profile("Daily setup", {"rpm_limit": 6500, "enabled": True})

    assert saved == tmp_path / "profiles" / "Daily setup.json"
    assert manager.load_saved_profile("Daily setup") == {
        "rpm_limit": 6500,
        "enabled": True,
    }
    assert manager.list_saved_profiles() == ["Daily setup"]
    assert manager.load_saved_profile("missing") is None

    with pytest.raises(ValueError):
        manager.save_profile("../outside", {"rpm_limit": 6500})
    with pytest.raises(ValueError):
        manager.load_saved_profile(r"..\outside")
    with pytest.raises(TypeError):
        manager.save_profile("invalid", ["not", "an", "object"])  # type: ignore[arg-type]


def test_profile_manager_rejects_non_finite_json(tmp_path: Path) -> None:
    manager = ProfileManager(base_dir=tmp_path / "profiles")

    with pytest.raises(ValueError):
        manager.save_profile("invalid", {"boost": float("nan")})

    assert not (tmp_path / "profiles" / "invalid.json").exists()


def test_ecu_manager_load_apply_and_extract_map_arrays(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    configs = tmp_path / "configs"
    maps = tmp_path / "maps"
    configs.mkdir()
    maps.mkdir()
    (maps / "stage1_map.json").write_text(
        json.dumps({"values": [1, 2, 3], "ignored": ["x", 2]}),
        encoding="utf-8",
    )
    (configs / "stage1.json").write_text(
        json.dumps({"Profile_Name": "Stage 1", "map": "stage1_map.json"}),
        encoding="utf-8",
    )
    monkeypatch.setattr(ecu_module, "CONFIGS_DIR", configs)
    monkeypatch.setattr(ecu_module, "MAPS_DIR", maps)

    manager = ECUManager()

    assert manager.load_profile("stage1.json")["Profile_Name"] == "Stage 1"
    assert manager.apply_profile("stage1.json") == (True, [])
    assert manager.list_numeric_arrays("stage1.json") == {
        "stage1_map.json:values": [1, 2, 3]
    }
    assert manager.validate_profile_maps({"map": "missing.json"})
    assert manager.validate_profile_maps({"map": "../outside.json"})

    with pytest.raises(ValueError):
        manager.load_profile("../stage1.json")
    with pytest.raises(ValueError):
        manager.load_profile(r"..\stage1.json")


def test_rollback_manager_backup_restore_and_path_validation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    configs = tmp_path / "configs"
    backups = tmp_path / "backups"
    configs.mkdir()
    backups.mkdir()
    profile = configs / "daily_profile.json"
    original = '{"rpm_limit": 6200}'
    profile.write_text(original, encoding="utf-8")
    monkeypatch.setattr(rollback_module, "CONFIGS_DIR", configs)
    monkeypatch.setattr(rollback_module, "BACKUPS_DIR", backups)

    manager = RollbackManager()
    backup = manager.backup_profile(profile.name)

    assert backup is not None
    assert backup.read_text(encoding="utf-8") == original
    assert manager.list_backups() == [backup.name]

    profile.write_text('{"rpm_limit": 7000}', encoding="utf-8")
    restored = manager.restore_backup(backup.name)

    assert restored == profile
    assert restored.read_text(encoding="utf-8") == original
    assert manager.backup_profile("missing.json") is None

    with pytest.raises(ValueError):
        manager.backup_profile("../outside.json")
    with pytest.raises(ValueError):
        manager.restore_backup("../outside.json")
    with pytest.raises(ValueError):
        manager.restore_backup("daily_profile.json.bak.json")


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf"), True])
def test_numeric_map_rejects_non_finite_and_boolean_values(value: float) -> None:
    valid, message = validate_numeric_map([value], -100, 100)

    assert not valid
    assert message != "OK"


def test_numeric_map_rejects_invalid_bounds() -> None:
    assert validate_numeric_map([1], 10, -10)[0] is False
    assert validate_numeric_map([1], float("-inf"), 10)[0] is False


@pytest.mark.parametrize("name", ["", "  ", "../map", r"..\map", "bad/name", "bad:name"])
def test_map_name_rejects_unsafe_names(name: str) -> None:
    assert validate_map_name(name)[0] is False


def test_map_name_accepts_normal_names() -> None:
    assert validate_map_name("Stage 1 - Daily_2026")[0] is True



def test_rollback_backup_same_second_does_not_overwrite(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    configs = tmp_path / "configs"
    backups = tmp_path / "backups"
    configs.mkdir()
    backups.mkdir()
    profile = configs / "daily_profile.json"
    monkeypatch.setattr(rollback_module, "CONFIGS_DIR", configs)
    monkeypatch.setattr(rollback_module, "BACKUPS_DIR", backups)
    profile.write_text('{"rpm_limit": 6200}', encoding="utf-8")

    class FixedDateTime:
        @staticmethod
        def now() -> object:
            from datetime import datetime

            return datetime(2026, 11, 21, 12, 30, 45)

    monkeypatch.setattr(rollback_module, "datetime", FixedDateTime)
    manager = RollbackManager()

    first = manager.backup_profile(profile.name)
    assert first is not None
    profile.write_text('{"rpm_limit": 6800}', encoding="utf-8")
    second = manager.backup_profile(profile.name)

    assert second is not None
    assert first != second
    assert first.read_text(encoding="utf-8") == '{"rpm_limit": 6200}'
    assert second.read_text(encoding="utf-8") == '{"rpm_limit": 6800}'
    assert set(manager.list_backups()) == {first.name, second.name}
    assert manager.restore_backup(second.name) == profile
    assert json.loads(profile.read_text(encoding="utf-8")) == {"rpm_limit": 6800}


@pytest.mark.parametrize(
    "corrupt_content",
    [
        "{broken json",
        "[]",
        '"scalar"',
        "null",
        '{"boost":NaN}',
        '{"rpm_limit":1e999}',
        '{"rpm_limit":-1e999}',
    ],
)
def test_rollback_restore_rejects_corrupt_or_non_object_backup_without_overwrite(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    corrupt_content: str,
) -> None:
    configs = tmp_path / "configs"
    backups = tmp_path / "backups"
    configs.mkdir()
    backups.mkdir()
    profile = configs / "daily_profile.json"
    profile.write_text('{"rpm_limit": 7100}', encoding="utf-8")
    backup = backups / "daily_profile.json_20261121_123000.bak.json"
    backup.write_text(corrupt_content, encoding="utf-8")
    monkeypatch.setattr(rollback_module, "CONFIGS_DIR", configs)
    monkeypatch.setattr(rollback_module, "BACKUPS_DIR", backups)

    manager = RollbackManager()

    with pytest.raises(ValueError):
        manager.restore_backup(backup.name)

    assert profile.read_text(encoding="utf-8") == '{"rpm_limit": 7100}'
    assert not (configs / "daily_profile.json.restore.tmp").exists()

@pytest.mark.parametrize("bad_json", ['{"value":NaN}', '{"value":Infinity}', '{"value":-Infinity}'])
def test_profile_manager_load_rejects_nonstandard_json_constants(
    tmp_path: Path, bad_json: str
) -> None:
    manager = ProfileManager(base_dir=tmp_path / "profiles")
    (tmp_path / "profiles" / "invalid.json").write_text(bad_json, encoding="utf-8")

    with pytest.raises(ValueError):
        manager.load_saved_profile("invalid")


@pytest.mark.parametrize("bad_json", ['{"rpm":NaN}', '{"boost":Infinity}', '{"x":-Infinity}'])
def test_ecu_manager_profile_load_rejects_nonstandard_json_constants(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, bad_json: str
) -> None:
    configs = tmp_path / "configs"
    maps = tmp_path / "maps"
    configs.mkdir()
    maps.mkdir()
    (configs / "invalid.json").write_text(bad_json, encoding="utf-8")
    monkeypatch.setattr(ecu_module, "CONFIGS_DIR", configs)
    monkeypatch.setattr(ecu_module, "MAPS_DIR", maps)

    with pytest.raises(ValueError):
        ECUManager().load_profile("invalid.json")


def test_ecu_manager_map_load_rejects_nonstandard_constants_and_filters_nonfinite_arrays(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    configs = tmp_path / "configs"
    maps = tmp_path / "maps"
    configs.mkdir()
    maps.mkdir()
    (configs / "stage.json").write_text(
        '{"Profile_Name":"Stage","map":"stage_map.json"}', encoding="utf-8"
    )
    (maps / "stage_map.json").write_text(
        '{"safe":[1,2,3],"nan_values":[1,NaN,3],"infinite":[Infinity,2]}',
        encoding="utf-8",
    )
    monkeypatch.setattr(ecu_module, "CONFIGS_DIR", configs)
    monkeypatch.setattr(ecu_module, "MAPS_DIR", maps)

    result = ECUManager().list_numeric_arrays("stage.json")
    assert result == {}


def test_ecu_manager_direct_numeric_arrays_filter_nonfinite_values(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    configs = tmp_path / "configs"
    maps = tmp_path / "maps"
    configs.mkdir()
    maps.mkdir()
    (configs / "direct.json").write_text(
        '{"Profile_Name":"Direct","values":[1,NaN,3]}', encoding="utf-8"
    )
    monkeypatch.setattr(ecu_module, "CONFIGS_DIR", configs)
    monkeypatch.setattr(ecu_module, "MAPS_DIR", maps)

    with pytest.raises(ValueError):
        ECUManager().load_profile("direct.json")

@pytest.mark.parametrize("bad_json", ['{"value":1e999}', '{"value":NaN}'])
def test_profile_manager_rejects_overflow_and_nonfinite_json_values(
    tmp_path: Path, bad_json: str
) -> None:
    manager = ProfileManager(base_dir=tmp_path / "profiles")
    (tmp_path / "profiles" / "invalid.json").write_text(bad_json, encoding="utf-8")

    with pytest.raises(ValueError):
        manager.load_saved_profile("invalid")


@pytest.mark.parametrize("bad_json", ['{"config":NaN}', '{"config":1e999}'])
def test_profile_manager_config_load_rejects_nonfinite_json_values(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, bad_json: str
) -> None:
    import src.core.profile_manager as profile_module

    configs = tmp_path / "configs"
    configs.mkdir()
    (configs / "invalid.json").write_text(bad_json, encoding="utf-8")
    monkeypatch.setattr(profile_module, "CONFIGS_DIR", configs)

    with pytest.raises(ValueError):
        ProfileManager(base_dir=tmp_path / "profiles").load_config_profile("invalid.json")

@pytest.mark.parametrize("bad_json", ['{"value":1e999}'])
def test_profile_manager_rejects_numeric_overflow_json(
    tmp_path: Path, bad_json: str
) -> None:
    manager = ProfileManager(base_dir=tmp_path / "profiles")
    (tmp_path / "profiles" / "invalid.json").write_text(bad_json, encoding="utf-8")

    with pytest.raises(ValueError):
        manager.load_saved_profile("invalid")
