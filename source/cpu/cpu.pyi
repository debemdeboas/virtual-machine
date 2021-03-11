from abc import ABC, abstractmethod
from typing import Union

from command import IBaseCommand
from register import IRegister
from virtual_machine import IVirtualMachine


class ICpu(ABC):
    @abstractmethod
    def __init__(self, ): ...

    @property
    @abstractmethod
    def pc(self): ...

    @property
    @abstractmethod
    def ir(self): ...

    @abstractmethod
    def loop(self): ...


class Cpu(ICpu):
    owner: IVirtualMachine
    __program_counter: IRegister
    __instruction_register: Union[IBaseCommand, None]

    def __init__(self, owner: IVirtualMachine): ...

    @property
    def pc(self) -> IRegister: ...

    @property
    def ir(self) -> IBaseCommand: ...

    def command_params(self, r1: IRegister, r2: IRegister, p: IRegister): ...

    def loop(self): ...
