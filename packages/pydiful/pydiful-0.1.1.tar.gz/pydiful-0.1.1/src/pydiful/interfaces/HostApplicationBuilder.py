import inspect
from typing import Type, get_type_hints

from devtools import debug  # type: ignore

from pydiful.interfaces.ServiceCollection import ServiceCollection
from pydiful.interfaces.ServiceProvider import ServiceProvider
from pydiful.utils import ServiceLifetime


class HostApplicationBuilder:
    """Wires dependencies and builds the DI container."""

    debug("HostApplicationBuilder class body entered")
    service_collection: ServiceCollection = ServiceCollection()
    service_provider: ServiceProvider

    def __init__(self):
        # self.service_collection = ServiceCollection()
        pass

    @classmethod
    def add_singleton(cls, abstract: Type, concrete: Type) -> None:
        debug(
            f"Collecting Singleton: {abstract.__class__}"
            f" {abstract.__class__.__annotations__}"
        )
        cls.service_collection.add(ServiceLifetime.SINGLETON, abstract, concrete)

    @classmethod
    def add_scoped(cls, abstract: Type, concrete: Type) -> None:
        cls.service_collection.add(ServiceLifetime.SCOPED, abstract, concrete)

    @classmethod
    def add_transient(cls, abstract: Type, concrete: Type) -> None:
        """
        Transient dependencies will be instantiated every time a
        dependee is called. A typical use-case is a service instance
        which extends functionality of an HTTP-Request object.

        Consider declaring the dependency as transient if:
            - The instance has little to no state
            - Multiple instances should run indepedently from each other (think multi-threading)


        :param abstract: The interface to be implemented by the
            lower-level module. Classes in the higher-level module
            should depend on this abstraction instead of the concrete implementation.
        :param concrete:
        :return:
        """
        cls.service_collection.add(ServiceLifetime.TRANSIENT, abstract, concrete)

    @classmethod
    def build(cls) -> None:
        cls.service_provider = cls.service_collection.build()


def inject(cls):
    """
    Class decorator that automatically injects constructor
    dependencies from the global DI container.
    :param cls:
    :return:
    """

    orig_init = cls.__init__

    def wrapped_init(self, *args, **kwargs):
        signature = inspect.signature(orig_init)
        type_hints = get_type_hints(orig_init)

        for param_name, param in signature.parameters.items():
            if param_name == "self":
                continue
            if param_name not in kwargs:
                abstract_type = type_hints.get(param_name)
                if ServiceCollection.has_service(abstract_type):
                    kwargs[param_name] = (
                        HostApplicationBuilder
                            .service_provider.get_required_service(
                            abstract_type
                        )
                    )

        orig_init(self, *args, **kwargs)

    cls.__init__ = wrapped_init

    return cls

