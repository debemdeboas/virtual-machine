from source.command.command import EShutdown
import threading
from abc import ABC, abstractmethod
from pathlib import Path

from pyfiglet import figlet_format

from source.cpu.cpu import Cpu
from source.memory.memory import MemoryManager, ProcessManager
from source.vm.io_handler import IOHandler

import socket


class IVirtualMachine(ABC, threading.Thread):
    """Virtual Machine Interface

    Implemented by the `VirtualMachine` class.
    """

    @property
    @abstractmethod
    def memory(self): ...

    @property
    @abstractmethod
    def cpu(self): ...

    @abstractmethod
    def dump(self, e=None, to_file=True): ...


class VirtualMachine(IVirtualMachine):
    """Virtual Machine Controller

    Main virtual machine thread. Implements the `IVirtualMachine` interface.
    Contains a CPU and a Memory modules, that each refer to this object as their "owner" (or parent).
    """

    def __init__(self, mem_size, create_shell_sock = False, tk=None):
        """Creates a new Virtual Machine thread

        Creates both a CPU object and a Memory object as well.

        Args:
            mem_size (int): Total memory size
            tk (Text): Tkinter Text object
        """

        threading.Thread.__init__(self, daemon=False)

        self._cpu = Cpu(self)
        self._memory = MemoryManager(self, mem_size, 16)
        self._process_manager = ProcessManager(self)
        self._io_handler = IOHandler(self)
        self._io_handler.start()
        self.end_threads = False

        if create_shell_sock:
            self.create_shell_socket()

    def create_shell_socket(self):
        def client(conn: socket.socket, vm):
            conn.settimeout(30)
            while True:
                if vm.end_threads:
                    break

                try:
                    data = conn.recv(4096)
                    if not data:
                        print('Shell connection closed')
                        break
                    command, _, *args = data.decode('ascii').partition(' ')
                    ret = {
                        'shutdown': lambda _: f'Halting... {vm.cpu.queue_interrupt(EShutdown()) or ""}',
                        'load': lambda path: f'New process PID: {vm.load_from_file(Path(path[0]))}'
                    }[command](args)
                    conn.sendall(ret.encode('ascii'))
                except BlockingIOError:
                    continue
                except socket.timeout:
                    continue
            conn.close()

        def shell_sock(vm):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
                s.bind(('localhost', 8899))
                s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

                print('Shell socket bound')
                s.listen()
                s.setblocking(False)
                while True:
                    if vm.end_threads:
                        break

                    try:
                        c, _ = s.accept()
                        proc = threading.Thread(target=client, daemon=True, args=(c, vm,))
                        proc.start()
                    except BlockingIOError:
                        continue
                s.close()
            except OSError as E:
                exit
        shell_sock_proc = threading.Thread(target=shell_sock, daemon=True, args=(self,))
        shell_sock_proc.start()

    @property
    def memory(self):
        return self._memory

    @property
    def cpu(self):
        return self._cpu
    
    @property
    def process_manager(self):
        return self._process_manager

    @property
    def io_handler(self):
        return self._io_handler

    def load_from_file(self, file: Path, _print = True):
        try:
            with open(file, 'r') as f:
                lines = f.readlines()
            # Close the file as soon as possible to free the disk
            # Also use an auxiliary list to get its len()
            pid = self._process_manager.create_process(file.name, lines)
            if _print: print(f'Loaded process {file.name} into memory. PID: {pid}')
            return pid
        except:
            return -1


    def run(self):
        """
        Thread loop
        """

        self._cpu.loop()

    def dump(self, e=None, to_file=True):
        """
        Dump the CPU and Memory information to a file or to the TK Text() module

        Args:
            e (Exception): An interruption (Exception) thrown by a CPU command
            to_file (bool): Flag specifying if the output should be saved to a file or not
        """

        if to_file:
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
                self.process_manager.dump(f)
                self.memory.dump(f)
