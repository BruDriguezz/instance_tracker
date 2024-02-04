from typing import Generic, Optional, TypeVar, Any, Generator, Type, Self
from weakref import WeakSet, ref
from threading import Lock
from inspect import signature

from .thread_manager import ThreadControl
from .interface import ITrackable
from .utils.settings import Settings
from .utils.types import ObjectSet
T = TypeVar("T")


class TrackedObject(Generic[T]):
    """Base class for tracked objects.

    This class represents a base class for objects that can be tracked. It provides
    functionality to store instances of the tracked object and retrieve them.

    Attributes:
        signature (inspect.Signature): The signature of the tracked object's __init__ method.
        name (str): The qualified name of the tracked object's class.
        id (int): The unique identifier of the tracked object.
        instances (weakref.WeakSet): The set of instances of the tracked object.

    Methods:
        add(instance: T) -> None: Adds an instance to the set of instances.
    """

    def __init__(
        self,
        _cls: Type[T],
        /,
        **params,
    ) -> None:
        self.signature, self.name = (signature(_cls.__init__), _cls.__qualname__)
        self.id = hash(self.name + str(self.signature))
        self._instances: WeakSet[T] = WeakSet()


    @property
    def instances(self) -> Generator[T, None, None]:
        """Returns a generator of instances."""
        yield from self._instances

    @instances.setter
    def instances(self, value: Optional[WeakSet[T]]) -> None:
        """Sets the set of instances."""
        self._instances = value


    def add(
        self,
        instance: T,
    ) -> None:
        """Adds an instance to the set of instances."""
        self._instances.add(instance)



class TrackedObjectSet(ITrackable):
    """Too lazy for docstring. Will do later."""
    sets: ObjectSet[Type[T], Self] = ObjectSet()
    sets_lock: Lock = Lock()

    def __init__(
        self,
        obj: TrackedObject[T],
        /,
        **params,
    ) -> None:
        self.settings = Settings(**params)
        self.tc = ThreadControl()
        self.obj = obj

    @classmethod
    def get(
        cls,
        _cls: Type[T],
        /,
        **params,
    ) -> Self:
        with cls.sets_lock:
            obj_identifier = hash(_cls.__qualname__ + str(signature(_cls.__init__)))
            if obj_identifier not in cls.sets:
                cls.sets[obj_identifier] = cls(
                    TrackedObject(_cls), **params
                )
            return cls.sets[obj_identifier]
