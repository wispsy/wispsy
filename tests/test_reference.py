"""Observable behavior of the dependency-free reference."""

import json
import subprocess
import sys
import unittest

from wispsy.reference import normalize, report, run_reference


class ReferenceTests(unittest.TestCase):
    def test_normalization_and_report_are_explicit_separate_operations(self):
        self.assertEqual(normalize("  Hello\tWORLD\n"), "hello world")
        self.assertEqual(report(" A "), {"text": " A ", "words": 1, "characters": 3})
        self.assertEqual(run_reference("  Hello\tWORLD\n"),
                         {"text": "hello world", "words": 2, "characters": 11})

    def test_empty_and_unicode_inputs_have_defined_counts(self):
        self.assertEqual(run_reference(" \n\t"), {"text": "", "words": 0, "characters": 0})
        self.assertEqual(run_reference("  Straße\u2003🍑  "),
                         {"text": "strasse 🍑", "words": 2, "characters": 9})

    def test_module_cli_uses_the_same_reference(self):
        text = " Straße 🍑 "
        result = subprocess.run([sys.executable, "-I", "-m", "wispsy", text],
                                capture_output=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), run_reference(text))

    def test_cli_json_uses_utf8_independently_of_console_encoding(self):
        text = " Straße 🍑 "
        result = subprocess.run([sys.executable, "-I", "-c",
                                 "import sys; sys.stdout.reconfigure(encoding='cp1252'); "
                                 "from wispsy.reference import main; main()", text],
                                capture_output=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("🍑".encode("utf-8"), result.stdout)
        self.assertEqual(json.loads(result.stdout), run_reference(text))

    def test_reference_import_keeps_optional_integrations_unloaded(self):
        result = subprocess.run([sys.executable, "-I", "-c",
                                 "import sys, wispsy.reference; "
                                 "assert 'hidden_moves' not in sys.modules; "
                                 "assert 'func_seq' not in sys.modules"],
                                capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)

    if sys.version_info < (3, 14):
        def test_lower_python_floor_rejects_sequence_explicitly(self):
            result = subprocess.run([sys.executable, "-I", "-c", "import wispsy.sequence"],
                                    capture_output=True, text=True, timeout=15)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("requires Python 3.14", result.stderr)
