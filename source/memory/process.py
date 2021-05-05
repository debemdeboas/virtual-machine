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

    def suspend(self):
        self.running = False
        self.ready = False  # Only set ready to True on the end of this method
        pass

    def resume(self):
        self.running = True
        self.ready = True
        pass

    def dump(self) -> List[str]:
        return [
            f'|\tNAME: {self.name:<69}|\n',
            f'|\tPID: {self.pid:<70}|\n',
            f'|\tSIZE: {self.process_size:<69}|\n',
            f'|\tNUM. FRAMES: {len(self.frames):<62}|\n',
            f'|\tCURRENT_FRAME: {self.current_frame:<60}|\n',
            f'|\tCURRENT_OFFSET: {self.current_offset:<59}|\n',
        ]
