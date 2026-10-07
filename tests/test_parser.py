"""Тесты для парсера команд эмулятора оболочки."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from shell_emulator import parse_command  


class TestParseCommand(unittest.TestCase):
    """Проверки корректности разбора ввода."""

    def test_empty_line(self):
        self.assertEqual(parse_command(""), (None, []))

    def test_only_spaces(self):
        self.assertEqual(parse_command("    "), (None, []))

    def test_command_without_args(self):
        self.assertEqual(parse_command("ls"), ("ls", []))

    def test_command_with_args(self):
        self.assertEqual(
            parse_command("cd /home/user"), ("cd", ["/home/user"])
        )

    def test_extra_spaces(self):
        self.assertEqual(
            parse_command("  cd   /tmp  "), ("cd", ["/tmp"])
        )


if __name__ == "__main__":
    unittest.main()