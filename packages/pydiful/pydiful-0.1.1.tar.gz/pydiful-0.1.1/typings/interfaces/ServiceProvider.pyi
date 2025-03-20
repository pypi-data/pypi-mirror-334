from typing import Any, TypeVar, Dict, Type, Tuple, List

from pydiful.utils import ServiceLifetime as ServiceLifetime

T = TypeVar("T")
U = TypeVar("U")

class ServiceProvider:
    _service_names: List[str]
    _services: Dict[Type, Tuple[Type, ServiceLifetime, Any]]
    _scoped_services: Dict[Type, Any]

    def __init__(
        self, services: Dict[Type, Tuple[Type, ServiceLifetime, Any]]
    ) -> None: ...
    def get_required_service(self, abstract: Type[T]) -> T: ...
    def _instantiate(self, concrete: Type) -> Type: ...
