from rich.console import Console, Group, RenderableType
from rich.panel import Panel
from rich.text import Text

from msps.model import MavenProfiles

TITLE = "Maven Settings Profile Switcher"


class Printer:
    def _print(self, *contents: RenderableType, style: str) -> None:
        group = Group(*contents)
        panel = Panel.fit(
            group,
            title=TITLE,
            padding=(1, 2),
            style=style,
        )
        console = Console()
        console.print(panel)

    def text_label_value(self, label: str, value: str, value_color: str) -> Text:
        text = Text(f"{label}: ")
        text.append(value, style=f"{value_color} bold")
        return text

    def text_settings_profiles(self, settings_profiles: MavenProfiles) -> Text:
        text = Text("Available settings profiles: ")
        for profile, settings_file in settings_profiles.items():
            text.append("\n  - ")
            text.append(profile, style="yellow bold")
            text.append(" (")
            text.append(settings_file, style="yellow")
            text.append(")")
        return text

    def text_change_profile(
        self, current_profile: str | None, next_profile: str
    ) -> Text:
        text = Text("Profile changed from ")
        text.append(current_profile or "<empty>", style="cyan bold")
        text.append(" to ")
        text.append(next_profile, style="blue bold")
        text.append(".")
        return text

    def print_result_l1(self, current_profile: str, next_profile: str) -> None:
        self._print(
            self.text_change_profile(current_profile, next_profile),
            style="white",
        )

    def print_result_l2(
        self,
        m2_home: str,
        current_profile: str | None,
        next_profile: str,
        settings_profiles: MavenProfiles,
    ) -> None:
        self._print(
            self.text_label_value("M2_HOME", m2_home, "white"),
            self.text_settings_profiles(settings_profiles),
            self.text_change_profile(current_profile, next_profile),
            style="white",
        )

    def print_missing_profile(
        self,
        m2_home: str,
        next_profile: str,
        settings_profiles: MavenProfiles,
    ) -> None:
        self._print(
            self.text_label_value("Missing profile", next_profile, "red"),
            "",
            self.text_label_value("M2_HOME", m2_home, "white"),
            self.text_settings_profiles(settings_profiles),
            "No changes were made.",
            style="white on rgb(50,0,0)",
        )

    def print_profiles(self, settings_profiles: MavenProfiles) -> None:
        self._print(
            self.text_settings_profiles(settings_profiles),
            style="white",
        )
