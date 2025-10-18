# coding:utf-8

from dataclasses import dataclass
import os
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest import main

from xkits_config_file import ConfigFile
from xkits_config_toml import ConfigTOML


@dataclass
class FakeConfigTOML(ConfigTOML):
    name: str = "fake"


class TestConfigJSON(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.file: str = f"{ConfigFile.DEFAULT_FILE}.json"

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.config: FakeConfigTOML = FakeConfigTOML.load()

    def tearDown(self):
        pass

    def test_load(self):
        with TemporaryDirectory() as tmp:
            self.config.dumpf(path := os.path.join(tmp, self.file))
            instance: FakeConfigTOML = FakeConfigTOML.loadf(path)
            self.assertIsInstance(instance, FakeConfigTOML)
            self.assertIsInstance(instance, ConfigTOML)
            self.assertEqual(instance.dumpf(), path)


if __name__ == "__main__":
    main()
