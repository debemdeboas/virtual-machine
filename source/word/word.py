from abc import ABC
from typing import Any

from source.command.command import BaseCommand

class IWord(ABC):
    command: Any


class Word(IWord, BaseCommand):
    def __init__(self, command=None):
        self.command = command
