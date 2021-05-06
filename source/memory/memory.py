from abc import ABC, abstractmethod
from itertools import count
from typing import List, Dict
from queue import Queue

from source.command.command import to_word, EInvalidAddress, EShutdown
from source.memory.frame import Frame
from source.memory.process import ProcessControlBlock


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

        for address in range(self._length):
            word = to_word('____')
            word.address = address
            self._inner_memory.append(word)

        self._pos = 0

    def dump(self, file):
        file.writelines(self.dump_list())

    def dump_list(self):
        res = ['---- Memory data ----\n']
        for index, word in enumerate(self._inner_memory):
            command = word.command
            res.append(f'[0x{index:3x}]\t{command.dump():25} | {command.original}\n')
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
                    self._inner_memory[address].command = command.command
                else:
                    self._inner_memory[self._pos].command = command.command
                    self._pos += 1
            except IndexError as E:
                raise EInvalidAddress(str(E))


class IMemoryManager(IMemory):
    @abstractmethod
    def allocate(self, number_of_words: int, owner_pid: int) -> List[Frame]: ...

    @staticmethod
    @abstractmethod
    def deallocate(self, frames): ...


class MemoryManager(Memory):
    @staticmethod
    def deallocate(frames):
        # Mark each position in the given frames as free
        for frame in frames:
            frame.is_free = True
            # Don't re-write the owner
            # frame.owner = 0  # System owns this frame now

    @staticmethod
    def zero_memory_in_frame(frame):
        for address in frame.addresses:
            address.command = to_word('____')

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

        self._processes: List[ProcessControlBlock] = []
        self._pid_table: Dict[int] = {}
        self._pid_gen = count(0)
        self.process_queue = Queue()

        self.create_process('system', ['STOP'])
        self._curr_process = self._processes[0]
        self.process_queue.queue.clear()

    def set_current_process(self, next_process):
        self._curr_process = next_process
        # TODO: check if process is ready
        self._curr_process.resume(self.owner.cpu.pc, self.owner.cpu.registers)

    def cpu_schedule_next_process(self, should_increment_pc):
        # Suspend the current process
        old_process = self._curr_process
        old_process.suspend(self.owner.cpu.pc, self.owner.cpu.registers, should_increment_pc)
        # Add suspended process to the CPU queue
        self.process_queue.put(old_process)
        # Choose the next process from the ready queue
        # Restore the CPU process of the next process
        self.schedule_next_process()
        # Give back control to the CPU
        return

    def schedule_next_process(self):
        process = self._curr_process
        try:
            if self.process_queue.qsize() > 0:
                self.set_current_process(self.process_queue.get_nowait())
            else:
                print('No more processes. Ending CPU loop.')
                self.owner.cpu.queue_interrupt(EShutdown())
            print(f'Process {process.name} has exited the CPU')
            print(f'Process {self._curr_process.name} has entered the CPU')
        except Exception as E:
            print('A fatal exception has occurred. Ending CPU loop.')
            self.owner.cpu.queue_interrupt(EShutdown(str(E)))

    def allocate(self, number_of_words, owner_pid):
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

        # Zero the memory
        for frame in frames:
            frame.owner = owner_pid
            self.zero_memory_in_frame(frame)

        return frames

    def end_current_process(self):
        process = self._curr_process
        p_name = process.name
        print(f'Process {p_name} has ended')
        self.schedule_next_process()
        self.deallocate(process.frames)

    def create_process(self, process_name, code):
        pid = next(self._pid_gen)
        commands = []
        for line in code:
            if command := to_word(line.lstrip(' ').lstrip('\t')):
                commands.append(command)
        process_size = len(commands)
        process_frames = self.allocate(process_size, pid)

        # Load code into memory

        def divide_chunks(_list, _chunk_size):
            for i in range(0, len(_list), _chunk_size):
                yield _list[i: i + _chunk_size]

        divided_commands = list(divide_chunks(commands, self._page_size))

        # Load commands into the memory frames
        for frame, commands_per_frame in zip(process_frames, divided_commands):
            for address, word in zip(frame.addresses, commands_per_frame):
                address.command = word.command

        process = ProcessControlBlock(f'{process_name.replace(" ", "")}_{pid}', pid, process_frames, process_size)
        self._processes.append(process)
        self._pid_table[process.pid] = len(self._processes) - 1
        self.process_queue.put(process)
        process.ready = True
        return process.pid

    def get_next_free_frame(self) -> Frame:
        # Return the next free frame
        for frame in self._frames:
            if frame.is_free:
                frame.is_free = False
                return frame
        raise Exception('Out of memory')

    def relative_to_absolute_address(self, address: int) -> int:
        page = address // self._page_size
        offset = address % self._page_size
        return (self._curr_process.frames[page].index * self._page_size) + offset

    def access(self, address):
        # Address is a relative address for the current process
        self._curr_process.current_frame = address // self._page_size
        self._curr_process.current_offset = address % self._page_size

        absolute_address = self.relative_to_absolute_address(address)
        return self._inner_memory[absolute_address]

    def save(self, command, address=None):
        try:
            self.relative_to_absolute_address(address)
        except IndexError:  # Need to allocate more frames for this process
            extra_words = ((address // self._page_size) - len(self._curr_process.frames)) * self._page_size + 1
            new_frames = self.allocate(extra_words, self._curr_process.pid)
            self._curr_process.frames.extend(new_frames)
        absolute_address = self.relative_to_absolute_address(address)
        super(MemoryManager, self).save(command, absolute_address)

    def dump_list(self):
        process_begin = '-------------------------------- BEGIN PROCESS ---------------------------------\n'
        process_end = '--------------------------------- END PROCESS ----------------------------------\n'
        pcb_data = ['---- PROCESS DATA ----\n']
        for process in self._processes:
            pcb_data.append(process_begin)
            pcb_data.extend(process.dump())
            pcb_data.append(process_end)
        pcb_data.append('\n---- ---- ----\n\n')

        memory_data = ['---- MEMORY DATA ----\n', '[ ADDRESS ][ FRAME INDEX ][ FRAME OWNER ] ORIGINAL COMMAND | '
                                                  'COMMAND\n']
        for index, word in enumerate(self._inner_memory):
            command = word.command
            frame_index = index // self._page_size
            frame = self._frames[frame_index]
            memory_data.append(f'[0x{index:3x}][0x{frame_index:2x}][{frame.owner:3}]\t{command.original:99} | '
                               f'{command.dump()}\n')
        return pcb_data + memory_data
