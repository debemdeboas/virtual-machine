# RISC-like Virtual Machine Emulator

A RISC-like (**R**educed **I**nstruction **S**et **C**omputer) emulator that runs a simple Assembly-like machine language.

Commit message emoji meanings can be found [here](https://gist.github.com/parmentf/035de27d6ed1dce0b36a).
This repository's URL can be found [here](https://github.com/debemdeboas/virtual-machine).

## Contributors

Rafael Almeida de Bem ([website](https://www.debem.dev)).

## Pipeline status

![PyTest](https://img.shields.io/github/workflow/status/debemdeboas/virtual-machine/Run%20PyTest)

## About

Implement a virtual machine that contains a CPU and Memory modules and runs a simplified version of the Assembly
programming language. University project.

This project was implemented with scalability and ease of use in mind. Adding and modifying commands is very easy and
requires very little knowledge of the system as a whole. Since mutable objects were used, some confusion might arise.
However, they were treated similarly to C++'s pointers, so programmers with low-level language knowledge should feel
right at home.

Since the sixth release of this system, the VM supports simple concurrent mechanisms such as blocking processes that are waiting for an IO operation using an IO handler thread.
On the seventh release of the system, a simple shell socket was added to concurrently load new processes into the memory or to shutdown the system.

### Solution

Most of the initial code was heavily inspired by the teacher's example, written in Java.
The command structure is the same, albeit with different parameters and language-specific improvements
(see [Command_SWAP](https://github.com/debemdeboas/virtual-machine/blob/dd735828e7c6e094c83b4d22d44e92d083c323b9/source/command/command.py#L572)).

----

## The code

The project has two threads: the Virtual Machine thread, and the "main" thread. This allows the program to have a responsive 
GUI without having to stop and wait for the GUI to update.

Every CPU cycle the GUI updates and sleeps for half a second. Without a Tk object on the VM, there is no `sleep()`.

### The VM

The VM contains both the CPU and the Memory instances. First, the CPU is instantiated. Secondly, the memory. Lastly,
the Tk object is checked and, if it is defined, some properties are set - such as disabling the capture of keystrokes,
and some tags for coloring the current command (light red), and the command that set an interruption (dark red).

Upon initialization, the memory is populated with 512 `Command_EMPTY` objects.

Afterwards, the `IVirtualMachine.load_from_file()` method is called, which reads a file from the disk and converts the
lines to Command objects.

With the loading of the program into the memory done, the CPU can execute its loop on the `IVirtualMachine.start()`
(which, in turn, will call `IVirtualMachine.run()`) method.

### Interruptions and Traps

~~Interruptions and traps are also implemented, both using Exceptions.~~

Interruptions and traps are implemented using a Queue that holds the Exception classes that correspond to each
interruption type. Custom exception classes were used in this case to emphasize that an interruption needs to be handled.
A command can set a trap by doing the following:

```python
# Types of each of the referenced arguments:
self: IBaseCommand = ...
self.interruption_queue: Queue = ...
self.func: Callable = ...

# Set a trap 
self.interruption_queue.put(ETrap(self.func))
```

When an error occurs, such as an `IndexError` on a memory access attempt, an interruption is set and executed after the
command has ended. The interruption classes are as follows:

| Exception             | Meaning |
|:---------------------:|----|
|`EInvalidCommand`      | An invalid command string has been inputted |
|`ETrap`                | A trap has been set by the user program |
|`EInvalidAddress`      | There was an attempt to access an illegal memory area |
|`EProgramEnd`          | A `STOP` command was issued |
|`EMathOverflowError`   | An overflow has occurred |
|`EShutdown`            | End the CPU loop, no more processes are available |
|`ESignalVirtualAlarm`  | SIGVTALRM clock interruption |
|`EIOOperationComplete` | An IO request has been fulfilled



## Usage

This project requires Python 3.8 or higher to run. Older versions **will not work** as expected and have not been tested.

First, install the required files:

```commandline
python3 -m pip install -r requirements.txt
```

Then, simply run the program. This will open a new Tkinter window with the current command being executed, as well
as the rest of the memory. When no argument is passed, a default example program is loaded and executed.

```commandline
python3 main.py
```

Alternatively, you can also pass a `.asm` program file to be executed by the VM:

```commandline
python3 main.py foo.asm
```

This will load the program `foo.asm` into the virtual memory and evaluate the program execution step by step.

~~If you do not wish to see the step-by-step evaluation of the program, open `main.py` and remove the `#` (comment) sign
from `text = None`. This will stop Tkinter from opening.~~ ~~The Tkinter interface will be removed in a future release.~~ The Tkinter interface has been removed.

### Shell

This VM interacts with a so-called DeBem Shell or DBSH, for short.

The shell (client) will try to connect to `localhost:8899` via binary socket to communicate with the VM (server), which has bound that address and port upon creation.

Running the shell is as simple as:

```commandline
python3 source/user/shell.py
```

After running the command and assuming the connection was successful, you will be greeted by a welcome dialog:

```
88888888ba,   88888888ba   ad88888ba  88        88
88      `"8b  88      "8b d8"     "8b 88        88
88        `8b 88      ,8P Y8,         88        88
88         88 88aaaaaa8P' `Y8aaaaa,   88aaaaaaaa88
88         88 88""""""8b,   `"""""8b, 88""""""""88
88         8P 88      `8b         `8b 88        88
88      .a8P  88      a8P Y8a     a8P 88        88
88888888Y"'   88888888P"   "Y88888P"  88        88



        Welcome to DBSH - DeBem Shell
        Type 'help' to get started
$
```

Then you can interact with the interface with the keyboard as you would a normal shell.
The DBSH is very bare-bones, and you can list all of the available commands by entering `help`.

If you type `help` followed by a command, the shell will print out that command's documentation.

#### Examples

To load a program into the memory, enter the following:

```commandline
$ load example_programs/p2.asm
```

The program will then be loaded onto the memory of the VM and will be added to the process queue.
The PID of the new process will also be printed to the screen.

Playing around in the shell is also encouraged.

## Tests

This repository contains extensive tests for the virtual machine system.
Most programs in the `example_programs/` folder have tests testing their functionality.

The tests file is called `asm_test.py` and is contained in the `tests/` folder.

To run all tests:

```commandline
python3 -m pytest
```

To run a specific test (from this repository's root directory):
```commandline
python3 -m pytest test/asm_test.py::AssemblyTest::{{ desired test name goes here }}
# For example, to run the P2 file test:
python3 -m pytest test/asm_test.py::AssemblyTest::test_p2 
```

The "desired test name" is the name of the function defined in the `asm_test.py` script.
