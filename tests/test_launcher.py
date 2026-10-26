"""Protect existing archives when upgrading to the Zenith name."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from zenith.__main__ import default_data_dir


class LauncherTests(unittest.TestCase):
    def test_new_install_uses_zenith_folder(self):
        with tempfile.TemporaryDirectory() as home:
            self.assertEqual(default_data_dir({}, home), Path(home) / ".zenith")

    def test_existing_archive_survives_empty_zenith_directory(self):
        with tempfile.TemporaryDirectory() as home:
            previous = Path(home) / ".meeting-assistant"
            previous.mkdir()
            (previous / "archive.sqlite3").write_bytes(b"existing archive")
            (Path(home) / ".zenith").mkdir()
            self.assertEqual(default_data_dir({}, home), previous)
            self.assertEqual((previous / "archive.sqlite3").read_bytes(), b"existing archive")

    def test_existing_zenith_archive_has_priority(self):
        with tempfile.TemporaryDirectory() as home:
            for name in (".meeting-assistant", ".zenith"):
                directory = Path(home) / name
                directory.mkdir()
                (directory / "archive.sqlite3").touch()
            self.assertEqual(default_data_dir({}, home), Path(home) / ".zenith")

    def test_configuration_precedence_and_legacy_variable(self):
        self.assertEqual(default_data_dir({"ZENITH_DATA_DIR": "new", "MINUTES_DATA_DIR": "old"}), Path("new"))
        self.assertEqual(default_data_dir({"MINUTES_DATA_DIR": "old"}), Path("old"))
        self.assertEqual(default_data_dir({"ZENITH_DATA_DIR": "", "MINUTES_DATA_DIR": "old"}), Path("old"))

    def test_current_and_previous_launch_commands(self):
        root = Path(__file__).resolve().parents[1]
        for package in ("zenith", "meeting_assistant"):
            result = subprocess.run([sys.executable, "-m", package, "--version"], cwd=root, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), "1.1.0")


if __name__ == "__main__":
    unittest.main()
