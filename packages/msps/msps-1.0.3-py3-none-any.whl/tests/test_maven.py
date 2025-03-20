import os
import unittest
from unittest import mock

from msps.maven import Maven

HOME = os.environ["HOME"]


class TestMaven(unittest.TestCase):
    @mock.patch.dict(os.environ, {"M2_HOME": "/custom/path"})
    def test_M2_HOME1(self) -> None:
        self.assertEqual(Maven().m2_home, "/custom/path")

    def test_M2_HOME2(self) -> None:
        self.assertEqual(Maven().m2_home, f"{HOME}/.m2")
