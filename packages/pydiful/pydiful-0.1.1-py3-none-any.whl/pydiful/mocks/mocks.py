import abc
from typing import TypeVar


T = TypeVar("T")


class AbstractMockDatabase(abc.ABC):
    @abc.abstractmethod
    def fetch_string(self) -> str:
        pass

    @abc.abstractmethod
    def fetch_int(self) -> int:
        pass

    @abc.abstractmethod
    def delete_str(self) -> None:
        pass

    @abc.abstractmethod
    def delete_int(self) -> None:
        pass


class Database(AbstractMockDatabase):
    def delete_str(self) -> None:
        self.connection = "DELETED"

    def delete_int(self) -> None:
        self.number = 0

    def __init__(self):
        self.connection = "https://test-server:PORT"
        self.number = 100

    def fetch_int(self) -> int:
        return self.number

    def fetch_string(self):
        return f"Fetched data from {self.connection}"


class AbstractMockRepository[T](abc.ABC):
    @abc.abstractmethod
    def fetch(self) -> T:
        pass


class StringMockRepository(AbstractMockRepository[str]):
    def __init__(self, db: AbstractMockDatabase):
        self.db = db

    def fetch(self) -> str:
        return self.db.fetch_string()


class IntMockRepository(AbstractMockRepository[int]):
    def __init__(self, db: AbstractMockDatabase):
        self.db = db

    def fetch(self) -> int:
        return self.db.fetch_int()
