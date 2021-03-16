from abc import ABC, abstractmethod
from typing import Dict, Union, Any, TextIO, List

from source.command.command import IBaseCommand
from source.register.register import IRegister
from source.vm.virtual_machine import IVirtualMachine


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

    @abstractmethod
    def dump(self, file: TextIO): ...

    @abstractmethod
    def dump_list(self) -> List[str]: ...


class Cpu(ICpu):
    owner: IVirtualMachine
    registers: Dict[str, IRegister]

    __program_counter: IRegister
    __instruction_register: Union[IBaseCommand, None]

    def __init__(self, owner: IVirtualMachine): ...

    @property
    def pc(self) -> IRegister: ...

    @property
    def ir(self) -> IBaseCommand: ...

    @property
    def command_params(self) -> Dict[str, Any]: ...

    def loop(self): ...

    def dump(self, file: TextIO): ...

    def dump_list(self) -> List[str]: ...
