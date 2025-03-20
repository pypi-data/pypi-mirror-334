import pytest

from pydiful.interfaces.HostApplicationBuilder import \
    HostApplicationBuilder
from pydiful.mocks.mocks import (
    AbstractMockDatabase,
    Database,
    AbstractMockRepository,
    IntMockRepository,
    StringMockRepository,
)


@pytest.fixture(scope="module")
def service_collection():
    builder = HostApplicationBuilder()
    builder.add_singleton(AbstractMockDatabase,Database)
    builder.add_scoped(AbstractMockRepository[int], IntMockRepository)
    builder.add_transient(AbstractMockRepository[str], StringMockRepository)
    return builder.service_collection

def test_service_collection(service_collection):
    assert service_collection