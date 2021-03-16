from abc import ABC, abstractmethod
from typing import Any, List

from source.memory.memory import IMemory
from source.register.register import IRegister


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


class Command_TRAP(BaseCommand):
    def handle_trap(self): ...


def to_word(val: str) -> IBaseCommand: ...


class EInvalidCommand(Exception): ...


class ETrap(Exception): ...


class EInvalidAddress(Exception): ...


class EProgramEnd(Exception): ...


class EMathOverflowError(OverflowError): ...
