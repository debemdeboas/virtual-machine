# -----------------------------------------------------------------------------
# --------------------- Operating Systems Assignment #1 -----------------------
# ---- Author: Rafael Almeida de Bem                                       ----
# ---- Created on: 09/03/2021 (DD/MM/YYYY)                                 ----
# -----------------------------------------------------------------------------

from __future__ import annotations

import argparse
import pathlib

from glob import iglob
from source.vm.virtual_machine import VirtualMachine


def parse_args():
    parser = argparse.ArgumentParser(
        description='virtual machine emulator',
        epilog='star this on github: https://github.com/debemdeboas/virtual-machine'
    )
    parser.add_argument('programs', nargs='*', help='assembly files to be loaded and executed')

    return parser.parse_args()


def main():
    args = parse_args()

    if len(args.programs) > 0:
        files = args.programs
    else:
        files = iglob('example_programs/*.asm')

    vm = VirtualMachine(mem_size=4096, create_shell_sock=True)
    for file in files:
        vm.load_from_file(pathlib.Path(file))
    vm.start()
    vm.join()


if __name__ == '__main__':
    main()
