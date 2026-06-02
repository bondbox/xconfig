# coding:utf-8

from dataclasses import dataclass
from os.path import dirname
from os.path import join
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest import main

sys.path.insert(0, join(dirname(__file__), ".."))
sys.path.insert(0, join(dirname(__file__), "..", "..", "xconfig"))
sys.path.insert(0, join(dirname(__file__), "..", "..", "xconfig_file"))

from xkits_config_file import ConfigFile
from xkits_config_toml import ConfigTOML


@dataclass
class FakeConfigTOML(ConfigTOML):
    name: str = "fake"


class TestConfigJSON(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.filename: Path = ConfigFile.DEFAULT_FILE.with_suffix(".toml")

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.config: FakeConfigTOML = FakeConfigTOML.load()

    def tearDown(self):
        pass

    def test_load(self):
        with TemporaryDirectory() as tmpdir:
            self.config.dumpf(path := Path(tmpdir) / self.filename)
            instance: FakeConfigTOML = FakeConfigTOML.loadf(path)
            self.assertIsInstance(instance, FakeConfigTOML)
            self.assertIsInstance(instance, ConfigTOML)
            self.assertEqual(instance.dumpf(), path)


if __name__ == "__main__":
    main()
