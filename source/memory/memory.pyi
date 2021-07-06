from abc import ABC, abstractmethod
from queue import Queue
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
    _inner_memory: List[IWord]

    @abstractmethod
    def allocate(self, number_of_words: int, owner_pid: int) -> List[Frame]: ...

    @staticmethod
    @abstractmethod
    def deallocate(frames): ...

    @property
    @abstractmethod
    def page_size(self) -> int: ...

    @property
    @abstractmethod
    def frame_amount(self) -> int: ...

    @property
    @abstractmethod
    def frames(self): ...

    @staticmethod
    @abstractmethod
    def zero_memory_in_frame(frame): ...


class MemoryManager(IMemoryManager, Memory):
    _frames: List[Frame]
    _frame_amount: int
    _page_size: int
    _processes: List
    _pid_gen: Any
    _pid_table: Dict
    _curr_process: Any
    process_queue: Queue

    def __init__(self, owner: IVirtualMachine, memory_length: int, page_size: int): ...

    def allocate(self, number_of_words: int, owner_pid: int) -> List[Frame]: ...

    def deallocate(self, frames: List[List[int]]) -> None: ...

    def get_next_free_frame(self) -> Frame: ...

    def end_current_process(self): ...

    def set_current_process(self, next_process): ...

class IProcessManager:
    def create_process(self, process_name: str, code: List[str]) -> int: ...

class ProcessManager():
    def __init__(self, owner) -> None: ...
