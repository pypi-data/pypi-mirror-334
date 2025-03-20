import inspect
import warnings
from typing import Dict, Type, Tuple, Any, TypeVar


from pydiful.exceptions.exceptions import InterfaceNotRegistered
from pydiful.utils import ServiceLifetime


T = TypeVar("T")
U = TypeVar("U")


class ServiceProvider:
    def __init__(self, services: Dict[Type, Tuple[Type, ServiceLifetime, Any]]) -> None:
        self._services = services
        self._scoped_services: Dict[Type, Any] = {}
        self._service_names = [abstract.__name__ for abstract in services]

    def _instantiate(self, concrete: Type) -> Type:
        constructor_params = inspect.signature(concrete.__init__).parameters

        args = {
            name: self.get_required_service(param.annotation)
            for name, param in constructor_params.items()
            if param.annotation in self._services
        }
        return concrete(**args)

    def get_required_service(self, abstract: Type[T] | Type) -> (
            Type[T]|Type):
        abstract_name: str = abstract.__name__
        #debug(abstract_name)
        if abstract_name not in self._service_names:
            raise InterfaceNotRegistered(abstract)
        concrete_name, lifetime, instance = self._services[abstract]

        match lifetime:
            case ServiceLifetime.SINGLETON:
                if instance is None:
                    instance = self._instantiate(concrete_name)
                    self._services[abstract] = (concrete_name, lifetime, instance)
                return instance
            case ServiceLifetime.SCOPED:
                if abstract not in self._scoped_services:
                    self._scoped_services[abstract] = self._instantiate(concrete_name)
                return self._scoped_services[abstract]
            case ServiceLifetime.TRANSIENT:
                return self._instantiate(concrete_name)
            case _:
                warnings.warn(
                    f"Service Lifetime for registered "
                    f"service {concrete_name.__name__} not "
                    "recognized. Make sure you set a valid "
                    "value for the lifetime parameter."
                    "Falling back to transient."
                )
                return self._instantiate(concrete_name)
