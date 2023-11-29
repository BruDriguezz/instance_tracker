"""Decorator for tracking, controlling, and logging instances of classes."""
from __future__ import annotations
from typing import TypeVar, Callable, Any, Type, Annotated
from weakref import WeakSet, ref
from types import FunctionType
from warnings import warn

__all__ = ["track"]
T = TypeVar("T", bound=(Callable[..., object] | Type[Any]))


def track(
        _o: Type[T] = None,
        /,
        **flags: Annotated[dict[Any, ...], "Flags for the decorator."],
) -> Callable[[T], T] | T:
    """Decorator for tracking, controlling, and logging instances of classes.

    :param _o: The object to decorate, if no flags are to be passed.
    :parameter flags: Flags for the decorator.
    :type flags: dict[Any, ...]

    :return: The decorated object.
    :rtype: Callable[[T], T] | T
    """

    def decorator(obj: T) -> T:
        if flags:
            for k, v in flags.items():
                if k in [
                    "instance_limit",
                ]:  # I have to decide what flags I want to use, and what they do.
                    obj.flags.update({k: v})

        if isinstance(obj, type):
            obj.instance_limit = flags.get("instance_limit", None)
            obj.instances = WeakSet()

            def __new__(
                    cls: Type[T],
                    *args: Any,
                    **kwargs: Any,
            ) -> T:
                if (
                        obj.instance_limit is not None
                        and len(obj.instances) >= obj.instance_limit
                ):
                    raise RuntimeError(
                        f"Can't create more than {obj.instance_limit} instances of {obj.__name__!r}"
                    )

                instance = super(cls, obj).__new__(cls)
                obj.instances.add(item=instance)
                return instance

            obj.__new__ = __new__

        if isinstance(obj, FunctionType):
            warn(
                message="Tracking functions is not yet supported, returning object as is.",
            )

        return obj

    if _o:
        return decorator(obj=_o)

    return decorator


__version__ = "1.1.0"
