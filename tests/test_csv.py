"""Regression tests for CSV input handling and CLI diagnostics."""
import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from shiftwatch.__main__ import main, read_column


class CsvInputTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "input.csv"

    def write(self, content):
        self.path.write_text(content, encoding="utf-8")
        return str(self.path)

    def test_bom_header(self):
        self.assertEqual(read_column(self.write("\ufeffvalue\n1\n2.5\n"), "value"), [1.0, 2.5])

    def test_missing_value_has_line_number(self):
        with self.assertRaisesRegex(ValueError, r"input.csv:3"):
            read_column(self.write("value\n1\n \n"), "value")

    def test_non_numeric_has_line_number(self):
        with self.assertRaisesRegex(ValueError, r"input.csv:3"):
            read_column(self.write("value\n1\nabc\n"), "value")

    def test_non_finite_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Non-finite"):
            read_column(self.write("value\nnan\n"), "value")

    def test_missing_column(self):
        with self.assertRaisesRegex(ValueError, "missing"):
            read_column(self.write("other\n1\n"), "value")

    def test_cli_outputs_valid_json(self):
        ref = self.write("value\n1\n2\n3\n")
        current = Path(self.tmp.name) / "current.csv"
        current.write_text("value\n1\n2\n4\n", encoding="utf-8")
        out = io.StringIO()
        with patch("sys.argv", ["shiftwatch", ref, str(current), "--column", "value"]), contextlib.redirect_stdout(out):
            main()
        report = json.loads(out.getvalue())
        self.assertEqual(report["reference_count"], 3)
        self.assertEqual(report["current_count"], 3)


if __name__ == "__main__":
    unittest.main()
