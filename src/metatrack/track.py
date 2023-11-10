"""Decorator for tracking instances of a given object."""
from typing import Type, TypeVar, Generic, Optional
from weakref import WeakSet, ref

T = TypeVar("T", bound=object)



def track(instance_limit: Optional[int] = None, ) -> Type[T]:
    """Decorator for tracking instances of a given object."""

    class Meta(type):
        __instances__ = WeakSet()
    class Tracked(Generic[T], metaclass=Meta):
        instances: WeakSet[Type[T]] = Meta.__instances__
        __instance_limit: Optional[int] = instance_limit

        def __new__(cls: Type[T], *args, **kwargs) -> 'Tracked[T].instance':
            if Tracked.__instance_limit is not None and len(Tracked.instances) >= Tracked.__instance_limit:
                raise RuntimeError(
                    f"Cannot create more than {Tracked.__instance_limit} instances of {cls.__name__}."
                )
            else:
                instance = super().__new__(cls)
                Tracked.instances.add(instance)
                return instance

        def __call__(self, *args, **kwargs) -> 'Tracked[T].instance':
            return self

    return Tracked
