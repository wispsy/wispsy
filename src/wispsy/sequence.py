"""Optional Python 3.14+ lifecycle reference using the public func_seq API."""

import sys

if sys.version_info < (3, 14):
    raise ImportError("The Wispsy sequence reference requires Python 3.14 or newer.")

import argparse
import json

from func_seq import Script, ScriptError
from hidden_moves.adapters import CapabilityCatalog

from .integration import SELECTED_NAMES, build_catalog

DEFINITION_VERSION = "text-reference-v1"


def build_script(text: str, *, catalog: CapabilityCatalog | None = None,
                 version: str = DEFINITION_VERSION) -> Script:
    """Map two selected synchronous calls into existing lifecycle boundaries.

    Bump version when callable behavior, captured catalog state or relevant
    environment changes. The executor cannot infer those changes from closures.
    """
    selected = build_catalog() if catalog is None else catalog
    for name in SELECTED_NAMES:
        if selected.describe(name).is_async:
            raise ValueError("This reference requires synchronous text capabilities.")

    def normalize_step(text: str) -> str:
        result = selected.invoke("text.normalize", {"text": text})
        return selected.serialize_result("text.normalize", result)

    def report_step(text: str) -> dict:
        result = selected.invoke("text.report", {"text": text})
        return selected.serialize_result("text.report", result)

    script = Script("wispsy-text-reference", version=version)
    normalized = script.add_function(normalize_step, text=text, step_id="normalize")
    script.add_function(report_step, text=normalized, step_id="report")
    return script


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text")
    parser.add_argument("--checkpoint", required=True, help="Explicit progress file in an existing parent directory.")
    parser.add_argument("--pace", choices=("auto", "function", "pause"), default="auto")
    parser.add_argument("--definition-version", default=DEFINITION_VERSION)
    recovery = parser.add_mutually_exclusive_group()
    recovery.add_argument("--retry", action="store_true", help="Explicitly repeat the uncertain step.")
    recovery.add_argument("--restart", action="store_true", help="Explicitly repeat the entire workflow.")
    arguments = parser.parse_args()
    try:
        script = build_script(arguments.text, version=arguments.definition_version)
        result = script.run(checkpoint=arguments.checkpoint, pace=arguments.pace,
                            retry=arguments.retry, restart=arguments.restart)
    except ScriptError as error:
        print(json.dumps({"error": type(error).__name__, "message": str(error)}), file=sys.stderr)
        raise SystemExit(2) from error
    print(json.dumps({"status": result.status, "completed": result.completed,
                      "results": result.results, "run_id": result.run_id},
                     ensure_ascii=False, allow_nan=False))


if __name__ == "__main__":
    main()
