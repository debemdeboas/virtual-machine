from abc import ABC, abstractmethod
from typing import Any

class IRegister(ABC):
    @property
    @abstractmethod
    def value(self) -> int: ...

    @value.setter
    @abstractmethod
    def value(self, val: Any): ...


class Register(IRegister):
    _value: int

    def __init__(self, value: int = ...): ...

    @property
    def value(self) -> int: ...

    @value.setter
    def value(self, val: Any): ...

    def __str__(self) -> str: ...
