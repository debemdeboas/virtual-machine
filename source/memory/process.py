from typing import List


class Process:
    def __init__(self, name, _id):
        self.name = name
        self.pid = _id
        self.ready = False
        self.running = False


class ProcessControlBlock(Process):
    def __init__(self, process_name, process_id, frames, size):
        super().__init__(process_name, process_id)
        self.current_frame = 0  # Goes from 0 to `process_frames`
        self.current_offset = 0  # Goes from 0 to `page_size`
        self.process_size = size  # For debugging
        self.frames = frames

        self.saved_pc_value = 0
        self.saved_register_values = {}

    def suspend(self, pc, registers, should_increment_pc):
        self.running = False
        self.ready = False  # Only set ready to True on the end of this method
        if should_increment_pc:
            self.saved_pc_value = pc.value + 1
        else:
            self.saved_pc_value = pc.value
        for register in registers.items():
            self.saved_register_values[register[0]] = register[1].value
        self.ready = True

    def resume(self, pc, registers):
        pc.value = self.saved_pc_value
        for register in registers.values():
            register.value = 0
        for register in self.saved_register_values.items():
            registers[register[0]].value = register[1]
        self.running = True
        self.ready = True

    def dump(self) -> List[str]:
        return [
            f'|\tNAME: {self.name:<69}|\n',
            f'|\tPID: {self.pid:<70}|\n',
            f'|\tSIZE: {self.process_size:<69}|\n',
            f'|\tNUM. FRAMES: {len(self.frames):<62}|\n',
            f'|\tCURRENT_FRAME: {self.current_frame:<60}|\n',
            f'|\tCURRENT_OFFSET: {self.current_offset:<59}|\n',
        ]
