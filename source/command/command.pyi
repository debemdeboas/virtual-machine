from abc import ABC, abstractmethod
from typing import Any, List

from memory import IMemory
from register import IRegister


class IBaseCommand(ABC):
    original: str

    @abstractmethod
    def __init__(self, opcode: str, **kwargs: List[Any]): ...

    @abstractmethod
    def dump(self) -> str: ...

    @abstractmethod
    def execute(self) -> Any: ...

    @abstractmethod
    def set_instance_params(self, **kwargs): ...


class BaseCommand(IBaseCommand):
    p = IRegister
    r2 = IRegister
    r1 = IRegister
    opcode = str
    original = str
    pc = IRegister
    mem = IMemory
    PARAMS: List[str]

    def __init__(self, opcode: str, *args: List[Any]): ...

    def dump(self) -> str: ...

    def execute(self, **kwargs): ...

    def set_instance_params(self, **kwargs): ...


def to_word(val: str) -> IBaseCommand: ...


class EInvalidCommand(Exception): ...

class EInterrupt(Exception): ...

class ETrap(Exception): ...
