# coding:utf-8

from pathlib import Path
from typing import Iterator
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

from xkits_config import Settings

TCF = TypeVar("TCF", bound="ConfigFile")


class ConfigFile(Settings):
    DEFAULT_FILE: Path = Path("xconfig")

    def __iter__(self) -> Iterator[str]:
        return iter(v for v in super().__iter__() if v not in ["__xconfig_file__"])  # noqa:E501

    @property
    def filepath(self) -> Path:
        return getattr(self, "__xconfig_file__")

    @filepath.setter
    def filepath(self, value: Union[str, Path]) -> None:
        setattr(self, "__xconfig_file__", Path(value))

    def dumps(self) -> str:
        raise NotImplementedError()

    def dumpf(self, filepath: Optional[Union[str, Path]] = None) -> Path:
        """dump config to file"""
        if isinstance(filepath, str):
            filepath = Path(filepath)

        if not isinstance(filepath, Path):
            filepath = self.filepath

        from xkits_file.safefile import SafeWrite  # pylint: disable=C0415

        with SafeWrite(filepath, encoding=None, truncate=True) as whdl:
            whdl.write(self.dumps().encode("utf-8"))
            return filepath

    @classmethod
    def loads(cls: Type[TCF], data: str) -> TCF:
        raise NotImplementedError()

    @classmethod
    def loadf(cls: Type[TCF], filepath: Union[str, Path] = DEFAULT_FILE) -> TCF:  # noqa:E501
        """load config from file"""
        if isinstance(filepath, str):
            filepath = Path(filepath)

        from xkits_file.safefile import SafeRead  # pylint: disable=C0415

        with SafeRead(filepath, encoding=None) as rhdl:
            data: bytes = rhdl.read()

        instance = cls.loads(data=data.decode("utf-8"))
        instance.filepath = filepath
        return instance
