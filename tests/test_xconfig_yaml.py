# coding:utf-8

from os.path import dirname
from os.path import join
import sys
from dataclasses import dataclass
import os
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest import main

sys.path.insert(0, join(dirname(__file__), "..", "xconfig_yaml"))
sys.path.insert(0, join(dirname(__file__), "..", "xconfig_file"))
sys.path.insert(0, join(dirname(__file__), "..", "xconfig"))

from xkits_config_file import ConfigFile
from xkits_config_yaml import ConfigYAML


@dataclass
class FakeConfigYAML(ConfigYAML):
    name: str = "fake"


class TestConfigJSON(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.file: str = f"{ConfigFile.DEFAULT_FILE}.json"

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.config: FakeConfigYAML = FakeConfigYAML.load()

    def tearDown(self):
        pass

    def test_load(self):
        with TemporaryDirectory() as tmp:
            self.config.dumpf(path := os.path.join(tmp, self.file))
            instance: FakeConfigYAML = FakeConfigYAML.loadf(path)
            self.assertIsInstance(instance, FakeConfigYAML)
            self.assertIsInstance(instance, ConfigYAML)
            self.assertEqual(instance.dumpf(), path)


if __name__ == "__main__":
    main()
