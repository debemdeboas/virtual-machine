# -----------------------------------------------------------------------------
# --------------------- Operating Systems Assignment #1 -----------------------
# ---- Author: Rafael Almeida de Bem                                       ----
# ---- Created on: 09/03/2021 (DD/MM/YYYY)                                 ----
# -----------------------------------------------------------------------------

from __future__ import annotations

import argparse
import pathlib
import tkinter as tk

from source.vm.virtual_machine import VirtualMachine


def parse_args():
    parser = argparse.ArgumentParser(
        description='virtual machine emulator',
        epilog='star this on github: https://github.com/debemdeboas/virtual-machine'
    )
    parser.add_argument('programs', nargs='*', help='assembly files to be loaded and executed')
    parser.add_argument('--tk', help='show the Tkinter memory interface', action='store_true')

    return parser.parse_args()


def main():
    args = parse_args()

    if args.tk:
        root = tk.Tk()
        root.protocol('WM_DELETE_WINDOW', lambda: (root.quit(), root.destroy(), vm.join(timeout=0.1)))
        root.resizable(False, False)
        text = tk.Text(root, width=120, height=80)
    else:
        text = None

    if len(args.programs) > 0:
        files = args.programs
    else:
        files = ['example_programs/p2.asm']

    vm = VirtualMachine(mem_size=2048, tk=text)
    for file in files:
        vm.load_from_file(pathlib.Path(file))
    vm.start()

    if text:
        root.mainloop()
    vm.join(timeout=10)


if __name__ == '__main__':
    main()