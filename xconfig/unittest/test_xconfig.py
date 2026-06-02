# coding:utf-8

from dataclasses import dataclass
from dataclasses import field
import os
from os.path import dirname
from os.path import join
import sys
from typing import Dict
from typing import List
from typing import Optional
from typing import Union
from unittest import TestCase
from unittest import main
from unittest import mock

sys.path.insert(0, join(dirname(__file__), ".."))

from xkits_config import Settings
from xkits_config_annot import Annot

from attribute import __authors__
from attribute import __package_vers__
from attribute import __project_desc__


@dataclass
class FakeAuthor(Settings):
    name: str
    email: str


@dataclass
class FakeModule(Settings):
    files: Dict[str, Dict[str, str]] = field(default_factory=dict)
    index: int = 0


@dataclass
class FakePackage(Settings):
    version: Optional[str] = __package_vers__
    authors: List[FakeAuthor] = field(default_factory=list)
    modules: Dict[str, FakeModule] = field(default_factory=dict)


if sys.version_info >= (3, 10):
    @dataclass
    class FakeSettings(Settings):
        name: str
        package: FakePackage
        description: Union[str, None] = None
        # Environment Variable Prefix
        ENVAR_PREFIX: str = "FakeConfig"
else:
    @dataclass
    class FakeSettings(Settings):
        name: str
        package: FakePackage
        description: Union[str, None] = None
        # Environment Variable Prefix
        ENVAR_PREFIX: str = "FakeConfig"


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
            package=FakePackage(
                authors=[
                    FakeAuthor(name=__authors__[0]["name"], email=__authors__[0]["email"]),  # noqa:E501
                    FakeAuthor(name=__authors__[0]["name"], email=__authors__[0]["email"]),  # noqa:E501
                ],
                modules={
                    "module1": FakeModule(index=1),
                    "module2": FakeModule(index=2),
                    "module3": FakeModule(index=3),
                },
            ),
        )

    def tearDown(self):
        pass

    def test_iter(self):
        for key in self.instance:
            self.assertIn(key, ["name", "package", "description"])

    def test_contains(self):
        for key in ["name", "package", "description"]:
            self.assertIn(key, self.instance)

    def test_get(self):
        self.assertEqual(self.instance["ENVAR_PREFIX"], "FakeConfig")
        self.assertEqual(self.instance.ENVAR_PREFIX, "FakeConfig")
        self.assertIsInstance(self.instance["package"], FakePackage)
        self.assertIsInstance(self.instance.package, FakePackage)
        self.assertEqual(self.instance["name"], "FakeSettings")
        self.assertEqual(self.instance["description"], None)
        self.assertEqual(self.instance.name, "FakeSettings")
        self.assertEqual(self.instance.description, None)

        assert isinstance(package := self.instance.package, FakePackage)
        self.assertEqual(package.ENVAR_PREFIX, "FakeConfig_FakePackage")

    def test_get_environ(self):
        with mock.patch.dict(os.environ, {"FAKECONFIG_FAKEPACKAGE_VERSION": "FAKE1"}):  # noqa:E501
            self.assertEqual(self.instance.package.version, "FAKE1")

        @dataclass
        class FakeSettings2(Settings):
            version: str
            number = 1234567890

            @property
            def hello(self) -> str:
                return "world"

        with mock.patch.dict(os.environ, {
            "XC_FAKESETTINGS2_VERSION": "VERSION",
            "XC_FAKESETTINGS2_NUMBER": "12345678",
            "XC_FAKESETTINGS2_HELLO": "WORLD",
        }):
            instance = FakeSettings2(version="_VERSION_")
            self.assertEqual(instance.version, "VERSION")
            self.assertEqual(instance.number, 1234567890)
            self.assertEqual(instance.hello, "world")

    def test_set_description(self):
        self.instance["description"] = __project_desc__
        self.assertEqual(self.instance.description, __project_desc__)
        self.assertEqual(self.instance["description"], __project_desc__)

    def test_dump(self):
        self.assertEqual(self.instance.dump(), {
            "name": "FakeSettings",
            "package": {
                "authors": [
                    __authors__[0],
                    __authors__[0],
                ],
                "modules": {
                    "module1": {"files": {}, "index": 1},
                    "module2": {"files": {}, "index": 2},
                    "module3": {"files": {}, "index": 3},
                },
                "version": __package_vers__,
            },
            "description": None,
        })

    def test_load_dict_check_multiple_dict(self):
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

    def test_load_list_check_multiple_dict(self):
        @dataclass
        class FakeSettings(Settings):
            indexes: List[Union[Dict[str, str], Dict[str, int]]]

        self.assertRaises(TypeError, FakeSettings.load, indexes=[{"index": 1}])

    def test_load_list_check_multiple_list(self):
        @dataclass
        class FakeSettings(Settings):
            indexes: List[Union[List[str], List[int]]]

        self.assertRaises(TypeError, FakeSettings.load, indexes=[[1, 2, 3]])

    def test_load_list(self):
        @dataclass
        class FakeSubclass(Settings):
            indexes: List[Union[Dict[str, int], int]]

        @dataclass
        class FakeSettings(Settings):
            classes: List[List[FakeSubclass]]

        instance = FakeSettings.load(
            classes=[[{
                "indexes": [{"a": 1}, 2],
            }]],
        )
        self.assertEqual(instance.classes[0][0].indexes, [{"a": 1}, 2])

    def test_load_no_default(self):
        self.assertRaises(ValueError, FakeSettings.load)

    def test_load(self):
        instance = FakeSettings.load(
            name="FakeSettings",
            package={
                "authors": [
                    __authors__[0],
                    __authors__[0],
                ],
                "modules": {
                    "module1": {
                        "files": {
                            "dir1": {
                                "file1": "FakeFile",
                            },
                        },
                        "index": 1234567890,
                        "value": "FakeModule",
                    },
                },
            },
        )
        self.assertIsInstance(instance.package, FakePackage)
        self.assertIsInstance(instance.package.version, str)
        self.assertIsInstance(instance.package.authors, list)
        for author in instance.package.authors:
            self.assertIsInstance(author, FakeAuthor)
        self.assertIsInstance(instance.package.modules, dict)
        for module in instance.package.modules.values():
            self.assertIsInstance(module, FakeModule)
            self.assertIsInstance(module.files, dict)
            self.assertIsInstance(module.index, int)
            for k, v in module.files.items():
                self.assertEqual(k, "dir1")
                self.assertEqual(v, {"file1": "FakeFile"})
        self.assertEqual(instance.name, "FakeSettings")
        self.assertEqual(instance.description, None)

    def test_parse(self):
        class FakeSettings(Settings):
            pass

        self.assertRaises(Exception, FakeSettings.load)


if __name__ == "__main__":
    main()
