from pyfiglet import figlet_format
from typing import Callable, Dict
import socket


class CommandHandler:
    def __init__(self, sock) -> None:
        self.sock = sock

        self._funcs: Dict[str, Callable] = {
            'help': self.help,
            'shutdown': self.shutdown,
            'load': self.load_program,
            'echo': self.echo,
            'exit': lambda _: exit(0),
        }

    def echo(self, *args):
        """
        Echo? Echo

        Prints the passed parameter to the console.
        """

        msg: str = args[0][0][0]
        print(msg)
        if msg.lower().strip() == 'hello there':
            print('[General Grievous]: General Kenobi!')

    def help(self, *args):
        """
        Get help

        If no arguments are given, list all commands.
        If an argument is given, get that command's documentation.
        """

        try:
            if args[0][0] != ['']:
                if func := self._funcs.get(args[0][0][0]):
                    print(func.__doc__.replace('            ', ''))
                else:
                    print('Unknown command')
            else:
                print('Available commands:')
                [print(f'\t{name}') for name in self._funcs]
        except:
            print('Error! Could not get help for the requested command')

    def shutdown(self, *args):
        """
        Halts the VM

        Stops everything and exits the program.
        """

        self.send("shutdown")

    def load_program(self, *args):
        """
        Loads a program into the VM's memory

        Args:
            path (str): the program file path
        """

        file: str = args[0][0][0]

        if not file or file.endswith('/') or file.endswith('\\') or \
            not file.endswith('.asm'):
            print('Invalid file')
            return

        self.send(f'load {file}')

    def handle(self, command: str, *args):
        """
        Handles a shell command

        Args:
            command (str): user input
        """

        try:
            self._funcs[command](args)
        except KeyError:
            print('Error! Invalid command')
        except Exception as E:
            print(f'An error has occurred. {E}')

    def send(self, *args):
        encoded_msg = args[0].encode('ascii')
        self.sock.sendall(encoded_msg)
        print(self.sock.recv(4096).decode('ascii'))


if __name__ == '__main__':
    print(figlet_format('DBSH', font='univers'))

    try:
        sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        sock.connect(('localhost', 8899))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

        handler = CommandHandler(sock)
        print('\tWelcome to DBSH - DeBem Shell\n\tType \'help\' to get started')
        try:
            while True:
                command, _, *args = input("$ ").partition(' ')

                if not command:
                    continue

                handler.handle(command, args)
        except KeyboardInterrupt:
            handler.handle('exit')
    except ConnectionRefusedError:
        print('Could not connect to the server')
