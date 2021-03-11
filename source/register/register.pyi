from abc import ABC, abstractmethod


class IRegister(ABC):
    @abstractmethod
    def __init__(self) -> None: ...

    @property
    @abstractmethod
    def value(self) -> int: ...


class Register(IRegister):
    _value: int

    def __init__(self, value: int = ...): ...

    @property
    def value(self) -> int: ...
