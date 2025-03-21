from expat.config import DBConfig

from abc import ABC, abstractmethod
from types import TracebackType
from typing import Self, Type


class Driver(ABC):
    config: DBConfig

    def __init__(self, config: DBConfig):
        self.config = config

    @abstractmethod
    def __enter__(self) -> Self: ...

    @abstractmethod
    def __exit__(
        self,
        exception_type: Type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ): ...

    @abstractmethod
    def create_expat_tables(self): ...

    @abstractmethod
    def destroy_expat_tables(self): ...
