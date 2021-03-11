# import re
from abc import ABC, abstractmethod
from collections import namedtuple
from typing import Any, Dict


class IBaseCommand(ABC):
    @abstractmethod
    def __init__(self): ...

    @abstractmethod
    def dump(self): ...

    @abstractmethod
    def execute(self): ...


class EInvalidCommand(Exception):
    pass


class BaseCommand(IBaseCommand):
    # noinspection PyMissingConstructor
    def __init__(self, opcode: str, **kwargs: Dict[str, Any]):
        self.opcode = opcode

        for key, value in kwargs.items():
            self.__setattr__(key, value)

    def dump(self) -> str:
        return f'MEM: {self.mem} | PC: {self.pc} | {self.opcode} {self.r1.value} {self.r2.value} {self.p.value}\n'

    def execute(self) -> Any:
        raise NotImplementedError


class Command_DATA(BaseCommand):
    def __init__(self, **kwargs):
        super().__init__('DATA', **kwargs)

    def execute(self) -> int:
        return self.p.value


class Command_EMPTY(BaseCommand):
    def __init__(self, **kwargs):
        super().__init__('____', **kwargs)

    def execute(self) -> int:
        return 0


class Command_JMP(BaseCommand):
    """Direct jump, absolute (immediate)

    Syntax:
        JMP p

    Micro-operation:
        PC <- p
    """

    def __init__(self, **kwargs):
        super().__init__('JMP', **kwargs)

    def execute(self):
        self.pc.value = self.p.value


class Command_JMPI(BaseCommand):
    # noinspection SpellCheckingInspection
    """Direct jump, with register

        Syntax:
            JMPI R1

        Micro-operation:
            PC <- R1
        """

    def __init__(self, **kwargs):
        # noinspection SpellCheckingInspection
        super().__init__('JMPI', **kwargs)

    def execute(self):
        self.pc.value = self.r1.value


class Command_JMPIG(BaseCommand):
    # noinspection SpellCheckingInspection
    """Conditional jump, with register

        Jumps to `r1` only if `r2` is greater than zero.

        Syntax:
            JMPIG R1, R2

        Micro-operation:
            If R2 > 0
                Then PC <- R1
                Else PC <- PC + 1

        """

    def __init__(self, **kwargs):
        # noinspection SpellCheckingInspection
        super().__init__('JMPIG', **kwargs)

    def execute(self):
        if self.r2.value > 0:
            self.pc.value = self.r1.value
        else:
            self.pc.value += 1


class Command_JMPIL(BaseCommand):
    # noinspection SpellCheckingInspection
    """Conditional jump, with register

        Jumps to `r1` only if `r2` is lesser than zero.

        Syntax:
            JMPIL R1, R2

        Micro-operation:
            If R2 < 0
                Then PC <- R1
                Else PC <- PC + 1

        """

    def __init__(self, **kwargs):
        # noinspection SpellCheckingInspection
        super().__init__('JMPIL', **kwargs)

    def execute(self):
        if self.r2.value < 0:
            self.pc.value = self.r1.value
        else:
            self.pc.value += 1


class Command_JMPIE(BaseCommand):
    # noinspection SpellCheckingInspection
    """Conditional jump, with register

        Jumps to `r1` only if `r2` is equal to zero.

        Syntax:
            JMPIE R1, R2

        Micro-operation:
            If R2 = 0
                Then PC <- R1
                Else PC <- PC + 1

        """

    def __init__(self, **kwargs):
        # noinspection SpellCheckingInspection
        super().__init__('JMPIE', **kwargs)

    def execute(self):
        if self.r2.value == 0:
            self.pc.value = self.r1.value
        else:
            self.pc.value += 1


class Command_JMPIM(BaseCommand):
    # noinspection SpellCheckingInspection
    """Indirect jump, with memory

        Jumps to the address contained in the position `p`.

        Syntax:
            JMPIM [P]

        Micro-operation:
            PC <- [P]
        """

    def __init__(self, **kwargs):
        # noinspection SpellCheckingInspection
        super().__init__('JMPIM', **kwargs)

    def execute(self):
        word = to_word(self.mem.access(self.p.value))
        if isinstance(word, Command_DATA):
            self.pc.value = word.execute()
        else:  # TODO: Add memory area for exceptions
            self.pc.value = -1


class Command_JMPIGM(BaseCommand):
    # noinspection SpellCheckingInspection
    """Conditional indirect jump, with memory

        Jumps to the address contained in the position `p` only if `r2` is greater than zero.

        Syntax:
            JMPIGM [P], R2

        Micro-operation:
            If R2 > 0
                Then PC <- [P]
                Else PC <- PC + 1
        """

    def __init__(self, **kwargs):
        # noinspection SpellCheckingInspection
        super().__init__('JMPIGM', **kwargs)

    def execute(self):
        if self.r2.value > 0:
            word = to_word(self.mem.access(self.p.value))
            if isinstance(word, Command_DATA):
                self.pc.value = word.execute()
            else:  # TODO: Add memory area for exceptions
                self.pc.value = -1
        else:
            self.pc.value += 1


class Command_JMPILM(BaseCommand):
    # noinspection SpellCheckingInspection
    """Conditional indirect jump, with memory

        Jumps to the address contained in the position `p` only if `r2` is lesser than zero.

        Syntax:
            JMPILM [P], R2

        Micro-operation:
            If R2 < 0
                Then PC <- [P]
                Else PC <- PC + 1
        """

    def __init__(self, **kwargs):
        # noinspection SpellCheckingInspection
        super().__init__('JMPILM', **kwargs)

    def execute(self):
        if self.r2.value < 0:
            word = to_word(self.mem.access(self.p.value))
            if isinstance(word, Command_DATA):
                self.pc.value = word.execute()
            else:  # TODO: Add memory area for exceptions
                self.pc.value = -1
        else:
            self.pc.value += 1


class Command_JMPIEM(BaseCommand):
    # noinspection SpellCheckingInspection
    """Conditional indirect jump, with memory

        Jumps to the address contained in the position `p` only if `r2` is equal to zero.

        Syntax:
            JMPIEM [P], R2

        Micro-operation:
            If R2 = 0
                Then PC <- [P]
                Else PC <- PC + 1
        """

    def __init__(self, **kwargs):
        # noinspection SpellCheckingInspection
        super().__init__('JMPIEM', **kwargs)

    def execute(self):
        if self.r2.value == 0:
            word = to_word(self.mem.access(self.p.value))
            if isinstance(word, Command_DATA):
                self.pc.value = word.execute()
            else:  # TODO: Add memory area for exceptions
                self.pc.value = -1
        else:
            self.pc.value += 1


class Command_STOP(BaseCommand):
    """Halts the program execution

    Syntax:
        STOP
    """

    def __init__(self, **kwargs):
        super().__init__('STOP', **kwargs)

    def execute(self):
        self.pc.value = -1


class Command_ADDI(BaseCommand):
    """Immediate addition

    Syntax:
        ADDI R1, p

    Micro-operation:
        Rd <- R1 + p
    """

    def __init__(self, **kwargs):
        super().__init__('ADDI', **kwargs)

    def execute(self):
        self.r1.value = self.r1.value + self.p.value


class Command_SUBI(BaseCommand):
    # noinspection SpellCheckingInspection
    """Immediate subtraction

        Syntax:
            SUBI R1, p

        Micro-operation:
            Rd <- R1 - p
        """

    def __init__(self, **kwargs):
        # noinspection SpellCheckingInspection
        super().__init__('SUBI', **kwargs)

    def execute(self):
        self.r1.value = self.r1.value - self.p.value


class Command_ADD(BaseCommand):
    """Addition

    Syntax:
        ADD R1, R2

    Micro-operation:
        Rd <- R1 + R2
    """

    def __init__(self, **kwargs):
        super().__init__('ADD', **kwargs)

    def execute(self):
        self.r1.value = self.r1.value + self.r2.value


class Command_SUB(BaseCommand):
    """Subtraction

    Syntax:
        SUB R1, R2

    Micro-operation:
        R1 <- R1 - R2
    """

    def __init__(self, **kwargs):
        super().__init__('SUB', **kwargs)

    def execute(self):
        self.r1.value = self.r1.value - self.r2.value


class Command_MULT(BaseCommand):
    # noinspection SpellCheckingInspection
    """Multiplication

        Syntax:
            MULT R1, R2

        Micro-operation:
            R1 <- R1 * R2
        """

    def __init__(self, **kwargs):
        # noinspection SpellCheckingInspection
        super().__init__('MULT', **kwargs)

    def execute(self):
        self.r1.value = self.r1.value * self.r2.value


class Command_LDI(BaseCommand):
    """Immediate load from memory

    Syntax:
        LDI R1, p

    Micro-operation:
        R1 <- p
    """

    def __init__(self, **kwargs):
        super().__init__('LDI', **kwargs)

    def execute(self):
        self.r1.value = self.p.value


class Command_LDD(BaseCommand):  # FIXME: Loads the value stored in position P of the memory? Loads the command itself?
    """Load from memory

    Syntax:
        LDD R1, [P]

    Micro-operation:
        R1 <- [P]
    """

    def __init__(self, **kwargs):
        super().__init__('LDD', **kwargs)

    def execute(self):
        word = to_word(self.mem.access(self.p.value))
        if isinstance(word, Command_DATA):
            self.r1.value = word.execute()
        else:  # TODO: Add memory area for exceptions
            self.r1.value = -1


class Command_STD(BaseCommand):
    """Store in memory

    Syntax:
        STD [P], R1

    Micro-operation:
        [P] <- R1
    """

    def __init__(self, **kwargs):
        super().__init__('STD', **kwargs)

    def execute(self):
        self.mem.save(Command_DATA(p=self.r1.value), self.p.value)


class Command_LDX(BaseCommand):
    """Indirect load from memory

    Syntax:
        LDX R1, [R2]

    Micro-operation:
        R1 <- [R2]
    """

    def __init__(self, **kwargs):
        super().__init__('LDX', **kwargs)

    def execute(self):
        word = to_word(self.mem.access(self.r2.value))
        if isinstance(word, Command_DATA):
            self.r1.value = word.execute()
        else:  # TODO: Add memory area for exceptions
            self.r1.value = -1


class Command_STX(BaseCommand):
    """Indirect store to memory

    Syntax:
        STX [R1], R2

    Micro-operation:
        [R1] <- R2
    """

    def __init__(self, **kwargs):
        super().__init__('STX', **kwargs)

    def execute(self):
        self.mem.save(Command_DATA(p=self.r2.value), self.r1.value)


class Command_SWAP(BaseCommand):
    """Swap two registers

    Syntax:
        SWAP R1, R2

    Micro-operation:
        T <- R1
        R1 <- R2
        R2 <- T
    """

    def __init__(self, **kwargs):
        super().__init__('STX', **kwargs)

    def execute(self):
        self.r1.value, self.r2.value = self.r2.value, self.r1.value


# noinspection SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection
REGEX_FORMATS = {
    'DATA': r'',
    '___': r'',
    # Flow control:
    'JMP': r'JMP\s(\d+)',
    'JMPI': r'JMPI\s([R|r]\d+)',
    'JMPIG': r'JMPIG\s([R|r]\d+),\s([R|r]\d+)',
    'JMPIL': r'JMPIL\s([R|r]\d+),\s([R|r]\d+)',
    'JMPIE': r'JMPIE\s([R|r]\d+),\s([R|r]\d+)',
    'JMPIM': r'JMPIM\s(\[\d+\])',
    'JMPIGM': r'JMPIGM\s(\[\d+\]),\s([R|r]\d+)',
    'JMPILM': r'JMPILM\s(\[\d+\]),\s([R|r]\d+)',
    'JMPIEM': r'JMPIEM\s(\[\d+\]),\s([R|r]\d+)',
    # Halt:
    'STOP': r'',
    # Mathmatical operations:
    'ADDI': r'ADDI\s([R|r]\d+),\s(\d+)',
    'SUBI': r'SUBI\s([R|r]\d+),\s(\d+)',
    'ADD': r'ADD\s([R|r]\d+),\s([R|r]\d+)',
    'SUB': r'SUB\s([R|r]\d+),\s([R|r]\d+)',
    'MULT': r'MULT\s([R|r]\d+),\s([R|r]\d+)',
    # Data (register) manipulation:
    'LDI': r'LDI\s([R|r]\d+),\s(\d+)',
    'LDD': r'LDD\s([R|r]\d+),\s\([\d+\])',
    'STD': r'STD\s(\[\d+\]),\s([R|r]\d+)',
    'LDX': r'LDX\s([R|r]\d+),\s\[([R|r]\d+)\]',
    'STX': r'STX\s\[([R|r]\d+)\],\s([R|r]\d+)',
    'SWAP': r'SWAP\s([R|r]\d+),\s([R|r]\d+)',
}

# noinspection SpellCheckingInspection
CommandInformation = namedtuple(
    'CommandInformation', ['opcode', 'regex_validator', 'classname'])

# noinspection SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection
INFO = {
    'DATA': CommandInformation('DATA', r'', Command_DATA),
    '____': CommandInformation('____', r'', Command_EMPTY),
    # Flow control:
    'JMP': CommandInformation('JMP', r'JMP\s(\d+)', Command_JMP),
    'JMPI': CommandInformation('JMPI', r'JMPI\s([R|r]\d+)', Command_JMPI),
    'JMPIG': CommandInformation('JMPIG', r'JMPIG\s([R|r]\d+),\s([R|r]\d+)', Command_JMPIG),
    'JMPIL': CommandInformation('JMPIL', r'JMPIL\s([R|r]\d+),\s([R|r]\d+)', Command_JMPIL),
    'JMPIE': CommandInformation('JMPIE', r'JMPIE\s([R|r]\d+),\s([R|r]\d+)', Command_JMPIE),
    'JMPIM': CommandInformation('JMPIM', r'JMPIM\s(\[\d+\])', Command_JMPIM),
    'JMPIGM': CommandInformation('JMPIGM', r'JMPIGM\s(\[\d+\]),\s([R|r]\d+)', Command_JMPIGM),
    'JMPILM': CommandInformation('JMPILM', r'JMPILM\s(\[\d+\]),\s([R|r]\d+)', Command_JMPILM),
    'JMPIEM': CommandInformation('JMPIEM', r'JMPIEM\s(\[\d+\]),\s([R|r]\d+)', Command_JMPIEM),
    # Halt:
    'STOP': CommandInformation('STOP', r'', Command_STOP),
    # Mathematical operations:
    'ADDI': CommandInformation('ADDI', r'ADDI\s([R|r]\d+),\s(\d+)', Command_ADDI),
    'SUBI': CommandInformation('SUBI', r'SUBI\s([R|r]\d+),\s(\d+)', Command_SUBI),
    'ADD': CommandInformation('ADD', r'ADD\s([R|r]\d+),\s([R|r]\d+)', Command_ADD),
    'SUB': CommandInformation('SUB', r'SUB\s([R|r]\d+),\s([R|r]\d+)', Command_SUB),
    'MULT': CommandInformation('MULT', r'MULT\s([R|r]\d+),\s([R|r]\d+)', Command_MULT),
    # Data (register) manipulation:
    'LDI': CommandInformation('LDI', r'LDI\s([R|r]\d+),\s(\d+)', Command_LDI),
    'LDD': CommandInformation('LDD', r'LDD\s([R|r]\d+),\s(\[\d+\])', Command_LDD),
    'STD': CommandInformation('STD', r'STD\s(\[\d+\]),\s([R|r]\d+)', Command_STD),
    'LDX': CommandInformation('LDX', r'LDX\s([R|r]\d+),\s\[([R|r]\d+)\]', Command_LDX),
    'STX': CommandInformation('STX', r'STX\s\[([R|r]\d+)\],\s([R|r]\d+)', Command_STX),
    'SWAP': CommandInformation('SWAP', r'SWAP\s([R|r]\d+),\s([R|r]\d+)', Command_SWAP),
}


def to_word(val: str):
    opcode, *params = val.split()
    if (command := INFO.get(opcode, None)) is not None:
        return command.classname(*params)
    raise EInvalidCommand
