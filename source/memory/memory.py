from abc import ABC, abstractmethod

from source.command.command import to_word, EInvalidAddress


class IMemory(ABC):
    @abstractmethod
    def dump(self, file): ...

    @abstractmethod
    def dump_list(self): ...

    @abstractmethod
    def access(self, address): ...

    @abstractmethod
    def save(self, command, address): ...


class Memory(IMemory):
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
        for index, word in enumerate(self._inner_memory):
            command = word.command
            res.append(f'[{index:4d}]\t{command.dump():25} | {command.original:30}\n')
        return res

    def access(self, address):
        if 0 <= address < len(self._inner_memory) - 1:
            return self._inner_memory[address]
        else:
            raise EInvalidAddress('Index out of bounds')

    def save(self, command, address=None):
        if command is not None:
            try:
                if address is not None:
                    self._inner_memory[address] = command
                else:
                    self._inner_memory[self._pos] = command
                    self._pos += 1
            except IndexError as E:
                raise EInvalidAddress(str(E))


class IMemoryManager(IMemory):
    @abstractmethod
    def allocate(self, number_of_words): ...

    @abstractmethod
    def deallocate(self, frames): ...


class MemoryManager(Memory):
    def __init__(self, owner, memory_length, frame_amount, page_size):
        super().__init__(owner, memory_length)

        self._frame_amount = frame_amount
        self._page_size = page_size

        for i in range(self._frame_amount):
            self._frames.append([*range(i * 16, (i + 1) * 16 - 1)])

    def page_address_to_frame(self, page_address: int) -> int:
        return page_address // self._page_size

    def allocate(self, number_of_words):
        pass

    def deallocate(self, frames):
        pass