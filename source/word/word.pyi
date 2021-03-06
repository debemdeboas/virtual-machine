from abc import ABC

from source.command.command import IBaseCommand


class IWord(ABC):
    command: IBaseCommand

    def dump(self): ...

    @property
    def original(self): ...

    def set_instance_params(self, **kwargs): ...

    def execute(self): ...

class Word(IWord):
    def __init__(self, command: IBaseCommand = None): ...

    def dump(self): ...

    @property
    def original(self): ...

    def set_instance_params(self, **kwargs): ...

    def execute(self): ...