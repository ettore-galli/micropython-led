from abc import ABC, abstractmethod


class ButtonStatus:
    PRESSED: int = 1
    RELEASED: int = 0


class PwmStatus:
    ON: int = 1
    OFF: int = 0


class LedStatus:
    ON: int = 1
    OFF: int = 0


class BaseTimer(ABC):
    @abstractmethod
    def sleep(self, seconds: float) -> None: ...

    @abstractmethod
    def ticks_diff(self, ticks1: int, ticks2: int) -> int: ...

    @abstractmethod
    def ticks_us(self) -> int: ...
class BaseButton(ABC):
    @abstractmethod
    def __init__(self, pin_number: int) -> None: ...

    @abstractmethod
    def value(self) -> int: ...


class BaseLed(ABC):
    @abstractmethod
    def __init__(self, pin_number: int) -> None: ...

    @abstractmethod
    def on(self) -> None: ...

    @abstractmethod
    def off(self) -> None: ...

    @abstractmethod
    def start_pwm(self, frequency: float) -> None: ...

    @abstractmethod
    def stop_pwm(self) -> None: ...
