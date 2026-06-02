# coding:utf-8

from os.path import dirname
from os.path import join
import sys
from typing import List
from unittest import TestCase
from unittest import main

from attr import attrib
from attr import attrs

sys.path.insert(0, join(dirname(__file__), ".."))
sys.path.insert(0, join(dirname(__file__), "..", "..", "xconfig"))

from xkits_config_annot import Annot
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

    def test_parse_attrs_default_null(self):
        @attrs
        class FakeSettings():
            name: str = attrib()

        for annot in (annots := list(parse_attrs(FakeSettings))):
            self.assertEqual(annot.default, Annot.NULL)

        self.assertEqual(len(annots), 1)

    def test_parse_attrs_default_factory(self):
        @attrs
        class FakeSettings():
            names: List[str] = attrib(factory=list)

        for annot in (annots := list(parse_attrs(FakeSettings))):
            self.assertIs(annot.default, list)

        self.assertEqual(len(annots), 1)


if __name__ == "__main__":
    main()
