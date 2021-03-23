# RISC-like Virtual Machine Emulator

A RISC-like (**R**educed **I**nstruction **S**et **C**omputer) emulator that runs a simple Assembly-like machine language.

Commit message emoji meanings can be found [here](https://gist.github.com/parmentf/035de27d6ed1dce0b36a).

## Pipeline status

Tests: ![PyTest](https://img.shields.io/github/workflow/status/debemdeboas/virtual-machine/Run%20PyTest)

## About

Implement a virtual machine that contains a CPU and Memory modules and runs a simplified version of the Assembly
programming language. University project.

This project was implemented with scalability and ease of use in mind. Adding and modifying commands is very easy and
requires very little knowledge of the system as a whole. Since mutable objects were used, some confusion might arise.
However, they were treated similarly to C++'s pointers, so programmers with low-level language knowledge should feel
right at home.

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
|`ETrap`                | A trap has been set by the user program |
|`EInvalidCommand`      | An invalid command string has been inputted |
|`EInvalidAddress`      | There was an attempt to access an illegal memory area |
|`EProgramEnd`          | A `STOP` command was issued |
|`EMathOverflowError`   | An overflow has occurred |


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

If you do not wish to see the step-by-step evaluation of the program, open `main.py` and remove the `#` (comment) sign
from `text = None`. This will stop Tkinter from opening.
