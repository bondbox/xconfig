# coding:utf-8

from inspect import isclass
import os
from typing import Any
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import get_args
from typing import get_origin

from xkits_config_annot import Annot
from xkits_config_class import parse
from xkits_lib.annot import each_annot

TS = TypeVar("TS", bound="Settings")


class Settings():
    ENVAR_PREFIX: Optional[str] = None  # Environment Variable Prefix

    def __iter__(self) -> Iterator[str]:
        return iter(v for v in vars(self) if v not in ["ENVAR_PREFIX"])

    def __setitem__(self, name: str, value: Any) -> None:
        return self.set(name=name, value=value)

    def __getitem__(self, name: str) -> Any:
        return self.get(name=name)

    def __contains__(self, name: str) -> bool:
        return hasattr(self, name)

    def __getattribute__(self, name: str) -> Any:
        attr: Any = super().__getattribute__(name)

        if callable(attr) or name[0] == "_" or name in ["ENVAR_PREFIX"]:
            return attr

        if isinstance(attr, Settings) and attr.ENVAR_PREFIX is None:
            envar: str = self.__get_envar_prefix
            klass: str = attr.__class__.__name__
            attr.ENVAR_PREFIX = f"{envar}_{klass}"
            return attr

        return self.__get_attr(name=name, default=attr)

    @property
    def __get_envar_prefix(self) -> str:
        if isinstance(prefix := self.ENVAR_PREFIX, str) and len(prefix) > 0:
            return prefix

        return f"XC_{self.__class__.__name__}"

    def __get_annot(self, name: str):
        """Get annotation for specified class property"""
        return self.__class__.__annotations__.get(name)

    def __get_attr(self, name: str, default: Any) -> Any:
        if (annot := self.__get_annot(name=name)) is None:
            return default

        # environment variable only support str type
        if annot is str or str in get_args(annot):
            prefix: str = self.__get_envar_prefix
            key: str = f"{prefix}_{name}".upper()
            return os.environ.get(key, default)

        return default

    def set(self, name: str, value: Any) -> None:
        setattr(self, name, value)

    def get(self, name: str) -> Any:
        return getattr(self, name)

    def dump(self) -> Dict[str, Any]:

        def __dump(value: Any):
            if isinstance(value, dict):
                return {k: __dump(v) for k, v in value.items()}

            return value.dump() if isinstance(value, Settings) else value

        return {k: __dump(value=self[k]) for k in self if k not in ["ENVAR_PREFIX"]}  # noqa:E501

    @classmethod
    def load(cls: Type[TS], **kwargs: Any) -> TS:

        def __load_dict(ftype: Type[Any], value: Dict[str, Any]):
            _subclasses: List[Type[Settings]] = []
            _recursions: List[Type[Dict]] = []

            if (origin_is_dict := get_origin(ftype) is dict):
                _, ftype = get_args(ftype)

            for _annot in each_annot(ftype):
                if isclass(_annot) and issubclass(_annot, Settings):
                    _subclasses.append(_annot)
                elif get_origin(_annot) is dict:
                    _recursions.append(_annot)

            if len(_subclasses) + len(_recursions) > 1:
                raise TypeError("cannot define multiple Settings or Dict")

            if len(_subclasses) == 1:
                subclass = _subclasses[0]
                if origin_is_dict:
                    return {
                        k: subclass.load(**v) if isinstance(v, dict) else v
                        for k, v in value.items()
                    }
                return subclass.load(**value)

            if len(_recursions) == 1:
                return {k: __load_dict(_recursions[0], v) for k, v in value.items()}  # noqa:E501

            return value

        def __load(fields: List[Annot], values: Dict[str, Any]):
            _args: Dict[str, Any] = {}

            for field in fields:
                if (value := values.get(field.name, field.default)) is Annot.NULL:  # noqa:E501
                    raise ValueError(f"{cls.__name__}.{field.name} no default")

                if isinstance(value, Dict):
                    value = __load_dict(field.type, value)

                _args[field.name] = value

            return _args

        return cls(**__load(fields=parse(cls), values=kwargs))
