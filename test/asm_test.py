import unittest
from pathlib import Path

import mock
from fibonacci import fibonacci
from parameterized import parameterized

from source.vm.virtual_machine import VirtualMachine


class AssemblyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.vm = VirtualMachine(mem_size=4096)

    def test_fibonacci(self):
        """
        Test the Fibonacci sequence generator assembly file
        """

        self.vm.load_from_file(Path('example_programs/fibonacci.asm'))
        self.vm.start()
        self.vm.join()

        # Test Fibonacci sequence
        for address, result in [(50, 0), (51, 1), (58, 21), (59, 34)]:
            with self.subTest(address=address, result=result):
                self.assertEqual(self.vm.memory.access(address).command.execute(), result)

    def test_p2(self):
        """
        Test the P2 assembly file, which should write `n` Fibonacci values
        """

        self.vm.load_from_file(Path('example_programs/p2.asm'))
        self.vm.start()
        self.vm.join()

        amount = self.vm.memory._inner_memory[17].command.p
        start_address = self.vm.memory._inner_memory[18].command.p

        for address, result in [(start_address, amount),
                                *zip([x + start_address + 1 for x in range(amount)], fibonacci(length=amount))]:
            with self.subTest(address=address, result=result):
                self.assertEqual(self.vm.memory.access(address).command.execute(), result)

    @parameterized.expand([
        (3,), (5,), (20,)
    ])
    def test_p2_traps(self, amount):
        """
        Test P2 ASM file with interruptions (traps)

        Mock user input with the `mock` module and use `amount` parameter as fibonacci length
        """

        self.vm.load_from_file(Path('example_programs/p2_traps.asm'))

        fib_amount = amount

        with mock.patch('builtins.input', return_value=fib_amount):
            self.vm.start()
            self.vm.join()

        start_address = self.vm.memory._inner_memory[18].command.p

        for address, result in [(start_address, fib_amount),
                                *zip([x + start_address + 1 for x in range(fib_amount)], fibonacci(length=fib_amount))]:
            with self.subTest(address=address, result=result):
                self.assertEqual(self.vm.memory.access(address).command.execute(), result)

    def test_p3(self):
        """
        Test P3 ASM file

        Calculate the factorial of a number
        """

        import math

        self.vm.load_from_file(Path('example_programs/p3.asm'))

        self.vm.start()
        self.vm.join()

        number = self.vm.memory._inner_memory[19].command.p

        if number < 0:
            factorial = -1
        else:
            factorial = math.factorial(number)

        self.assertEqual(self.vm.memory.access(50).command.execute(), factorial)

    @parameterized.expand([
        (5,), (6,), (-2,), (0,)
    ])
    def test_p3_traps(self, number):
        """
        Test P3 ASM file with traps

        Calculate the factorial of a number read from the keyboard (input mocked)
        """

        import math

        self.vm.load_from_file(Path('example_programs/p3_traps.asm'))

        with mock.patch('builtins.input', return_value=number):
            self.vm.start()
            self.vm.join()

        if number < 0:
            factorial = -1
        else:
            factorial = math.factorial(number)

        self.assertEqual(self.vm.memory.access(50).command.execute(), factorial)

    def test_p4(self):
        """
        Test P4 ASM file

        Bubble sorts an array
        """

        literal_array = [73, 29, 8, 82, 199, 62, 164, 182, 29, 197, 38, 2, 186, 192, 35, 18, 122, 138, 181, 195, 86,
                         174, 75, 135, 7, 12, 33, 67, 62, 133, 55, 104, 78, 84, 91, 121, 73, 178, 117, 109, 4, 163, 11,
                         182, 54, 77, 107, 197, 81, 100]
        literal_array.sort()

        self.vm.load_from_file(Path('example_programs/p4.asm'))

        self.vm.start()
        self.vm.join()

        self.assertEqual(literal_array, [self.vm.memory.access(i).command.execute() for i in range(300, 350)])


if __name__ == '__main__':
    unittest.main()
