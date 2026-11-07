"""Selected calls and actual process pipes match the ordinary Python workflow."""

import json
import subprocess
import sys
import unittest

from hidden_moves import UnknownMoveError

from wispsy.integration import build_catalog, run_catalog
from wispsy.reference import run_reference


class WorkflowTests(unittest.TestCase):
    command = [sys.executable, "-I", "-m", "hidden_moves", "--plugin", "wispsy-reference", "moves", "call"]

    def test_selected_catalog_matches_python_and_rejects_other_names(self):
        for text in ("  Hello\tWORLD ", "", "  Straße\u2003🍑  "):
            with self.subTest(text=text):
                self.assertEqual(run_catalog(text), run_reference(text))
        catalog = build_catalog()
        self.assertEqual([definition.name for definition in catalog.definitions()],
                         ["text.normalize", "text.report"])
        with self.assertRaises(UnknownMoveError):
            catalog.invoke("unselected.operation", {})

    def pipe(self, document):
        with subprocess.Popen([*self.command, "text.normalize", "--stdin", "--json-errors"],
                              stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as first:
            with subprocess.Popen([*self.command, "text.report", "--stdin", "--input-key", "text", "--json-errors"],
                                  stdin=first.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as second:
                first.stdout.close()
                first.stdin.write(document)
                first.stdin.close()
                output, second_error = second.communicate(timeout=15)
                first_error = first.stderr.read()
                first.wait(timeout=15)
                return first.returncode, second.returncode, output, first_error, second_error

    def test_actual_pipeline_matches_the_same_python_result(self):
        text = "  Straße\u2003🍑  "
        first, second, output, first_error, second_error = self.pipe(
            json.dumps({"text": text}, ensure_ascii=False).encode("utf-8"))
        self.assertEqual((first, second), (0, 0), (first_error, second_error))
        self.assertEqual(json.loads(output), run_reference(text))
        self.assertEqual((first_error, second_error), (b"", b""))

    def test_upstream_failure_leaves_no_success_output_downstream(self):
        first, second, output, first_error, second_error = self.pipe(b'{"text":3}')
        self.assertEqual((first, second, output), (2, 2, b""))
        self.assertEqual(json.loads(first_error)["error"]["code"], "invalid_arguments")
        self.assertEqual(json.loads(second_error)["error"]["code"], "invalid_input")

    def test_provider_inspection_and_activation_are_explicit(self):
        unloaded = subprocess.run([sys.executable, "-I", "-m", "hidden_moves", "moves", "list", "--json"],
                                  capture_output=True, text=True, timeout=15)
        self.assertEqual(unloaded.returncode, 0, unloaded.stderr)
        self.assertEqual(json.loads(unloaded.stdout), [])
        loaded = subprocess.run([*self.command[:-2], "moves", "list", "--json"],
                                capture_output=True, text=True, timeout=15)
        self.assertEqual(loaded.returncode, 0, loaded.stderr)
        self.assertEqual([item["name"] for item in json.loads(loaded.stdout)],
                         ["text.normalize", "text.report"])
