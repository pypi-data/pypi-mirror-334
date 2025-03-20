from typing import Dict, Type, Tuple, Any

from pydiful.interfaces.ServiceProvider import ServiceProvider
from pydiful.utils import ServiceLifetime


class ServiceCollection:
    """Registers service_collection according to their lifetimes."""

    _services: Dict[Type, Tuple[Type, ServiceLifetime, Any]] = {}

    @classmethod
    def add(cls, lifetime: ServiceLifetime, abstract: Type, concrete: Type) -> None:
        #        if not issubclass(concrete,abstract):
        #            raise IncompatibleImplementation(abstract,concrete)
        cls._services[abstract] = (concrete, lifetime, None)

    @classmethod
    def build(cls) -> ServiceProvider:
        return ServiceProvider(cls._services)

    @classmethod
    def has_service(cls, abstract: Type) -> bool:
        return abstract in cls._services