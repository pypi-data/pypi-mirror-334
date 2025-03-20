#!/usr/bin/env python

import glob
import os
import re
import sys

from msps.config import Config
from msps.maven import Maven
from msps.model import MavenProfiles
from msps.ui import Printer

maven = Maven()
config = Config()
printer = Printer()


def find_settings_profiles() -> MavenProfiles:
    profiles = dict()
    for file in glob.glob(f"{maven.m2_home}/*.xml"):
        res = re.findall(config.settings_file_pattern, file)
        if res:
            if len(res) > 1:
                raise ValueError(
                    f"Wrong settings_file_pattern, multiple matches found {res}"
                )
            profiles.update({res[0]: os.path.join(maven.m2_home, file)})
    return dict(sorted(profiles.items()))


class Msps:
    def __init__(self) -> None:
        self._profiles = find_settings_profiles()
        if not self._profiles:
            raise FileNotFoundError("No settings profile file found")

        self._current_profile = self._get_current_profile()

    def switch_to(self, profile: str | None) -> None:
        if profile:
            self._validate_profile(profile)
            self._switch_to(profile)
        else:
            self.switch_next()

    def switch_next(self) -> None:
        self._switch_to(self._get_next_profile())

    def list(self) -> None:
        printer.print_profiles(self._profiles)

    def _get_current_profile(self) -> str | None:
        try:
            settings_file = str(os.readlink(maven.maven_settings))
        except FileNotFoundError:
            settings_file = None

        if not settings_file:
            return None

        return settings_file[settings_file.rfind("__") + 2 : settings_file.rfind(".")]

    def _get_next_profile(self) -> str:
        if not self._current_profile:
            return str(next(iter(self._profiles)))
        profiles: list[str] = list(self._profiles.keys())
        if profiles.index(self._current_profile) == len(profiles) - 1:
            return profiles[0]
        return profiles[profiles.index(self._current_profile) + 1]

    def _validate_profile(self, profile: str) -> None:
        if profile not in self._profiles:
            printer.print_missing_profile(maven.m2_home, profile, self._profiles)
            sys.exit(1)

    def _switch_to(self, next_profile: str) -> None:
        next_settings = self._profiles[next_profile]
        os.unlink(maven.maven_settings)
        os.symlink(next_settings, maven.maven_settings)

        printer.print_result_l2(
            maven.m2_home, self._current_profile, next_profile, self._profiles
        )
