from msps.ui import Printer


def print_test(printer: Printer) -> None:
    print("-" * 80)
    printer.print_result_l1(
        "current_profile",
        "next_profile",
    )
    print("-" * 80)
    printer.print_result_l2(
        "/home/testuser/.m2/",
        "current_profile",
        "next_profile",
        {
            "personal": "/home/testuser/.m2/settings__personal.xml",
            "work": "/home/testuser/.m2/settings__work.xml",
        },
    )
    print("-" * 80)
    printer.print_missing_profile(
        "/home/testuser/.m2/",
        "current_profile",
        {
            "personal": "/home/testuser/.m2/settings__personal.xml",
            "work": "/home/testuser/.m2/settings__work.xml",
        },
    )
    print("-" * 80)
    printer.print_profiles(
        {
            "personal": "/home/testuser/.m2/settings__personal.xml",
            "work": "/home/testuser/.m2/settings__work.xml",
        },
    )
    print("-" * 80)


def main() -> None:
    print_test(Printer())
