"""Decorator for tracking instances of a given object."""
from collections.abc import Callable
from typing import Type, TypeVar, Generic, Optional
from weakref import WeakSet, ref

T = TypeVar("T", bound=object)


def track(
        instance_limit: Optional[int] = None,
) -> Callable[[Type[T]], Type[T]]:
    def decorator(cls: Type[T]) -> Type[T]:
        cls.instances = WeakSet()

        def __new__(
                obj,
                *args,
                **kwargs,
        ) -> T:
            if instance_limit is not None and len(obj.instances) >= instance_limit:
                raise RuntimeError(
                    f"Cannot create more than {instance_limit} instances of {obj.__name__}."
                )
            else:
                instance = super(obj, obj).__new__(obj)
                obj.instances.add(instance)
                return instance

        cls.__new__ = classmethod(__new__)
        return cls

    return decorator
