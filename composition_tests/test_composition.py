import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scriptty import loads
from wispsy.composition import text_workflow_document
from wispsy.integration import build_catalog
from wispsy.reference import run_reference


class CrossPackageTests(unittest.TestCase):
    def test_real_reference_catalog_pipeline_document_and_installed_cli_match(self):
        text = " Straße   🌍 "
        expected = run_reference(text)
        document = text_workflow_document()
        workflow = loads(json.dumps(document))
        bound = workflow.bind(build_catalog(), catalog_version="wispsy-text-v1")
        self.assertEqual(bound.run({"text": text}).outputs, {"report": expected})
        with tempfile.TemporaryDirectory() as directory:
            outside = Path(directory)
            path, inputs = outside / "workflow.json", outside / "inputs.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            inputs.write_text(json.dumps({"schema": 1, "inputs": {"text": text}}), encoding="utf-8")
            selection = ["--provider", "wispsy-reference", "--select", "text.normalize", "--select", "text.report", "--catalog-version", "wispsy-text-v1"]
            def command(action, *options):
                result = subprocess.run([sys.executable, "-I", "-m", "scriptty", action, str(path), "--inputs", str(inputs), *selection, *options], cwd=outside, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8", errors="replace"))
                return json.loads(result.stdout)
            self.assertEqual(command("run")["outputs"], {"report": expected})
            if importlib.util.find_spec("func_seq"):
                checkpoint = str(outside / "progress.json")
                first = command("run", "--checkpoint", checkpoint, "--pace", "function")
                self.assertEqual((first["status"], first["completed"]), ("paused", ["normalize"]))
                resumed = command("resume", "--checkpoint", checkpoint)
                self.assertEqual((resumed["status"], resumed["outputs"], resumed["run_id"]), ("completed", {"report": expected}, first["run_id"]))


class TerminalReferenceTests(unittest.IsolatedAsyncioTestCase):
    @unittest.skipUnless(importlib.util.find_spec("carets"), "optional terminal profile")
    async def test_selected_terminal_uses_the_same_application_workflow(self):
        from carets import KeyMsg
        from carets.testing import TestProgram
        from scriptty.terminal import WorkflowTerminal

        with tempfile.TemporaryDirectory() as directory:
            text = " Hello   WORLD "
            model = WorkflowTerminal(loads(json.dumps(text_workflow_document())), build_catalog(),
                catalog_version="wispsy-text-v1", checkpoint=str(Path(directory) / "terminal.json"), inputs={"text": text})
            test = TestProgram(model)
            model.attach(test.program)
            async with test:
                await test.send(KeyMsg("tab"), KeyMsg(" "), KeyMsg("down"), KeyMsg(" "), KeyMsg("tab"), KeyMsg("enter"))
                await test.wait_for(lambda: model.status == "completed")
                self.assertEqual(model.outcome["outputs"], {"report": run_reference(text)})
                await test.resize(60, 12)
                test.assert_fits(60, 12)
