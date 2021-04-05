from abc import ABC, abstractmethod
from queue import Queue
from typing import Dict, Union, Any, TextIO, List

from source.register.register import IRegister
from source.vm.virtual_machine import IVirtualMachine
from source.word.word import IWord


class ICpu(ABC):
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

    @abstractmethod
    def queue_interrupt(self, interrupt: Exception) -> None: ...


class Cpu(ICpu):
    owner: IVirtualMachine
    registers: Dict[str, IRegister]

    __program_counter: IRegister
    __instruction_register: Union[IWord, None]
    __interruption_queue: Queue

    def __init__(self, owner: IVirtualMachine): ...

    @property
    def pc(self) -> IRegister: ...

    @property
    def ir(self) -> IWord: ...

    @property
    def command_params(self) -> Dict[str, Any]: ...

    def loop(self): ...

    def dump(self, file: TextIO): ...

    def dump_list(self) -> List[str]: ...

    def queue_interrupt(self, interrupt: Exception) -> None: ...
