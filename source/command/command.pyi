from abc import ABC, abstractmethod
from typing import Any, Dict

from memory import IMemory
from register import IRegister


class IBaseCommand(ABC):
    @abstractmethod
    def __init__(self, opcode: str, **kwargs: Dict[str, Any]): ...

    @abstractmethod
    def dump(self) -> str: ...

    @abstractmethod
    def execute(self) -> Any: ...


class BaseCommand(IBaseCommand):
    p = IRegister
    r2 = IRegister
    r1 = IRegister
    opcode = str
    pc = IRegister
    mem = IMemory

    def __init__(self, opcode: str, **kwargs: Dict[str, Any]): ...

    def dump(self) -> str: ...

    def execute(self, **kwargs): ...


def to_word(val: str) -> IBaseCommand: ...


class EInvalidCommand(Exception): ...
