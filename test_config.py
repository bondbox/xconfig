# coding:utf-8

from dataclasses import dataclass
import sys
from typing import Optional
from typing import Union
from unittest import TestCase
from unittest import main

from attr import attrib
from attr import attrs

from xkits_config import Settings
from xkits_config import __description__
from xkits_config import __version__


@dataclass
class FakeModule(Settings):
    index: int


if sys.version_info >= (3, 10):
    @attrs
    class FakeSettings(Settings):
        name: str = attrib()
        module: FakeModule | None = attrib(default=None)
        version: Optional[str] = attrib(default=__version__)
        description: Union[str, None] = attrib(default=None)
else:
    @attrs
    class FakeSettings(Settings):
        name: str = attrib()
        module: Optional[FakeModule] = attrib(default=None)
        version: Optional[str] = attrib(default=__version__)
        description: Union[str, None] = attrib(default=None)


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
            index: int = attrib()

        @attrs
        class FakeModule2(Settings):
            index: int = attrib()

        @dataclass
        class FakeModule3(Settings):
            index: int = attrib()

        if sys.version_info >= (3, 10):
            @attrs
            class FakeSettings(Settings):
                module: Union[FakeModule1, FakeModule2] | FakeModule3 = attrib()  # noqa:E501
        else:
            @attrs
            class FakeSettings(Settings):
                module: Union[FakeModule1, FakeModule2, FakeModule3] = attrib()

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


if __name__ == "__main__":
    main()
