"""Opt-in Python 3.14+ normalization, typed table source and presentation reference."""

import sys

if sys.version_info < (3, 14):
    raise ImportError("The Wispsy table reference requires Python 3.14 or newer")

from headless_spreadsheets import SourceColumn, Table, TableSource
from moveset import Input, Pipeline, Ref, Step

from .integration import build_catalog

COLUMNS = (
    SourceColumn("text", "Text", "text", nullable=False, searchable=True),
    SourceColumn("words", "Words", "integer", nullable=False),
    SourceColumn("characters", "Characters", "integer", nullable=False),
)
CATALOG_VERSION = "wispsy-text-v1"


def normalization_pipeline(count: int) -> Pipeline:
    if type(count) is not int or not 1 <= count <= 64:
        raise ValueError("Select 1–64 text rows")
    steps = []
    for index in range(count):
        steps.append(Step(f"normalize-{index}", "text.normalize", {"text": Input("texts")[index]}))
        steps.append(Step(f"report-{index}", "text.report", {"text": Ref(f"normalize-{index}")}))
    return Pipeline("text-table", version="1", steps=tuple(steps),
                    outputs={"rows": [Ref(f"report-{index}") for index in range(count)]})


def normalize_table(texts: list[str]) -> Table:
    """Run explicit mappings, then preserve string/integer report cells in a Table."""
    if type(texts) is not list:
        raise ValueError("Texts must be a list")
    bound = normalization_pipeline(len(texts)).bind(build_catalog(), catalog_version=CATALOG_VERSION)
    result = bound.run({"texts": texts})
    return Table.from_records(result.outputs["rows"], columns=("text", "words", "characters"))


def table_source(table: Table) -> TableSource:
    """Use the existing caller-owned, read-only tabular/1 source contract."""
    return TableSource(table, columns=COLUMNS)


def markdown_report(texts: list[str]) -> str:
    """Select the existing detached display-document consumer explicitly."""
    return normalize_table(texts).to_document().to_markdown()
