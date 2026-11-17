from __future__ import annotations

import math
import re
from typing import Iterable


def clamp(value: float, minimum: float, maximum: float) -> float:
    if minimum > maximum:
        raise ValueError("O limite mínimo não pode exceder o máximo.")
    return max(minimum, min(maximum, value))


def validate_numeric_map(
    values: Iterable[float], minimum: float, maximum: float
) -> tuple[bool, str]:
    if not math.isfinite(minimum) or not math.isfinite(maximum) or minimum > maximum:
        return False, "Intervalo de validação inválido."

    data = list(values)
    if not data:
        return False, "Mapa vazio."

    for value in data:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return False, "Todos os valores devem ser numéricos."
        if not math.isfinite(value):
            return False, "Todos os valores devem ser finitos."
        if value < minimum or value > maximum:
            return False, f"Valor fora do intervalo permitido: {minimum}..{maximum}."

    return True, "OK"


def validate_map_name(name: str) -> tuple[bool, str]:
    if not isinstance(name, str):
        return False, "Nome inválido."

    cleaned = name.strip()
    if not cleaned:
        return False, "Nome obrigatório."
    if len(cleaned) > 80:
        return False, "Nome demasiado longo."
    if cleaned in {".", ".."} or re.search(r'[<>:"/\\\\|?*\\x00-\\x1f]', cleaned):
        return False, "O nome contém caracteres não permitidos."
    if cleaned.endswith((" ", ".")):
        return False, "O nome não pode terminar com espaço ou ponto."

    return True, "OK"
