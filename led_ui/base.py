from abc import ABC, abstractmethod


class BaseTimer(ABC):
    @abstractmethod
    def sleep(self, seconds: float) -> None: ...


class BaseButton(ABC):
    @abstractmethod
    def __init__(self, pin_number: int) -> None: ...


class BaseLed(ABC):
    @abstractmethod
    def __init__(self, pin_number: int) -> None: ...

    @abstractmethod
    def on(self) -> None: ...

    @abstractmethod
    def off(self) -> None: ...
