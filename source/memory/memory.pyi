from abc import ABC, abstractmethod
from typing import List, TextIO, Deque

from command import IBaseCommand
from virtual_machine import IVirtualMachine


class IMemory(ABC):
    @abstractmethod
    def __init__(self, owner: IVirtualMachine, memory_length: int): ...

    @abstractmethod
    def dump(self, file: TextIO): ...

    @abstractmethod
    def dump_list(self) -> List[str]: ...

    @abstractmethod
    def access(self, address: int) -> IBaseCommand: ...

    @abstractmethod
    def save(self, command: IBaseCommand, address: int = None): ...


class Memory(IMemory):
    _inner_memory: List[IBaseCommand]
    _length: int
    _pos: int

    def __init__(self, owner: IVirtualMachine, memory_length: int): ...

    def dump(self, file: TextIO): ...

    def dump_list(self) -> List[str]: ...

    def access(self, address: int) -> IBaseCommand: ...

    def save(self, command: IBaseCommand, address: int = None): ...
