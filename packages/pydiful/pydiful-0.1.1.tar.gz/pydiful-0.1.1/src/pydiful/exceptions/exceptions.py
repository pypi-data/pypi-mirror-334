from typing import Type


class IncompatibleImplementation(TypeError):
    def __init__(self, abstract: Type, concrete: Type):
        super().__init__(
            f"The registered Service {concrete.__name__} "
            f"does not implement "
            f"the abstract class {abstract.__name__}."
            f"Currently, "
            f"only nominal subtyping is supported."
        )


class InterfaceNotRegistered(KeyError):
    def __init__(self, abstract: Type):
        super().__init__(
            f"The abstract class {abstract.__name__} "
            f"has not been registered. Did you register "
            f"it in the ServiceCollection?"
        )


class ImplementationNotFound(KeyError):
    def __init__(self, concrete_name: str):
        super().__init__(
            f"The implementation {concrete_name} "
            f"has not been found in global namespace."
        )
