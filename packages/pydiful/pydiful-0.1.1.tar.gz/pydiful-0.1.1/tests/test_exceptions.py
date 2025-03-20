import pytest

from pydiful import builder
from pydiful.exceptions import InterfaceNotRegistered
from pydiful.mocks import AbstractMockDatabase


def test_incompatible_raises_error():
    builder.build()
    with pytest.raises(InterfaceNotRegistered):
        builder.service_provider.get_required_service(AbstractMockDatabase)