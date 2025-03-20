
from pydiful import builder
from pydiful.interfaces.HostApplicationBuilder import inject
from pydiful.mocks import AbstractMockDatabase, AbstractMockRepository
from pydiful.mocks.mocks import Database, StringMockRepository, \
    IntMockRepository


@inject
class TestDependee:
    def __init__(self, mock_db: AbstractMockDatabase) -> None:
        self._mock_db = mock_db

    def fetch_from_db(self) -> str:
        db_connection: str = self._mock_db.fetch_string()
        return db_connection


def test_prepare():
    builder.add_singleton(AbstractMockDatabase, Database)
    builder.add_scoped(AbstractMockRepository[str],StringMockRepository )
    builder.add_scoped(AbstractMockRepository[int], IntMockRepository)
    builder.build()
    test_dependee = TestDependee()
    mock_db = builder.service_provider.get_required_service(
            AbstractMockDatabase
    )
    assert test_dependee.fetch_from_db() == mock_db.fetch_string()
