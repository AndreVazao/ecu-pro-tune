from __future__ import annotations

from typing import Iterable

def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))

def validate_numeric_map(values: Iterable[float], minimum: float, maximum: float) -> tuple[bool, str]:
    data = list(values)
    if not data:
        return False, "Mapa vazio."
    for value in data:
        if not isinstance(value, (int, float)):
            return False, "Todos os valores devem ser numéricos."
        if value < minimum or value > maximum:
            return False, f"Valor fora do intervalo permitido: {minimum}..{maximum}."
    return True, "OK"

def validate_map_name(name: str) -> tuple[bool, str]:
    cleaned = name.strip()
    if not cleaned:
        return False, "Nome obrigatório."
    if len(cleaned) > 80:
        return False, "Nome demasiado longo."
    return True, "OK"
