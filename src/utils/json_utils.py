from __future__ import annotations

import json
from typing import Any


def _reject_nonstandard_constant(value: str) -> None:
    raise ValueError(f"Constante JSON não permitida: {value}")


def strict_json_loads(content: str) -> Any:
    """Decode JSON while rejecting JavaScript-style NaN and Infinity constants."""
    return json.loads(content, parse_constant=_reject_nonstandard_constant)
