import threading
import time
import tkinter
from abc import ABC, abstractmethod
from pathlib import Path

from pyfiglet import figlet_format

from command import to_word
from cpu import Cpu
from memory import Memory


class IVirtualMachine(ABC, threading.Thread):
    """Virtual Machine Interface

    Implemented by the `VirtualMachine` class.
    """

    # noinspection PyMissingConstructor
    @abstractmethod
    def __init__(self, mem_size): ...

    @property
    @abstractmethod
    def memory(self): ...

    @property
    @abstractmethod
    def cpu(self): ...

    @abstractmethod
    def dump(self, e=None): ...


class VirtualMachine(IVirtualMachine):
    """Virtual Machine Controller

    Main virtual machine thread. Implements the `IVirtualMachine` interface.
    Contains a CPU and a Memory modules, that each refer to this object as their "owner" (or parent).
    """

    # noinspection PyMissingConstructor
    def __init__(self, mem_size, tk):
        """Creates a new Virtual Machine thread

        Creates both a CPU object and a Memory object as well.

        Args:
            mem_size (int): Total memory size
        """
        threading.Thread.__init__(self, daemon=False)

        self._cpu = Cpu(self)
        self._memory = Memory(self, mem_size)
        self.tk = tk
        if self.tk is not None:
            self.tk.tag_configure('current_command', background='misty rose')
            self.tk.tag_configure('exception_command', background='brown2')
            self.tk.bind('<Key>', lambda _: 'break')

    @property
    def memory(self):
        return self._memory

    @property
    def cpu(self):
        return self._cpu

    def load_from_file(self, file: Path):
        with open(file, 'r') as f:
            for index, line in enumerate(f):
                command = to_word(line.lstrip(' ').lstrip('\t'))
                self._memory.save(command, index)

    def run(self):
        """Thread loop
        """
        self._cpu.loop()

    def dump(self, e=None):
        if self.tk is not None:
            self.tk.delete('1.0', tkinter.END)
            for line in self.cpu.dump_list():
                self.tk.insert(tkinter.END, line)

            for index, line in enumerate(self.memory.dump_list()):
                if index == self.cpu.pc.value + 1:
                    if e:
                        self.tk.insert(tkinter.END, line, 'exception_command')
                    else:
                        self.tk.insert(tkinter.END, line, 'current_command')
                    continue
                self.tk.insert(tkinter.END, line)

            self.tk.pack()
            time.sleep(0.5)

        dump_file = Path('memory.dump')
        with open(dump_file, 'w') as f:
            f.write(figlet_format('Memory Dump', font='cyberlarge', width=120))
            f.write(figlet_format('----------', font='cybermedium', width=120))
            f.write(figlet_format('CPU', font='cybermedium', width=120))
            if e:
                f.write(f'---- Interruption----\n{e.__class__.__name__}: {e}\n')
            # Dump CPU information
            self.cpu.dump(f)
            f.write('\n')
            f.write(figlet_format('----------', font='cybermedium', width=120))
            f.write(figlet_format('Memory', font='cybermedium', width=120))
            # Dump memory
            self.memory.dump(f)
