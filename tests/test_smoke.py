"""Scaffold smoke tests: every module imports and the entry points print help or version."""

import importlib
import subprocess
import sys
import unittest

MODULES = [
    "tinydb_journal", "tinydb_journal._upstream", "tinydb_journal.errors", "tinydb_journal.lock",
    "tinydb_journal.store", "tinydb_journal.log", "tinydb_journal.recovery",
    "tinydb_journal.checkpoint", "tinydb_journal.legacy_import", "tinydb_journal.index",
    "tinydb_journal.scenario", "tinydb_journal.cli", "tinydb_journal.harness",
    "tinydb_journal.report",
]


def run(*args):
    return subprocess.run([sys.executable, "-m", *args], capture_output=True, text=True, timeout=60)


class Smoke(unittest.TestCase):
    def test_modules_import(self):
        for name in MODULES:
            with self.subTest(module=name):
                importlib.import_module(name)

    def test_cli_version_and_help(self):
        self.assertIn("tinydb_journal 0.0.0", run("tinydb_journal", "--version").stdout)
        result = run("tinydb_journal", "--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("scenario", result.stdout)

    def test_planned_command_names_its_ticket(self):
        result = run("tinydb_journal", "scenario", "show", "x")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not implemented yet: see #13", result.stderr)

    def test_harness_help_and_planned(self):
        self.assertEqual(run("tinydb_journal.harness", "--help").returncode, 0)
        result = run("tinydb_journal.harness", "run", "--seed", "1", "--out", "x")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("see #24", result.stderr)


if __name__ == "__main__":
    unittest.main()
