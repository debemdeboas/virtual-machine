import re
from abc import ABC, abstractmethod
from collections import namedtuple


class IBaseCommand(ABC):
    """
    Base Command interface

    This class is an interface to any commands that inherit from the BaseCommand class (that implements this class).
    This was created to avoid circular importing throughout the modules.
    """

    original: str

    @abstractmethod
    def __init__(self, opcode, **kwargs): ...

    @abstractmethod
    def dump(self): ...

    @abstractmethod
    def execute(self): ...

    @abstractmethod
    def set_instance_params(self, **kwargs): ...


class EInvalidCommand(Exception):
    """
    Invalid Command

    This interruption is thrown when a command is illegally-formatted.
    """
    pass


class ETrap(Exception):
    """
    Trap

    This interruption is thrown when there is a system call being made by the user.
    """
    pass


class EInvalidAddress(Exception):
    """
    Invalid Address

    This interruption is thrown when the user program tries to access illegal positions in the memory.
    """
    pass


class EProgramEnd(Exception):
    """
    Program End

    This interruption is thrown upon reaching a `STOP` command.
    """
    pass


class EMathOverflowError(OverflowError):
    """
    Math Overflow Error

    This interruption is thrown when there is an overflow during a mathematical operation.
    """
    pass


class BaseCommand(IBaseCommand):
    """
    Base Command class

    Every command inherits from this class, implementing their own `execute()` methods. Each command has to call
    `super()` upon construction to properly define its OPCODE. Objects created from this class and its children are
    dynamically allocated and have dynamic parameters (see `BaseCommand.__init__()`, near `self.__setattr__()`).
    """

    PARAMS = []  # Parameters defined here will become instance attributes (accessed as `<object>.<parameter>`).

    # noinspection PyMissingConstructor
    def __init__(self, opcode, *args):
        self.opcode = opcode
        self.original = f'{opcode} {args}'

        parameters = dict(zip(self.PARAMS, map(lambda x: x, args)))

        for key, value in parameters.items():
            try:
                self.__setattr__(key, int(value))
            except (ValueError, TypeError):  # Could not convert value to (int)
                self.__setattr__(key, value)

    def dump(self):
        res = f'{self.opcode}'
        for i in self.PARAMS:
            res += f' {i} : {self.__getattribute__(i)}'
        return res

    def execute(self):
        raise NotImplementedError

    def set_instance_params(self, **kwargs):
        """
        Set this command instance's extra parameters, such as `memory`, `pc` and `registers`.

        Args:
            **kwargs (Dict[str, Any]): Dictionary containing the extra parameters for this instance
        """

        for key, value in kwargs.items():
            self.__setattr__(key, value)

        try:
            self.r1 = self.registers[self.r1.strip(',').lower()]
        except KeyError as E:
            raise EInvalidCommand(f'Register {self.r1.strip(",")} is not a valid register value')
        except:
            pass

        try:
            self.r2 = self.registers[self.r2.strip(',').lower()]
        except KeyError as E:
            raise EInvalidCommand(f'Register {self.r2.strip(",")} is not a valid register value')
        except:
            pass


class Command_DATA(BaseCommand):
    PARAMS = ['p']

    def __init__(self, *args):
        super().__init__('DATA', *args)

    def execute(self) -> int:
        return self.p


class Command_EMPTY(BaseCommand):
    def __init__(self, *args):
        super().__init__('____', *args)

    def execute(self) -> int:
        return 0


class Command_JMP(BaseCommand):
    """Direct jump, absolute (immediate)

    Syntax:
        JMP p

    Micro-operation:
        PC <- p
    """

    PARAMS = ['p']

    def __init__(self, *args):
        super().__init__('JMP', *args)

    def execute(self):
        self.pc.value = self.p


class Command_JMPI(BaseCommand):
    # noinspection SpellCheckingInspection
    """Direct jump, with register

        Syntax:
            JMPI R1

        Micro-operation:
            PC <- R1
    """

    PARAMS = ['r1']

    def __init__(self, *args):
        # noinspection SpellCheckingInspection
        super().__init__('JMPI', *args)

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

    PARAMS = ['r1', 'r2']

    def __init__(self, *args):
        # noinspection SpellCheckingInspection
        super().__init__('JMPIG', *args)

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

    PARAMS = ['r1', 'r2']

    def __init__(self, *args):
        # noinspection SpellCheckingInspection
        super().__init__('JMPIL', *args)

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

    PARAMS = ['r1', 'r2']

    def __init__(self, *args):
        # noinspection SpellCheckingInspection
        super().__init__('JMPIE', *args)

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

    PARAMS = ['p']

    def __init__(self, *args):
        # noinspection SpellCheckingInspection
        super().__init__('JMPIM', *args)

    def execute(self):
        word = self.mem.access(self.p)
        if isinstance(word, Command_DATA):
            self.pc.value = word.execute()
        else:
            self.interruption_queue.put(EInvalidCommand(f'Address {self.p} does not contain any DATA'))


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

    PARAMS = ['p', 'r2']

    def __init__(self, *args):
        # noinspection SpellCheckingInspection
        super().__init__('JMPIGM', *args)

    def execute(self):
        if self.r2.value > 0:
            word = self.mem.access(self.p)
            if isinstance(word, Command_DATA):
                self.pc.value = word.execute()
            else:
                self.interruption_queue.put(EInvalidCommand(f'Address {self.p} does not contain any DATA'))
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

    PARAMS = ['p', 'r2']

    def __init__(self, *args):
        # noinspection SpellCheckingInspection
        super().__init__('JMPILM', *args)

    def execute(self):
        if self.r2.value < 0:
            word = self.mem.access(self.p)
            if isinstance(word, Command_DATA):
                self.pc.value = word.execute()
            else:
                self.interruption_queue.put(EInvalidCommand(f'Address {self.p} does not contain any DATA'))
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

    PARAMS = ['p', 'r2']

    def __init__(self, *args):
        # noinspection SpellCheckingInspection
        super().__init__('JMPIEM', *args)

    def execute(self):
        if self.r2.value == 0:
            word = self.mem.access(self.p)
            if isinstance(word, Command_DATA):
                self.pc.value = word.execute()
            else:
                self.interruption_queue.put(EInvalidCommand(f'Address {self.p} does not contain any DATA'))
        else:
            self.pc.value += 1


class Command_STOP(BaseCommand):
    """Halts the program execution

    Syntax:
        STOP
    """

    def __init__(self, *args):
        super().__init__('STOP', *args)

    def execute(self):
        self.interruption_queue.put(EProgramEnd())


class Command_ADDI(BaseCommand):
    """Immediate addition

    Syntax:
        ADDI R1, p

    Micro-operation:
        Rd <- R1 + p
    """

    PARAMS = ['r1', 'p']

    def __init__(self, *args):
        super().__init__('ADDI', *args)

    def execute(self):
        self.r1.value = self.r1.value + self.p


class Command_SUBI(BaseCommand):
    # noinspection SpellCheckingInspection
    """Immediate subtraction

        Syntax:
            SUBI R1, p

        Micro-operation:
            Rd <- R1 - p
    """

    PARAMS = ['r1', 'p']

    def __init__(self, *args):
        # noinspection SpellCheckingInspection
        super().__init__('SUBI', *args)

    def execute(self):
        self.r1.value = self.r1.value - self.p


class Command_ADD(BaseCommand):
    """Addition

    Syntax:
        ADD R1, R2

    Micro-operation:
        Rd <- R1 + R2
    """

    PARAMS = ['r1', 'r2']

    def __init__(self, *args):
        super().__init__('ADD', *args)

    def execute(self):
        self.r1.value = self.r1.value + self.r2.value


class Command_SUB(BaseCommand):
    """Subtraction

    Syntax:
        SUB R1, R2

    Micro-operation:
        R1 <- R1 - R2
    """

    PARAMS = ['r1', 'r2']

    def __init__(self, *args):
        super().__init__('SUB', *args)

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

    PARAMS = ['r1', 'r2']

    def __init__(self, *args):
        # noinspection SpellCheckingInspection
        super().__init__('MULT', *args)

    def execute(self):
        self.r1.value = self.r1.value * self.r2.value


class Command_LDI(BaseCommand):
    """Immediate load

    Syntax:
        LDI R1, p

    Micro-operation:
        R1 <- p
    """

    PARAMS = ['r1', 'p']

    def __init__(self, *args):
        super().__init__('LDI', *args)

    def execute(self):
        self.r1.value = self.p


class Command_LDD(BaseCommand):
    """Load from memory

    Syntax:
        LDD R1, [P]

    Micro-operation:
        R1 <- [P]
    """

    PARAMS = ['r1', 'p']

    def __init__(self, *args):
        super().__init__('LDD', *args)

    def execute(self):
        if isinstance((word := self.mem.access(self.p)), Command_DATA):
            self.r1.value = word.execute()
        else:
            self.interruption_queue.put(EInvalidCommand(f'Address {self.p} does not contain any DATA'))


class Command_STD(BaseCommand):
    """Store in memory

    Syntax:
        STD [P], R1

    Micro-operation:
        [P] <- R1
    """

    PARAMS = ['p', 'r1']

    def __init__(self, *args):
        super().__init__('STD', *args)

    def execute(self):
        self.mem.save(to_word(f'DATA {self.r1.value}\n'), self.p)


class Command_LDX(BaseCommand):
    """Indirect load from memory

    Syntax:
        LDX R1, [R2]

    Micro-operation:
        R1 <- [R2]
    """

    PARAMS = ['r1', 'r2']

    def __init__(self, *args):
        super().__init__('LDX', *args)

    def execute(self):
        word = self.mem.access(self.r2.value)
        if isinstance(word, Command_DATA):
            self.r1.value = word.execute()
        else:
            self.interruption_queue.put(EInvalidCommand(f'Address {self.p} does not contain any DATA'))


class Command_STX(BaseCommand):
    """Indirect store to memory

    Syntax:
        STX [R1], R2

    Micro-operation:
        [R1] <- R2
    """

    PARAMS = ['r1', 'r2']

    def __init__(self, *args):
        super().__init__('STX', *args)

    def execute(self):
        self.mem.save(to_word(f'DATA {self.r2.value}\n'), self.r1.value)


class Command_SWAP(BaseCommand):
    """Swap two registers

    Syntax:
        SWAP R1, R2

    Micro-operation:
        T <- R1
        R1 <- R2
        R2 <- T
    """

    PARAMS = ['r1', 'r2']

    def __init__(self, *args):
        super().__init__('SWAP', *args)

    def execute(self):
        self.r1.value, self.r2.value = self.r2.value, self.r1.value


class Command_TRAP(BaseCommand):
    """Send a TRAP to the CPU

    Make a system call encoded in R8 (see below).
    R9 represents the TRAP's extra parameters.

    System calls:

    R8 = 1: IN
        Read something from STDIO.
        In this case, R9 represents the address in memory in which the value read from STDIO will be stored.

    R8 = 2: OUT
        Print something to STDIO.
        In this case, R9 represents the address in memory in which the value to be printed is stored.

    Syntax:
        TRAP R8, R9
    """

    PARAMS = ['r1', 'r2']

    def __init__(self, *args):
        super().__init__('TRAP', *args)
        self.func = None

    def _sys_call_in(self):
        """Mock a system call to the I/O handler

        Equivalent to:
         `scanf("%d", R8)` (not `&R8` because R8 already points to an address)
        """

        # In a real system, this TRAP would call the keyboard driver
        word = input()
        self.mem.save(to_word(f'DATA {int(word)}'), self.r2.value)

    def _sys_call_out(self):
        """Mock a system call to the I/O handler

        Equivalent to:
         `printf("%d", *R8)` (not `R8` because it is a pointer to an address)
        """
        if isinstance((word := self.mem.access(self.r2.value)), Command_DATA):
            # In a real system, this TRAP would call the graphics card driver
            print(word.execute())
        else:
            self.interruption_queue.put(EInvalidCommand(f'Address {self.r2.value} does not contain any DATA'))

    def execute(self):
        self.func = {
            1: self._sys_call_in,
            2: self._sys_call_out,
        }[self.r1.value]
        self.interruption_queue.put(ETrap(self.func))


# noinspection SpellCheckingInspection
CommandInformation = namedtuple(
    'CommandInformation', ['opcode', 'regex_validator', 'classname'])

# noinspection SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,
# SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,
# SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,
# SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,
# SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,
# SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,
# SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,
# SpellCheckingInspection,SpellCheckingInspection
INFO = {
    'DATA': CommandInformation('DATA', r'DATA\s(-?\d+)', Command_DATA),
    '____': CommandInformation('____', r'____', Command_EMPTY),
    # Flow control:
    'JMP': CommandInformation('JMP', r'JMP\s(-?\d+)', Command_JMP),
    'JMPI': CommandInformation('JMPI', r'JMPI\s([R|r]\d+)', Command_JMPI),
    'JMPIG': CommandInformation('JMPIG', r'JMPIG\s([R|r]\d+),\s([R|r]\d+)', Command_JMPIG),
    'JMPIL': CommandInformation('JMPIL', r'JMPIL\s([R|r]\d+),\s([R|r]\d+)', Command_JMPIL),
    'JMPIE': CommandInformation('JMPIE', r'JMPIE\s([R|r]\d+),\s([R|r]\d+)', Command_JMPIE),
    'JMPIM': CommandInformation('JMPIM', r'JMPIM\s\[(\d+)\]', Command_JMPIM),
    'JMPIGM': CommandInformation('JMPIGM', r'JMPIGM\s\[(\d+)\],\s([R|r]\d+)', Command_JMPIGM),
    'JMPILM': CommandInformation('JMPILM', r'JMPILM\s\[(\d+)\],\s([R|r]\d+)', Command_JMPILM),
    'JMPIEM': CommandInformation('JMPIEM', r'JMPIEM\s\[(\d+)\],\s([R|r]\d+)', Command_JMPIEM),
    # Halt:
    'STOP': CommandInformation('STOP', r'STOP', Command_STOP),
    # Mathematical operations:
    'ADDI': CommandInformation('ADDI', r'ADDI\s([R|r]\d+),\s(-?\d+)', Command_ADDI),
    'SUBI': CommandInformation('SUBI', r'SUBI\s([R|r]\d+),\s(-?\d+)', Command_SUBI),
    'ADD': CommandInformation('ADD', r'ADD\s([R|r]\d+),\s([R|r]\d+)', Command_ADD),
    'SUB': CommandInformation('SUB', r'SUB\s([R|r]\d+),\s([R|r]\d+)', Command_SUB),
    'MULT': CommandInformation('MULT', r'MULT\s([R|r]\d+),\s([R|r]\d+)', Command_MULT),
    # Data (register) manipulation:
    'LDI': CommandInformation('LDI', r'LDI\s([R|r]\d+),\s(-?\d+)', Command_LDI),
    'LDD': CommandInformation('LDD', r'LDD\s([R|r]\d+),\s\[(\d+)\]', Command_LDD),
    'STD': CommandInformation('STD', r'STD\s\[(\d+)\],\s([R|r]\d+)', Command_STD),
    'LDX': CommandInformation('LDX', r'LDX\s([R|r]\d+),\s\[([R|r]\d+)\]', Command_LDX),
    'STX': CommandInformation('STX', r'STX\s\[([R|r]\d+)\],\s([R|r]\d+)', Command_STX),
    'SWAP': CommandInformation('SWAP', r'SWAP\s([R|r]\d+),\s([R|r]\d+)', Command_SWAP),
    # Traps:
    # 'TRAP': CommandInformation('TRAP', r'TRAP\s([R|r]\d+),\s([R|r]\d+)', Command_TRAP),
    # TRAP commands should not accept any registers besides R8 and R9 (see definition in `Command_TRAP`)
    'TRAP': CommandInformation('TRAP', r'TRAP\s([R|r]8),\s([R|r]9)', Command_TRAP),
}


def to_word(val):
    """
    Convert a `str` value to a BaseCommand-derived class.

    Args:
        val (str): Line to be converted

    Returns:
        IBaseCommand: The command object
    """

    try:
        opcode, *_ = val.split()
    except ValueError:  # Empty line
        opcode = val
    if ((c_info := INFO.get(opcode, None)) is not None) and \
            (match := re.match(c_info.regex_validator, val)):
        curr: IBaseCommand = c_info.classname(*match.groups())
        curr.original = val.rstrip('\n')
        return curr
    elif val.startswith('\n') or val.startswith(';'):
        curr: IBaseCommand = Command_EMPTY()
        curr.original = val.rstrip('\n')  # Either a comment (;) or a blank line
        return curr
    raise EInvalidCommand(f'Value \'{val.strip()}\' is not a valid command')
