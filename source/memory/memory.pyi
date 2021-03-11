from abc import ABC, abstractmethod
from typing import List

from command import IBaseCommand
from virtual_machine import IVirtualMachine


class IMemory(ABC):
    @abstractmethod
    def __init__(self, owner: IVirtualMachine, memory_length: int): ...

    @abstractmethod
    def dump(self): ...

    @abstractmethod
    def access(self, address: int) -> IBaseCommand: ...

    @abstractmethod
    def save(self, command: IBaseCommand, address: int = None): ...


class Memory(IMemory):
    _inner_memory: List[IBaseCommand]

    def __init__(self, owner: IVirtualMachine, memory_length: int): ...

    def dump(self): ...

    def access(self, address: int) -> IBaseCommand: ...

    def save(self, command: IBaseCommand, address: int = None): ...
