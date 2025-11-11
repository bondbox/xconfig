# coding:utf-8

from dataclasses import dataclass
from os.path import dirname
from os.path import join
import sys
from typing import Optional
from typing import Union
from unittest import TestCase
from unittest import main

sys.path.insert(0, join(dirname(__file__), "..", "xconfig_attr"))
sys.path.insert(0, join(dirname(__file__), "..", "xconfig"))

from xkits_config import Settings
from xkits_config_annot import Annot

from attribute import __description__
from attribute import __version__


@dataclass
class FakeModule(Settings):
    index: int


if sys.version_info >= (3, 10):
    @dataclass
    class FakeSettings(Settings):
        name: str
        module: FakeModule | None = None
        version: Optional[str] = __version__
        description: Union[str, None] = None
else:
    @dataclass
    class FakeSettings(Settings):
        name: str
        module: Optional[FakeModule] = None
        version: Optional[str] = __version__
        description: Union[str, None] = None


class TestAnnot(TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.instance = Annot(name="example", type=str)

    def tearDown(self):
        pass

    def test_str(self):
        name = repr(self.instance.name)
        type = repr(self.instance.type)
        default = repr(self.instance.default)
        expected = f"Annot(name={name},type={type},default={default})"
        self.assertEqual(str(self.instance), expected)


class TestSettings(TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.instance = FakeSettings(
            name="FakeSettings",
            module=FakeModule(index=1)
        )

    def tearDown(self):
        pass

    def test_iter(self):
        for key in self.instance:
            self.assertIn(key, ["name", "module", "version", "description"])

    def test_contains(self):
        for key in ["name", "module", "version", "description"]:
            self.assertIn(key, self.instance)

    def test_get(self):
        self.assertIsInstance(self.instance["module"], FakeModule)
        self.assertIsInstance(self.instance.module, FakeModule)
        self.assertEqual(self.instance["name"], "FakeSettings")
        self.assertEqual(self.instance["version"], __version__)
        self.assertEqual(self.instance["description"], None)
        self.assertEqual(self.instance.name, "FakeSettings")
        self.assertEqual(self.instance.version, __version__)
        self.assertEqual(self.instance.description, None)

    def test_set_description(self):
        self.instance["description"] = __description__
        self.assertEqual(self.instance.description, __description__)
        self.assertEqual(self.instance["description"], __description__)

    def test_dump(self):
        self.assertEqual(self.instance.dump(), {
            "name": "FakeSettings",
            "module": {"index": 1},
            "version": __version__,
            "description": None,
        })

    def test_load_no_default(self):
        self.assertRaises(ValueError, FakeSettings.load)

    def test_load_check_subclass_type(self):
        @dataclass
        class FakeModule1(Settings):
            index: int

        @dataclass
        class FakeModule2(Settings):
            index: int

        @dataclass
        class FakeModule3(Settings):
            index: int

        if sys.version_info >= (3, 10):
            @dataclass
            class FakeSettings(Settings):
                module: Union[FakeModule1, FakeModule2] | FakeModule3
        else:
            @dataclass
            class FakeSettings(Settings):
                module: Union[FakeModule1, FakeModule2, FakeModule3]
        self.assertRaises(TypeError, FakeSettings.load, module={"index": 1})

    def test_load(self):
        instance = FakeSettings.load(
            name="FakeSettings",
            module={
                "index": 1234567890,
                "value": "FakeModule"
            }
        )
        self.assertEqual(instance.name, "FakeSettings")
        self.assertEqual(instance.version, __version__)
        self.assertEqual(instance.description, None)

    def test_parse(self):
        class FakeSettings(Settings):
            pass

        self.assertRaises(Exception, FakeSettings.load)


if __name__ == "__main__":
    main()
