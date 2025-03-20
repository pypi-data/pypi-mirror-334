import abc
import enum
from typing import TypedDict

class ConcreteImplementation(TypedDict):
    class_: type
    singleton: bool
    lazy: bool

class GlobalRegistry(TypedDict):
    abstract: type[abc.ABC]
    concrete: ConcreteImplementation

class ServiceLifetime(enum.Enum):
    SINGLETON = 'singleton'
    SCOPED = 'scoped'
    TRANSIENT = 'transient'
