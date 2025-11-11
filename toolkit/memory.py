# coding:utf-8

import os

from psutil import Process
from xkits_config import Settings


def memory_info(process: Process):
    memory_info = process.memory_info()
    print(f"VMS (Virtual Memory Size)\t{memory_info.vms / 1024 / 1024:.2f} MB\t{memory_info.vms}")  # noqa:E501
    print(f"RSS (Resident Set Size)  \t{memory_info.rss / 1024 / 1024:.2f} MB\t{memory_info.rss}")  # noqa:E501


def main():
    pid: int = os.getpid()
    print(f"Hello, PID {pid}")
    process: Process = Process(pid)
    print("Before load:")
    memory_info(process)

    from dataclasses import dataclass

    @dataclass
    class FakeSettings(Settings):
        name: str = "dataclass"

    FakeSettings.load()
    print("After load:")
    memory_info(process)
    print("Goodbye!")


if __name__ == "__main__":
    main()
