# coding:utf-8

from dataclasses import dataclass
from dataclasses import field
from os.path import dirname
from os.path import join
import sys
from typing import List
from unittest import TestCase
from unittest import main

sys.path.insert(0, join(dirname(__file__), "..", "xconfig_attr"))
sys.path.insert(0, join(dirname(__file__), "..", "xconfig"))

from xkits_config_annot import Annot
from xkits_config_class import parse_dataclass


class TestDataclass(TestCase):

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

    def test_parse_dataclass_default_null(self):
        @dataclass
        class FakeSettings():
            name: str

        for annot in (annots := list(parse_dataclass(FakeSettings))):
            self.assertEqual(annot.default, Annot.NULL)

        self.assertEqual(len(annots), 1)

    def test_parse_dataclass_default_factory(self):
        @dataclass
        class FakeSettings():
            names: List[str] = field(default_factory=list)

        for annot in (annots := list(parse_dataclass(FakeSettings))):
            self.assertIs(annot.default, list)

        self.assertEqual(len(annots), 1)


if __name__ == "__main__":
    main()
