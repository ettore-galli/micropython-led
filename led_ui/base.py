from abc import ABC, abstractmethod


class BaseButton(ABC):
    @abstractmethod
    def __init__(self, pin_number: int) -> None: ...


class BaseLed(ABC):
    @abstractmethod
    def __init__(self, pin_number: int) -> None: ...
