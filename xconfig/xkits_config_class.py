# coding:utf-8

from typing import Any
from typing import Iterator
from typing import List
from typing import Type

from xkits_config_annot import Annot

try:
    from xkits_config_attrs import parse_attrs
except ImportError:  # pragma: no cover
    def parse_attrs(cls: Type[Any]) -> Iterator[Annot]:  # pragma: no cover
        raise NotImplementedError("Module xkits-config-attrs is not installed")


def parse_dataclass(cls: Type[Any]) -> Iterator[Annot]:
    from dataclasses import MISSING  # pylint: disable=C0415
    from dataclasses import fields  # pylint: disable=C0415
    for field in fields(cls):  # type: ignore
        if field.default_factory is not MISSING:
            default = field.default_factory()
        elif field.default is not MISSING:
            default = field.default
        else:
            default = Annot.NULL
        yield Annot(field.name, field.type, default)


def parse(cls: Type[Any]) -> List[Annot]:
    try:
        return list(parse_dataclass(cls))
    except TypeError:
        return list(parse_attrs(cls))
