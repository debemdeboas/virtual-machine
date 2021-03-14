# -----------------------------------------------------------------------------
# --------------------- Operating Systems Assignment #1 -----------------------
# ---- Author: Rafael Almeida de Bem
# ---- Created on: 09/03/2021 (DD/MM/YYYY)
# ---- Modified on: 13/03/2021
# ----              14/03/2021
# -----------------------------------------------------------------------------

from __future__ import annotations

import pathlib
import sys
import tkinter as tk

from source.vm.virtual_machine import VirtualMachine

try:
    file = sys.argv[1]
except:
    file = 'example_programs/p2.asm'

root = tk.Tk()
root.protocol('WM_DELETE_WINDOW', lambda: (root.quit(), root.destroy()))
root.resizable(False, False)
text = tk.Text(root, width=120, height=80)
# text = None

vm = VirtualMachine(mem_size=512, tk=text)
vm.load_from_file(pathlib.Path(file))
vm.start()

if text:
    root.mainloop()
vm.join()
