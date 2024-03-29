from abc import ABC, abstractmethod
from queue import Queue

from source.command.command import EIOOperationComplete, ETrap, EProgramEnd, EShutdown, ESignalVirtualAlarm
from source.register.register import Register

import logging

logging.basicConfig(level=logging.WARN)

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
        self.__instruction_register = ...
        self.__interruption_queue = Queue()  # Infinitely big interruption queue
        self.last_pc_value = 0  # Used in the memory dumping mechanism
        self.current_process_instruction_count = 0

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
            'interrupt': self.queue_interrupt,  # Method pointer to the CPU's interruption queue,
            'process_manager': self.owner.process_manager,  # Reference to the VM's process manager
        }

    def loop(self):
        end_loop = False
        logging.info('CPU: Start loop')
        while True:
            # Default to False on every loop
            skip_pc_increment = False

            # Access the memory address stored in PC
            _curr_address = self.pc.value

            # Set IR to the command pointed by PC
            self.__instruction_register = self.owner.process_manager.access(int(_curr_address))

            # Load the command instance with CPU registers, memory and PC
            self.__instruction_register.command.set_instance_params(**self.command_params)

            # Don't dump to disk to save on disk I/O time, only update the TK interface
            self.owner.dump(to_file=False)

            # Execute the command
            self.__instruction_register.command.execute()

            if self.current_process_instruction_count >= ESignalVirtualAlarm.SIGVTALRM_THRESHOLD:
                self.queue_interrupt(ESignalVirtualAlarm())
            else:
                self.current_process_instruction_count += 1

            # Check for any interruptions
            while self.__interruption_queue.qsize() > 0:
                interrupt = self.__interruption_queue.get_nowait()
                if isinstance(interrupt, ETrap):  # Software interruption triggered by the user program
                    self.owner.io_handler.queue_operation(self.owner.process_manager.current_process, interrupt.args[0])

                    # Give way to another process
                    self.owner.process_manager.cpu_schedule_next_process(self.pc.value == _curr_address, blocked=True)
                    self.current_process_instruction_count = 0
                    skip_pc_increment = True

                    continue
                elif isinstance(interrupt, EIOOperationComplete):  # An IO request has been fulfilled
                    response = interrupt.args[0]
                    self.owner.process_manager.unblock_process(response.process_id)

                    continue
                elif isinstance(interrupt, EProgramEnd):  # STOP instruction
                    logging.info('STOP received. Ending process.')
                    self.reset()
                    self.owner.process_manager.end_current_process()
                    # Process changing routine
                    skip_pc_increment = True
                    continue
                elif isinstance(interrupt, EShutdown):
                    self.pc.value = self.last_pc_value
                    logging.info('Shutting down...')
                elif isinstance(interrupt, ESignalVirtualAlarm):
                    # Give way to another process
                    self.owner.process_manager.cpu_schedule_next_process(self.pc.value == _curr_address)
                    self.current_process_instruction_count = 0
                    skip_pc_increment = True
                    continue
                else:
                    logging.error(f'Error: {interrupt}')

                # Some other exception (interruption) occurred, end the program execution
                with self.__interruption_queue.mutex:  # Guarantee thread-safety
                    self.__interruption_queue.queue.clear()
                self.owner.dump(interrupt)
                end_loop = True

            if end_loop:  # End loop before incrementing PC to dump the correct memory data
                break

            if (not skip_pc_increment) and (self.pc.value == _curr_address):
                self.pc.value += 1
        logging.info('CPU: End')

    def dump(self, file):
        file.writelines(self.dump_list())

    def dump_list(self):
        res = ['---- Program counter ----\n', f'{self.__program_counter}\n', '---- Instruction register ----\n',
               f'{self.__instruction_register.command.dump()}\n', '---- Registers ----\n']

        [res.append(f'{k}: {v}\n') for k, v in self.registers.items()]
        return res

    def queue_interrupt(self, interrupt):
        self.__interruption_queue.put(interrupt)

    def reset(self):
        self.last_pc_value = self.__program_counter.value
        self.__program_counter.value = 0
        self.current_process_instruction_count = 0
