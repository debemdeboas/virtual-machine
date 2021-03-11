from abc import ABC, abstractmethod


class IRegister(ABC):
    @abstractmethod
    def __init__(self) -> None: ...

    @property
    @abstractmethod
    def value(self) -> int: ...


class Register(IRegister):
    # noinspection PyMissingConstructor
    def __init__(self, value: int = -1):
        self._value: int = value

    @property
    def value(self) -> int: return self._value
