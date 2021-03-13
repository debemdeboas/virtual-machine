import threading
from abc import ABC, abstractmethod
from pathlib import Path
from tkinter import Text

from memory import IMemory
from cpu import ICpu


class IVirtualMachine(ABC, threading.Thread):
    @abstractmethod
    def __init__(self, mem_size: int) -> None: ...

    @property
    @abstractmethod
    def memory(self) -> IMemory: ...

    @property
    @abstractmethod
    def cpu(self) -> ICpu: ...

    @abstractmethod
    def dump(self): ...



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

    def dump(self) -> None: ...
