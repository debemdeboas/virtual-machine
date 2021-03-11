import threading
from abc import ABC, abstractmethod
from pathlib import Path

from command import to_word
from cpu import Cpu
from memory import Memory


class IVirtualMachine(ABC, threading.Thread):
    # noinspection PyMissingConstructor
    @abstractmethod
    def __init__(self) -> None: ...

    @property
    @abstractmethod
    def memory(self): ...

    @abstractmethod
    def load_from_file(self, file): ...


class VirtualMachine(IVirtualMachine):
    def __init__(self):
        threading.Thread.__init__(self, daemon=False)

        self._cpu = Cpu(self)
        self._memory = Memory(self, 512)

    @property
    def memory(self): return self._memory

    def load_from_file(self, file: Path):
        with open(file, 'r') as f:
            for line in f:
                command = to_word(line)
                self._memory.append(command)

    def run(self) -> None:
        self._cpu.loop()
