from typing import List


class Frame:
    addresses: List
    is_free: bool
    owner: int  # PID that owns this memory frame

    def __init__(self, addresses: List, index: int, owner: int = 0):
        # Reference to the memory addresses contained in this frame
        self.addresses = addresses
        self.is_free = True
        self.index = index
        self.owner = owner
