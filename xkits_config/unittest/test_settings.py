# coding:utf-8

from typing import Optional
from typing import Union
from unittest import TestCase
from unittest import main

from attr import attrib
from attr import attrs
from typeguard import TypeCheckError

from xkits_config.attribute import __description__
from xkits_config.attribute import __version__
from xkits_config.settings import Settings


@attrs
class FakeModule(Settings):
    index: int = attrib()


@attrs
class FakeSettings(Settings):
    name: str = attrib()
    module: FakeModule | None = attrib(default=None)
    version: str | None = attrib(default=__version__)
    description: Optional[str] = attrib(default=None)


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

    def test_load_no_type(self):
        @attrs
        class FakeSetting0(Settings):
            name = attrib()  # pyright: ignore[reportGeneralTypeIssues]

        self.assertRaises(TypeError, FakeSetting0.load, name="FakeSetting0")

    def test_load_type_check_1(self):
        @attrs
        class FakeSetting1(Settings):
            ver: str = attrib()

        self.assertIsInstance(FakeSetting1.load(ver="v1"), FakeSetting1)
        self.assertRaises(TypeCheckError, FakeSetting1.load, ver=None)
        self.assertRaises(TypeCheckError, FakeSetting1.load, ver=1)

    def test_load_type_check_2(self):
        @attrs
        class FakeSetting2(Settings):
            ver: str | None = attrib()

        self.assertIsInstance(FakeSetting2.load(ver="v1"), FakeSetting2)
        self.assertIsInstance(FakeSetting2.load(ver=None), FakeSetting2)
        self.assertRaises(TypeCheckError, FakeSetting2.load, ver=1)

    def test_load_type_check_3(self):
        @attrs
        class FakeSetting3(Settings):
            ver: Union[str, int] = attrib()

        self.assertIsInstance(FakeSetting3.load(ver="v1"), FakeSetting3)
        self.assertRaises(TypeCheckError, FakeSetting3.load, ver=None)
        self.assertIsInstance(FakeSetting3.load(ver=1), FakeSetting3)

    def test_load_type_check_4(self):
        @attrs
        class FakeSetting4(Settings):
            ver: Union[str, int] | None = attrib()

        self.assertIsInstance(FakeSetting4.load(ver="v1"), FakeSetting4)
        self.assertIsInstance(FakeSetting4.load(ver=None), FakeSetting4)
        self.assertIsInstance(FakeSetting4.load(ver=1), FakeSetting4)

    def test_load_type_check_subclass(self):
        @attrs
        class FakeModule1(Settings):
            index: int = attrib()

        @attrs
        class FakeModule2(Settings):
            index: int = attrib()

        @attrs
        class FakeModule3(Settings):
            index: int = attrib()

        @attrs
        class FakeSettings(Settings):
            module: Union[FakeModule1, FakeModule2] | FakeModule3 = attrib()

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
