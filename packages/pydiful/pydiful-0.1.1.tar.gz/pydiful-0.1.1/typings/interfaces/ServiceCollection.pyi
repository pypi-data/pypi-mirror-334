from typing import Dict, Any, Type, Tuple

from pydiful.interfaces.ServiceProvider import ServiceProvider as ServiceProvider
from pydiful.utils import ServiceLifetime as ServiceLifetime

class ServiceCollection:
    _services: Dict[Type, Tuple[Type, ServiceLifetime, Any]]
    @classmethod
    def add(cls, lifetime: ServiceLifetime, abstract: type, concrete: type) -> None: ...
    @classmethod
    def build(cls) -> ServiceProvider: ...
