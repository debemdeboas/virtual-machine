from abc import ABC

from source.command.command import IBaseCommand


class IWord(ABC):
    command: IBaseCommand
    free: bool


class Word(IWord):
    def __init__(self, command: IBaseCommand = None, free: bool = True): ...
