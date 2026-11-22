from __future__ import annotations

import json
import math
from typing import Any


def _reject_nonstandard_constant(value: str) -> None:
    raise ValueError(f"Constante JSON não permitida: {value}")


def _parse_finite_float(value: str) -> float:
    parsed = float(value)
    if not math.isfinite(parsed):
        raise ValueError("Valor numérico JSON fora do intervalo finito.")
    return parsed


def strict_json_loads(content: str) -> Any:
    """Decode JSON while rejecting non-standard and non-finite numeric values."""
    return json.loads(
        content,
        parse_constant=_reject_nonstandard_constant,
        parse_float=_parse_finite_float,
    )
