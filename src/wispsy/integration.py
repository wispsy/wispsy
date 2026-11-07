"""Opt-in Hidden Moves assembly for the ordinary reference functions."""

from hidden_moves import Moves, MoveSet, MoveSpec
from hidden_moves.adapters import CapabilityCatalog

from .reference import TextReport, normalize, report

SELECTED_NAMES = ("text.normalize", "text.report")


def provide_moves() -> tuple[MoveSpec, ...]:
    """Advertise definitions only; no resources, content or functions are opened."""
    text = MoveSet("text")
    text.learn(normalize)
    text.learn(report)
    return text.moves()


def build_catalog() -> CapabilityCatalog:
    moves = Moves()
    moves.registry.register_many(provide_moves())
    return CapabilityCatalog(moves, SELECTED_NAMES)


def run_catalog(text: str) -> TextReport:
    catalog = build_catalog()
    value = catalog.serialize_result("text.normalize", catalog.invoke("text.normalize", {"text": text}))
    result = catalog.invoke("text.report", {"text": value})
    return catalog.serialize_result("text.report", result)
