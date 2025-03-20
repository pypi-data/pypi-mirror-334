from abc import ABCMeta, abstractmethod


class DictMixin(metaclass=ABCMeta):
    """
    A mixin class that defines an interface for objects that can be
    converted to a dictionary.

    This class serves as an abstract base class (ABC), requiring subclasses
    to implement the `to_dict` method.

    Methods
    -------
    to_dict()
        Abstract method that must be implemented by subclasses.
        Converts the object into a dictionary.
    """
    @abstractmethod
    def to_dict(self) -> dict:
        pass
