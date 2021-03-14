from abc import ABC, abstractmethod

from command import EInvalidCommand, ETrap, EInvalidAddress, EProgramEnd, EMathOverflowError, Command_TRAP
from register import Register


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


class Cpu(ICpu):
    # noinspection PyMissingConstructor
    def __init__(self, owner):
        self.owner = owner

        self.registers = {}
        for i in range(10):
            self.registers[f'r{i}'] = Register()

        self.__program_counter = Register(0)
        self.__instruction_register = None

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
            'registers': self.registers
        }

    def loop(self):
        print('CPU: Start loop')
        while True:
            # Access the memory address stored in PC
            _curr_address = self.pc.value

            # Set IR to the command pointed by PC
            self.__instruction_register = self.owner.memory.access(int(_curr_address))

            self.__instruction_register.set_instance_params(**self.command_params)

            self.owner.dump()

            # Execute the command
            try:
                self.__instruction_register.execute()
            except EInvalidCommand as E:
                self.owner.dump(E)
                break
            except EInvalidAddress as E:
                self.owner.dump(E)
                break
            except EProgramEnd as E:
                self.owner.dump(E)
                break
            except (EMathOverflowError, OverflowError) as E:
                self.owner.dump(E)
                break
            except ETrap as E:
                if isinstance(self.__instruction_register, Command_TRAP):
                    self.__instruction_register.handle_trap()
            except Exception as E:
                self.owner.dump(E)
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
