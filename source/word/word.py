from abc import ABC
from typing import Any


class IWord(ABC):
    command: Any
    free: bool


class Word(IWord):
    def __init__(self, command=None, free=True):
        self.command = command
        self.free = free
