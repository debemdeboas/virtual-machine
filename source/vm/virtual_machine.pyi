import threading
from abc import ABC, abstractmethod
from pathlib import Path
from tkinter import Text

from source.cpu.cpu import ICpu
from source.memory.memory import IMemory


class IVirtualMachine(ABC, threading.Thread):
    @property
    @abstractmethod
    def memory(self) -> IMemory: ...

    @property
    @abstractmethod
    def cpu(self) -> ICpu: ...

    @abstractmethod
    def dump(self, e: Exception = None, to_file: bool = True) -> None: ...


class VirtualMachine(IVirtualMachine):
    _memory: IMemory
    _cpu: ICpu
    tk: Text

    def __init__(self, mem_size: int, tk: Text = None): ...

    @property
    def memory(self) -> IMemory: ...

    @property
    def cpu(self) -> ICpu: ...

    def load_from_file(self, file: Path) -> None: ...

    def run(self) -> None: ...

    def dump(self, e: Exception = None, to_file: bool = True) -> None: ...
