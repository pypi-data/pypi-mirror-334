import io
import unittest
from unittest import mock

from rich.console import Console

from msps.ui import Printer


def get_mock_console_output(mock_console: mock.Mock) -> str:
    with io.StringIO() as f:
        Console(file=f, highlight=False).print(mock_console.mock_calls[1].args[0])
        f.seek(0)
        return f.read()


class TestPrinter(unittest.TestCase):
    def setUp(self) -> None:
        self.printer = Printer()

    def test_print_result_l1(self) -> None:
        current_profile = "profile1"
        next_profile = "profile2"
        expected_output = (
            "╭────── Maven Settings Profile Switcher ───────╮\n"
            "│                                              │\n"
            "│  Profile changed from profile1 to profile2.  │\n"
            "│                                              │\n"
            "╰──────────────────────────────────────────────╯\n"
        )
        with mock.patch("msps.ui.Console") as mock_console:
            self.printer.print_result_l1(current_profile, next_profile)
            mock_console.assert_called_once_with()

            console_output = get_mock_console_output(mock_console)
            print(console_output)
            self.assertEqual(console_output, expected_output)

    def test_print_result_l2(self) -> None:
        m2_home = "/custom/path"
        current_profile = "profile1"
        next_profile = "profile2"
        settings_profiles = {"profile1": "settings1.xml", "profile2": "settings2.xml"}
        expected_output = (
            "╭────── Maven Settings Profile Switcher ───────╮\n"
            "│                                              │\n"
            "│  M2_HOME: /custom/path                       │\n"
            "│  Available settings profiles:                │\n"
            "│    - profile1 (settings1.xml)                │\n"
            "│    - profile2 (settings2.xml)                │\n"
            "│  Profile changed from profile1 to profile2.  │\n"
            "│                                              │\n"
            "╰──────────────────────────────────────────────╯\n"
        )
        with mock.patch("msps.ui.Console") as mock_console:
            self.printer.print_result_l2(
                m2_home, current_profile, next_profile, settings_profiles
            )
            mock_console.assert_called_once_with()

            console_output = get_mock_console_output(mock_console)
            self.assertEqual(console_output, expected_output)

    def test_print_missing_profile(self) -> None:
        m2_home = "/custom/path"
        next_profile = "profile1"
        settings_profiles = {"profile1": "settings1.xml", "profile2": "settings2.xml"}
        expected_output = (
            "╭─ Maven Settings Profile Switcher ─╮\n"
            "│                                   │\n"
            "│  Missing profile: profile1        │\n"
            "│                                   │\n"
            "│  M2_HOME: /custom/path            │\n"
            "│  Available settings profiles:     │\n"
            "│    - profile1 (settings1.xml)     │\n"
            "│    - profile2 (settings2.xml)     │\n"
            "│  No changes were made.            │\n"
            "│                                   │\n"
            "╰───────────────────────────────────╯\n"
        )
        with mock.patch("msps.ui.Console") as mock_console:
            self.printer.print_missing_profile(m2_home, next_profile, settings_profiles)
            mock_console.assert_called_once_with()

            console_output = get_mock_console_output(mock_console)
            print(console_output)
            self.assertEqual(console_output, expected_output)

    def test_print_profiles(self) -> None:
        settings_profiles = {"profile1": "settings1.xml", "profile2": "settings2.xml"}
        expected_output = (
            "╭─ Maven Settings Profile Switcher ─╮\n"
            "│                                   │\n"
            "│  Available settings profiles:     │\n"
            "│    - profile1 (settings1.xml)     │\n"
            "│    - profile2 (settings2.xml)     │\n"
            "│                                   │\n"
            "╰───────────────────────────────────╯\n"
        )
        with mock.patch("msps.ui.Console") as mock_console:
            self.printer.print_profiles(settings_profiles)
            mock_console.assert_called_once_with()

            console_output = get_mock_console_output(mock_console)
            print(console_output)
            self.assertEqual(console_output, expected_output)
