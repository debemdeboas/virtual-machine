from abc import ABC, abstractmethod
from typing import List, Dict
from itertools import count

from source.command.command import to_word, EInvalidAddress, EShutdown
from source.memory.frame import Frame
from process import ProcessControlBlock


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
    def __init__(self, owner, memory_length, page_size):
        super().__init__(owner, memory_length)

        self._page_size = page_size
        self._frame_amount = self._length // self._page_size
        self._frames = []

        all_frame_addresses = [(f * self._page_size, (f + 1) * self._page_size - 1) for f in range(self._frame_amount)]
        index = 0
        for start_address, stop_address in all_frame_addresses:
            frame_addresses = [self._inner_memory[i] for i in range(start_address, stop_address + 1)]
            frame = Frame(frame_addresses, index)
            index += 1
            self._frames.append(frame)

        self._curr_frame = (0, self._frames[0])
        self._processes: List[ProcessControlBlock] = []
        self._pid_table: Dict[int] = {}
        self._pid_gen = count(0)

        self.create_process('system', ['STOP'])
        self._curr_process = self._processes[0]

    def allocate(self, number_of_words):
        # "I wish to allocate this number of words"
        # First, check if there is enough free size on the memory
        # Then, return the list of allocated frames

        from math import ceil

        needed_frames = ceil(number_of_words / self._page_size)
        try:
            frames = [self.get_next_free_frame() for _ in range(needed_frames)]
        except Exception as E:
            # There is not enough memory to allocate this process
            print(E)
            return

        # Mark frames as not free
        for frame in frames:
            frame.is_free = False

        return frames

    @staticmethod
    def deallocate(frames):
        # Mark each position in the given frames as free
        for frame in frames:
            for address in frame.addresses:
                # Zero the memory address to avoid errors later on
                address.command = to_word('____')
            frame.is_free = True

    def end_current_process(self):
        process = self._curr_process
        self.deallocate(process.frames)
        next_process = self._processes[int(self._pid_gen.__repr__()[5:].replace('(', '').replace(')', '')) - 1]
        if next_process == self._curr_process:
            print('No more processes. Ending CPU loop.')
            self.owner.cpu.queue_interrupt(EShutdown)
        self._curr_process = next_process
        print(f'Process {process.name} ended')
        del process

    def create_process(self, process_name, code):
        pid = next(self._pid_gen)
        commands = []
        for line in code:
            if command := to_word(line.lstrip(' ').lstrip('\t')):
                commands.append(command)
        process_size = len(commands)
        process_frames = self.allocate(process_size)

        # Load code into memory

        def divide_chunks(_list, _chunk_size):
            for i in range(0, len(_list), _chunk_size):
                yield _list[i: i + _chunk_size]

        divided_commands = list(divide_chunks(commands, self._page_size))

        for frame, memory in zip(process_frames, divided_commands):
            for address, word in zip(frame.addresses, memory):
                address.command = word.command

        process = ProcessControlBlock(f'{process_name.replace(" ", "")}_{pid}', pid, process_frames, process_size)
        self._processes.append(process)
        self._pid_table[process.pid] = len(self._processes) - 1
        return process.pid

    def get_next_free_frame(self) -> Frame:
        # Return the next free frame
        if self._curr_frame[1].is_free:
            frame_index = self._curr_frame[0]
            self._curr_frame = (frame_index + 1, self._frames[frame_index + 1])
            return self._frames[frame_index]
        else:
            for index, frame in enumerate(self._frames):
                if frame.is_free:
                    self._curr_frame = (index + 1, self._frames[index + 1])
                    return frame
        raise Exception('Out of memory')

    def relative_to_absolute_address(self, address: int) -> int:
        page = address // self._page_size
        offset = address % self._page_size
        return (self._curr_process.frames[page].index * self._page_size) + offset

    def access(self, address):
        # Address is a relative address for the current process
        absolute_address = self.relative_to_absolute_address(address)
        return self._inner_memory[absolute_address]

    def save(self, command, address=None):
        try:
            self.relative_to_absolute_address(address)
        except IndexError:  # Need to allocate more frames for this process
            new_frames = self.allocate(((address // self._page_size) - len(self._curr_process.frames)) * self._page_size + 1)
            self._curr_process.frames.extend(new_frames)
        absolute_address = self.relative_to_absolute_address(address)
        super(MemoryManager, self).save(command, absolute_address)
