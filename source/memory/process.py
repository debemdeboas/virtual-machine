from typing import List
from enum import Enum

ProcessState = Enum('ProcessState', 'READY RUNNING BLOCKED ENDED')

class Process:
    def __init__(self, name, _id):
        self.name = name
        self.pid = _id
        self.state: ProcessState = ProcessState.READY


class ProcessControlBlock(Process):
    def __init__(self, process_name, process_id, frames, size):
        super().__init__(process_name, process_id)
        self.current_frame = 0  # Goes from 0 to `process_frames`
        self.current_offset = 0  # Goes from 0 to `page_size`
        self.process_size = size  # For debugging
        self.frames = frames

        self.saved_pc_value = 0
        self.saved_register_values = {}

    def suspend(self, pc, registers, should_increment_pc, blocked = False):
        if should_increment_pc:
            self.saved_pc_value = pc.value + 1
        else:
            self.saved_pc_value = pc.value
        for register in registers.items():
            self.saved_register_values[register[0]] = register[1].value

        if blocked:
            self.state = ProcessState.BLOCKED
        else:
            self.state = ProcessState.READY

    def resume(self, pc, registers):
        pc.value = self.saved_pc_value
        for register in registers.values():
            register.value = 0
        for register in self.saved_register_values.items():
            registers[register[0]].value = register[1]
        self.state = ProcessState.RUNNING

    def dump(self) -> List[str]:
        return [
            f'|\tNAME: {self.name:<69}|\n',
            f'|\tPID: {self.pid:<70}|\n',
            f'|\tSIZE: {self.process_size:<69}|\n',
            f'|\tNUM. FRAMES: {len(self.frames):<62}|\n',
            f'|\tCURRENT_FRAME: {self.current_frame:<60}|\n',
            f'|\tCURRENT_OFFSET: {self.current_offset:<59}|\n',
        ]
