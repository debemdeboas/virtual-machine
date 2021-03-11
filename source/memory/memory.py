from abc import ABC, abstractmethod
from typing import List

from command import IBaseCommand, to_word


class IMemory(ABC):
    @abstractmethod
    def __init__(self, ): ...

    @abstractmethod
    def dump(self): ...

    @abstractmethod
    def access(self, address: int) -> IBaseCommand: ...

    @abstractmethod
    def save(self, command: IBaseCommand, address: int = None): ...


class Memory(IMemory):
    # noinspection PyMissingConstructor
    def __init__(self, owner, memory_length):
        self.owner = owner
        self._inner_memory: List[IBaseCommand] = []
        for _ in range(memory_length):
            self._inner_memory.append(to_word('____'))

    def dump(self):
        with open('mem.dump', 'w') as f:
            for index, command in enumerate(self._inner_memory):
                f.write(f'[{index}] [{command}]')

    def access(self, address):
        if 0 <= address < len(self._inner_memory):
            return self._inner_memory[address]
        else:
            return to_word('STOP "Index out of bounds"')

    def save(self, command, address=None):
        if address is not None:
            self._inner_memory.insert(address, command)
        else:
            self._inner_memory.append(command)
