from abc import ABC, abstractmethod
from typing import List

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


class Cpu(ICpu):
    # noinspection PyMissingConstructor
    def __init__(self, owner):
        self.owner = owner

        self.__registers: List[Register] = []
        for _ in range(8):
            self.__registers.append(Register())

        self.__program_counter = Register()
        self.__instruction_register = None

    @property
    def pc(self):
        return self.__program_counter

    @property
    def ir(self):
        return self.__instruction_register

    def command_params(self, r1: Register, r2: Register, p: Register):
        return {
            'mem': self.owner.memory,
            'pc': self.__program_counter,
            'r1': r1,
            'r2': r2,
            'p': p
        }

    def loop(self):
        while True:
            # Accesses the memory address stored in PC
            _curr_address = self.pc.value

            # Sets IR to the command pointed by PC
            self.__instruction_register = self.owner.memory.access(_curr_address)

            # Execute the command
            try:
                self.__instruction_register.execute()
            except Exception:  # TODO: add EInterrupt
                pass  # Treat interruption
