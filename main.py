# -----------------------------------------------------------------------------
# --------------------- Operating Systems Assignment #1 -----------------------
# ---- Author: Rafael Almeida de Bem
# ---- Created on: 09/03/2021 (DD/MM/YYYY)
# ---- Modified on: 13/03/2021
# -----------------------------------------------------------------------------

from __future__ import annotations

import pathlib
import tkinter as tk

from virtual_machine import VirtualMachine

root = tk.Tk()
root.resizable(False, False)
text = tk.Text(root, width=120, height=80)
# text = None

vm = VirtualMachine(mem_size=512, tk=text)
vm.load_from_file(pathlib.Path('example_programs/p3.asm'))
vm.start()

if text:
    root.mainloop()
vm.join()
