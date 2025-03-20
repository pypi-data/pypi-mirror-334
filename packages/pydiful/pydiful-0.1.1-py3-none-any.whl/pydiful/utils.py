import abc
import enum
from typing import Type, TypedDict


class ConcreteImplementation(TypedDict):
    class_: Type
    singleton: bool
    lazy: bool


class GlobalRegistry(TypedDict):
    abstract: Type[abc.ABC]
    concrete: ConcreteImplementation


class ServiceLifetime(enum.Enum):
    SINGLETON = "singleton"
    SCOPED = "scoped"
    TRANSIENT = "transient"
