# coding:utf-8

from os.path import dirname
from os.path import join
import sys
from unittest import TestCase
from unittest import main

from attr import attrib
from attr import attrs

sys.path.insert(0, join(dirname(__file__), "..", "xconfig_attr"))
sys.path.insert(0, join(dirname(__file__), "..", "xconfig"))

from xkits_config_attrs import parse_attrs


class TestAttrs(TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_attrs(self):
        @attrs
        class FakeSettings():
            name: str = attrib()

        self.assertEqual(len(list(parse_attrs(FakeSettings))), 1)


if __name__ == "__main__":
    main()
