# coding:utf-8

from dataclasses import dataclass
from os.path import dirname
from os.path import join
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest import main

sys.path.insert(0, join(dirname(__file__), "..", "xconfig_file"))
sys.path.insert(0, join(dirname(__file__), "..", "xconfig"))

from xkits_config_file import ConfigFile
from xkits_config_json import ConfigJSON


@dataclass
class FakeConfigJSON(ConfigJSON):
    name: str = "fake"


class TestConfigJSON(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.filename: Path = ConfigFile.DEFAULT_FILE.with_suffix(".json")

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.config: FakeConfigJSON = FakeConfigJSON.load()

    def tearDown(self):
        pass

    def test_load(self):
        with TemporaryDirectory() as tmpdir:
            self.config.dumpf(path := Path(tmpdir) / self.filename)
            instance: FakeConfigJSON = FakeConfigJSON.loadf(str(path))
            self.assertEqual(instance.dumpf(str(path)), path)
            self.assertIsInstance(instance, FakeConfigJSON)
            self.assertIsInstance(instance, ConfigJSON)


if __name__ == "__main__":
    main()
