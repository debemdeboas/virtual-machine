from abc import ABC, abstractmethod
from typing import List, TextIO

from source.vm.virtual_machine import IVirtualMachine
from source.word.word import IWord


class IMemory(ABC):
    @abstractmethod
    def dump(self, file: TextIO): ...

    @abstractmethod
    def dump_list(self) -> List[str]: ...

    @abstractmethod
    def access(self, address: int) -> IWord: ...

    @abstractmethod
    def save(self, command: IWord, address: int = None): ...


class Memory(IMemory):
    _inner_memory: List[IWord]
    _length: int
    _pos: int

    def __init__(self, owner: IVirtualMachine, memory_length: int): ...

    def dump(self, file: TextIO): ...

    def dump_list(self) -> List[str]: ...

    def access(self, address: int) -> IWord: ...

    def save(self, command: IWord, address: int = None): ...
