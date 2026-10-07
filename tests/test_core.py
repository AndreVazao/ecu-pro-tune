import json
from pathlib import Path

from src.tuning.validators import clamp, validate_numeric_map, validate_map_name

def test_clamp():
    assert clamp(150, -100, 100) == 100
    assert clamp(-150, -100, 100) == -100

def test_validate_numeric_map():
    assert validate_numeric_map([0, 1, 2], -10, 10)[0]
    assert not validate_numeric_map([], -10, 10)[0]
    assert not validate_numeric_map([99], -10, 10)[0]

def test_validate_map_name():
    assert validate_map_name("Stage 1")[0]
    assert not validate_map_name("")[0]

def test_stage1_profile_shape():
    path = Path(__file__).resolve().parents[1] / "configs" / "stage1.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["Profile_Name"] == "Stage 1"
    assert data["map"] == "stage1_map.json"
