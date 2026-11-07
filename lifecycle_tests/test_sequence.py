"""Counted effects prove process restart and explicit uncertain-step recovery."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from hidden_moves import Moves, MoveSet
from hidden_moves.adapters import CapabilityCatalog

from wispsy.reference import report, run_reference
from wispsy.sequence import build_script

WORKER = Path(__file__).with_name("worker.py")


class SequenceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.outside = Path(self.temporary.name)
        self.checkpoint = self.outside / "progress.json"
        self.receipts = self.outside / "receipts.txt"

    def worker(self, *options):
        return subprocess.run([sys.executable, "-I", str(WORKER),
                               "--checkpoint", str(self.checkpoint), "--receipts", str(self.receipts),
                               *options], cwd=self.outside, capture_output=True, text=True, timeout=15)

    def success(self, result):
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_selected_default_workflow_uses_the_same_json_results(self):
        script = build_script("  Straße 🍑 ")
        first = script.run(pace="function")
        self.assertEqual(first.status, "paused")
        self.assertEqual(first.completed, ("normalize",))
        completed = script.run()
        self.assertEqual(completed.status, "completed")
        self.assertEqual(completed.results["report"], run_reference("  Straße 🍑 "))

    def test_fresh_process_resume_and_completed_runs_do_not_replay(self):
        first = self.success(self.worker("--pace", "function"))
        self.assertEqual((first["status"], first["completed"]), ("paused", ["normalize"]))
        self.assertEqual(self.receipts.read_text(), "normalize\n")
        second = self.success(self.worker())
        self.assertEqual(second["status"], "completed")
        self.assertEqual(second["run_id"], first["run_id"])
        self.assertEqual(second["results"]["report"], run_reference(" Hello WORLD "))
        self.assertEqual(self.receipts.read_text(), "normalize\nreport\n")
        third = self.success(self.worker())
        self.assertEqual(third, second)
        self.assertEqual(self.receipts.read_text(), "normalize\nreport\n")

    def test_uncertain_failure_requires_explicit_retry_and_restart_repeats_effects(self):
        failed = self.worker("--fail-report-once")
        self.assertEqual(failed.returncode, 2)
        self.assertEqual(json.loads(failed.stderr)["error"], "StepFailedError")
        self.assertEqual(self.receipts.read_text(), "normalize\nreport\n")
        blocked = self.worker("--fail-report-once")
        self.assertEqual(blocked.returncode, 2)
        self.assertEqual(json.loads(blocked.stderr)["error"], "RecoveryRequiredError")
        self.assertEqual(self.receipts.read_text(), "normalize\nreport\n")
        retried = self.success(self.worker("--fail-report-once", "--retry"))
        self.assertEqual(retried["status"], "completed")
        self.assertEqual(self.receipts.read_text(), "normalize\nreport\nreport\n")
        restarted = self.success(self.worker("--fail-report-once", "--restart"))
        self.assertNotEqual(restarted["run_id"], retried["run_id"])
        self.assertEqual(self.receipts.read_text(), "normalize\nreport\nreport\nnormalize\nreport\n")

    def test_changed_definition_or_initial_arguments_reject_resume_before_effects(self):
        self.success(self.worker("--pace", "function"))
        for options in (("--version", "counted-v2"), ("--text", "different input")):
            with self.subTest(options=options):
                result = self.worker(*options)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(json.loads(result.stderr)["error"], "DefinitionMismatchError")
                self.assertEqual(self.receipts.read_text(), "normalize\n")

    def test_public_module_cli_pauses_and_resumes_in_another_process(self):
        text = " Straße 🍑 "
        command = [sys.executable, "-I", "-m", "wispsy.sequence", text,
                   "--checkpoint", str(self.checkpoint)]
        first = subprocess.run([*command, "--pace", "function"], cwd=self.outside,
                               capture_output=True, timeout=15)
        self.assertEqual(self.success(first)["status"], "paused")
        second = subprocess.run(command, cwd=self.outside, capture_output=True, timeout=15)
        self.assertEqual(self.success(second)["results"]["report"], run_reference(text))

    def test_async_catalog_is_rejected_before_creating_an_unawaited_result(self):
        async def normalize(text: str) -> str:
            raise AssertionError("Construction invoked an async function")

        group = MoveSet("text")
        group.learn(normalize)
        group.learn(report)
        moves = Moves()
        group.install(moves.registry)
        catalog = CapabilityCatalog(moves, ["text.normalize", "text.report"])
        with self.assertRaisesRegex(ValueError, "synchronous"):
            build_script("hello", catalog=catalog)
