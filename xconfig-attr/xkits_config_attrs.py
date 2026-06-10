# coding:utf-8

from typing import Any
from typing import Iterator
from typing import Type

from attr import Factory
from xkits_config_annot import Annot


def parse_attrs(cls: Type[Any]) -> Iterator[Annot]:
    from attr import Attribute  # pylint: disable=C0415
    from attr import NOTHING  # pylint: disable=C0415
    from attr import fields  # pylint: disable=C0415
    for field in fields(cls):
        field: Attribute
        if (default := field.default) is NOTHING:
            default = Annot.NULL
        elif isinstance(default, Factory):  # type: ignore
            default = default.factory  # type: ignore
        yield Annot(field.name, field.type, default)
