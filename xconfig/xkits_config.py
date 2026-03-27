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

from xkits_config_annot import Annot
from xkits_config_class import parse
from xkits_lib.annot import each_annot

TS = TypeVar("TS", bound="Settings")


class Settings():
    ENVAR_PREFIX: Optional[str] = None  # Environment Variable Prefix

    def __iter__(self) -> Iterator[str]:
        return iter(vars(self))

    def __setitem__(self, name: str, value: Any) -> None:
        return self.set(name=name, value=value)

    def __getitem__(self, name: str) -> Any:
        return self.get(name=name)

    def __contains__(self, name: str) -> bool:
        return hasattr(self, name)

    def __getattribute__(self, name: str) -> Any:
        if callable(attr := super().__getattribute__(name)) or name[0] == "_" or name in ["ENVAR_PREFIX"]:  # noqa:E501
            return attr

        try:
            prefix: str = self.__get_envar_prefix
            key: str = f"{prefix}_{name}".upper()
            return os.environ[key]
        except KeyError:
            return attr

    @property
    def __get_envar_prefix(self) -> str:
        if isinstance(prefix := self.ENVAR_PREFIX, str) and len(prefix) > 0:
            return prefix

        return f"XC_{self.__class__.__name__}"

    def set(self, name: str, value: Any) -> None:
        setattr(self, name, value)

    def get(self, name: str) -> Any:
        return getattr(self, name)

    def dump(self) -> Dict[str, Any]:
        return {k: v.dump() if isinstance(v := self[k], Settings) else v for k in self}  # noqa:E501

    @classmethod
    def load(cls: Type[TS], **kwargs: Any) -> TS:
        args: Dict[str, Any] = {}

        for field in parse(cls):
            if (value := kwargs.get(field.name, field.default)) is Annot.NULL:
                raise ValueError(f"{cls.__name__}.{field.name} no default")

            if isinstance(value, Dict):
                _subclasses: List[Type[Settings]] = []

                for _arg in each_annot(field.type):
                    if isclass(_arg) and issubclass(_arg, Settings):
                        _subclasses.append(_arg)

                if len(_subclasses) > 1:
                    _subclass_str: str = ", ".join(f"'{_sub.__name__}'" for _sub in _subclasses)  # noqa:E501
                    raise TypeError(f"{cls.__name__}.{field.name} has multiple Settings: [{_subclass_str}]")  # noqa:E501

                if len(_subclasses) == 1:
                    value = _subclasses[0].load(**value)

            args[field.name] = value

        return cls(**args)
