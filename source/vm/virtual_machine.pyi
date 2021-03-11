import threading
from abc import ABC, abstractmethod
from pathlib import Path

from memory import IMemory


class IVirtualMachine(ABC, threading.Thread):
    @abstractmethod
    def __init__(self) -> None:
        ...

    @property
    @abstractmethod
    def memory(self) -> IMemory: ...

    @abstractmethod
    def load_from_file(self, file: Path): ...


class VirtualMachine(IVirtualMachine):
    def __init__(self):
        self._memory = None
        self._cpu = None
        ...

    @property
    def memory(self) -> IMemory: ...

    def load_from_file(self, file: Path) -> None: ...

    def run(self) -> None: ...
