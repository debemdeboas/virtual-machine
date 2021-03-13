from abc import ABC, abstractmethod
from command import to_word
from collections import deque


class IMemory(ABC):
    @abstractmethod
    def __init__(self, owner, memory_length): ...

    @abstractmethod
    def dump(self, file): ...

    @abstractmethod
    def dump_list(self): ...

    @abstractmethod
    def access(self, address): ...

    @abstractmethod
    def save(self, command, address): ...


class Memory(IMemory):
    # noinspection PyMissingConstructor
    def __init__(self, owner, memory_length):
        self.owner = owner
        self._inner_memory = []
        self._length = memory_length

        for _ in range(self._length):
            self._inner_memory.append(to_word('____'))

        self._pos = 0

    def dump(self, file):
        file.writelines(self.dump_list())

    def dump_list(self):
        res = ['---- Memory data ----\n']
        for index, command in enumerate(self._inner_memory):
            res.append(f'[{index:4d}]\t{command.dump():25} | {command.original:30}\n')
        return res

    def access(self, address):
        if 0 <= address < len(self._inner_memory):
            return self._inner_memory[address]
        else:
            return to_word('STOP "Index out of bounds"')

    def save(self, command, address=None):
        if address is not None:
            self._inner_memory[address] = command
        else:
            self._inner_memory[self._pos] = command
            self._pos += 1
