from abc import ABC
from typing import Any


class IWord(ABC):
    command: Any


class Word(IWord):
    def __init__(self, command=None):
        self.command = command

    def dump(self): return self.command.dump()

    @property
    def original(self): return self.command.original

    def set_instance_params(self, **kwargs): self.command.set_instance_params(**kwargs)

    def execute(self): return self.command.execute()
