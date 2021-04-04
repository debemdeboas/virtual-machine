from abc import ABC, abstractmethod
from queue import Queue

from source.command.command import ETrap, EProgramEnd
from source.register.register import Register


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
    def dump(self, file): ...

    @abstractmethod
    def dump_list(self): ...

    @abstractmethod
    def queue_interrupt(self, interrupt): ...


class Cpu(ICpu):
    def __init__(self, owner):
        self.owner = owner

        self.registers = {}
        for i in range(10):
            self.registers[f'r{i}'] = Register()

        self.__program_counter = Register(0)
        self.__instruction_register = None
        self.__interruption_queue = Queue()  # Infinitely big interruption queue

    @property
    def pc(self):
        return self.__program_counter

    @property
    def ir(self):
        return self.__instruction_register

    @property
    def command_params(self):
        return {
            'mem': self.owner.memory,
            'pc': self.__program_counter,
            'registers': self.registers,
            'interrupt': self.queue_interrupt,  # Method pointer to the CPU's interruption queue
        }

    def loop(self):
        end_loop = False
        print('CPU: Start loop')
        while True:
            # Access the memory address stored in PC
            _curr_address = self.pc.value

            # Set IR to the command pointed by PC
            self.__instruction_register = self.owner.memory.access(int(_curr_address)).command

            # Load the command instance with CPU registers, memory and PC
            self.__instruction_register.set_instance_params(**self.command_params)

            # Don't dump to disk to save on disk I/O time, only update the TK interface
            self.owner.dump(to_file=False)

            # Execute the command
            self.__instruction_register.execute()

            # Check for any interruptions
            while self.__interruption_queue.qsize() > 0:
                interrupt = self.__interruption_queue.get_nowait()
                if isinstance(interrupt, ETrap):  # Software interruption triggered by the user program
                    interrupt.args[0]()  # Handle the interruption
                    continue
                elif isinstance(interrupt, EProgramEnd):  # STOP instruction
                    print('STOP received. Ending program.')

                # Some other exception (interruption) occurred, end the program execution
                with self.__interruption_queue.mutex:  # Guarantee thread-safety
                    self.__interruption_queue.queue.clear()
                self.owner.dump(interrupt)
                end_loop = True

            if end_loop:  # End loop before incrementing PC to dump the correct memory data
                break

            if self.pc.value == _curr_address:
                self.pc.value += 1
        print('CPU: End')

    def dump(self, file):
        file.writelines(self.dump_list())

    def dump_list(self):
        res = ['---- Program counter ----\n', f'{self.__program_counter}\n', '---- Instruction register ----\n',
               f'{self.__instruction_register.dump()}\n', '---- Registers ----\n']

        [res.append(f'{k}: {v}\n') for k, v in self.registers.items()]
        return res

    def queue_interrupt(self, interrupt):
        self.__interruption_queue.put(interrupt)
