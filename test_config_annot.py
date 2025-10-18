# coding:utf-8

from unittest import TestCase
from unittest import main

from xkits_config_annot import Annot


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


if __name__ == "__main__":
    main()
