"""Synthetic counted effects for cross-process lifecycle acceptance."""

import argparse
import json
from pathlib import Path
import sys

from func_seq import ScriptError
from hidden_moves import Moves, MoveSet
from hidden_moves.adapters import CapabilityCatalog

from wispsy.reference import TextReport, normalize, report
from wispsy.sequence import build_script


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--receipts", required=True, type=Path)
    parser.add_argument("--text", default=" Hello WORLD ")
    parser.add_argument("--pace", default="auto")
    parser.add_argument("--version", default="counted-v1")
    parser.add_argument("--fail-report-once", action="store_true")
    parser.add_argument("--retry", action="store_true")
    parser.add_argument("--restart", action="store_true")
    arguments = parser.parse_args()

    def record(step: str) -> list[str]:
        previous = arguments.receipts.read_text(encoding="utf-8").splitlines() if arguments.receipts.exists() else []
        with arguments.receipts.open("a", encoding="utf-8") as stream:
            stream.write(step + "\n")
        return previous

    def counted_normalize(text: str) -> str:
        record("normalize")
        return normalize(text)

    def counted_report(text: str) -> TextReport:
        previous = record("report")
        if arguments.fail_report_once and "report" not in previous:
            raise RuntimeError("Synthetic failure after recording an effect")
        return report(text)

    group = MoveSet("text")
    group.learn(counted_normalize, name="normalize")
    group.learn(counted_report, name="report")
    moves = Moves()
    group.install(moves.registry)
    catalog = CapabilityCatalog(moves, ["text.normalize", "text.report"])
    try:
        script = build_script(arguments.text, catalog=catalog, version=arguments.version)
        result = script.run(checkpoint=arguments.checkpoint, pace=arguments.pace,
                            retry=arguments.retry, restart=arguments.restart)
    except ScriptError as error:
        print(json.dumps({"error": type(error).__name__}), file=sys.stderr)
        raise SystemExit(2) from error
    print(json.dumps({"status": result.status, "completed": result.completed,
                      "results": result.results, "run_id": result.run_id}))


if __name__ == "__main__":
    main()
