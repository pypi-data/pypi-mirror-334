from typing import Type

import pytest

from pydiful import builder
from pydiful.interfaces.HostApplicationBuilder import \
    HostApplicationBuilder
from pydiful.interfaces.ServiceProvider import ServiceProvider
from pydiful.mocks.mocks import (
    Database,
    AbstractMockDatabase,
    AbstractMockRepository,
    IntMockRepository,
    StringMockRepository,
)


@pytest.fixture(scope="session")
def test_builder() -> Type[HostApplicationBuilder]:
    return builder

@pytest.fixture(scope="function")
def provider(test_builder):
    test_builder.build()
    return test_builder.service_provider


def test_builder_instanceof_host_application_builder(test_builder):
    assert test_builder is HostApplicationBuilder

def test_provider_instanceof_service_provider(provider):
    assert isinstance(provider, ServiceProvider)


def test_builder_adds_correct_service_impl(test_builder):
    test_builder.add_singleton(AbstractMockDatabase, Database)

    test_builder.build()

    provider = test_builder.service_provider

    assert isinstance(provider.get_required_service(AbstractMockDatabase), Database)

def test_provider_no_multiple_singleton_impls(provider):

    db1 = provider.get_required_service(AbstractMockDatabase)
    db2 = provider.get_required_service(AbstractMockDatabase)

    # equality implies both objects point
    # to same memory-address
    assert id(db1) == id(db2)

    db1.__setattr__("connection", "test")

    assert  db2.fetch_string() == 'Fetched data from test'


def test_builder_resolves_correct_type_varred_repo(test_builder):
    test_builder.add_scoped(AbstractMockRepository[int], IntMockRepository)
    test_builder.add_scoped(AbstractMockRepository[str], StringMockRepository)
    test_builder.build()
    provider = test_builder.service_provider

    int_repo: Type[AbstractMockRepository[int]] = provider.get_required_service(
            AbstractMockRepository[int])
    str_repo: Type[AbstractMockRepository[str]] = (
            provider.get_required_service(
            AbstractMockRepository[str]))

    fetched_str = str_repo.fetch()
    fetched_int = int_repo.fetch()

    assert type(fetched_int) == int
    assert fetched_int == 100
    assert type(fetched_str) == str



