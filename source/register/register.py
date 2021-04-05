from abc import ABC, abstractmethod


class IRegister(ABC):
    @property
    @abstractmethod
    def value(self) -> int: ...

    @value.setter
    @abstractmethod
    def value(self, val: int): ...


class Register(IRegister):
    def __init__(self, value=0):
        self._value = value

    @property
    def value(self): return self._value

    @value.setter
    def value(self, val): self._value = int(val)

    def __str__(self): return str(self.value)
