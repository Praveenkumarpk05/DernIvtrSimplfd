"""Helpers that simplify and optionally invert structured data."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def simplify(value: Any) -> Any:
    """Normalize common input values by stripping strings and removing empties.

    Zero and False are preserved, but None and blank strings are dropped.
    """
    if value is None:
        return None

    if isinstance(value, str):
        cleaned = value.strip()
        return cleaned if cleaned else None

    if isinstance(value, Mapping):
        result: dict[Any, Any] = {}
        for key, item in value.items():
            simplified_item = simplify(item)
            if simplified_item is None:
                continue
            result[key] = simplified_item
        return result

    if isinstance(value, (list, tuple)):
        cleaned_items = [simplify(item) for item in value]
        return [item for item in cleaned_items if item is not None]

    if isinstance(value, set):
        cleaned_items = [simplify(item) for item in value]
        return {item for item in cleaned_items if item is not None}

    return value


def invert(value: Any) -> Any:
    """Invert a mapping by swapping keys and values, or reverse a sequence."""
    if isinstance(value, Mapping):
        return {str(v): k for k, v in value.items()}

    if isinstance(value, (list, tuple)):
        return list(reversed(value))

    if isinstance(value, set):
        return tuple(sorted(value, reverse=True))

    return value


def improve_function(value: Any, *, concept: str = "new", invert_data: bool = False, simplify_data: bool = True) -> Any:
    """Apply the improved concept: simplify input, then optionally invert it.

    The accepted concept value is informational; the function always performs the
    same generalized transformation.
    """
    if concept not in {"new", "simplify", "invert", "improve"}:
        raise ValueError(f"Unsupported concept: {concept!r}")

    processed = value
    if simplify_data:
        processed = simplify(processed)
    if invert_data:
        processed = invert(processed)
    return processed


new_concept = improve_function

__all__ = ["simplify", "invert", "improve_function", "new_concept"]
