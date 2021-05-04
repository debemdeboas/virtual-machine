from abc import ABC, abstractmethod
from typing import List, TextIO, Any, Dict

from source.vm.virtual_machine import IVirtualMachine
from source.word.word import IWord
from source.memory.frame import Frame


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


class IMemoryManager(IMemory):
    @abstractmethod
    def allocate(self, number_of_words: int, owner_pid: int) -> List[Frame]: ...

    @abstractmethod
    def deallocate(self, frames: List[List[int]]) -> None: ...

    @abstractmethod
    def create_process(self, process_name: str, code: List[str]) -> int: ...

    def end_current_process(self): ...


class MemoryManager(IMemoryManager, Memory):
    _frames: List[Frame]
    _frame_amount: int
    _page_size: int
    _processes: List
    _pid_gen: Any
    _pid_table: Dict

    def __init__(self, owner: IVirtualMachine, memory_length: int, page_size: int): ...

    def allocate(self, number_of_words: int, owner_pid: int) -> List[Frame]: ...

    def deallocate(self, frames: List[List[int]]) -> None: ...

    def create_process(self, process_name: str, code: List[str]) -> int: ...

    def get_next_free_frame(self) -> Frame: ...

    def end_current_process(self): ...