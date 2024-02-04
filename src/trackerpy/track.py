from typing import Any, Callable, Type, Optional, Iterator
from logic import ITrackable, T, TrackedObjectSet, TrackedObject


def track(_cls: Type[T], **args) -> Type[T]:
    orig_new = _cls.__new__

    def decorator(_o: Type[T]) -> Type[T]:
        def wrapper(cls, *w_args, **w_kwargs):
            instance = orig_new(cls)
            tos = TrackedObjectSet.get(_o, **args)
            with TrackedObjectSet.sets_lock:
                tos.obj.add(instance)
            return instance

        def instances(self=None):
            tos = TrackedObjectSet.get(_o, **args)
            return iter(tos.obj._instances)

        _o.__new__ = wrapper
        _o.instances = instances
        return _o

    return decorator(_cls)
@track
class TrackedClass:
    def __init__(self, name):
        self.name = name

@track
class TrackedClass2:
    def __init__(self, name):
        self.name = name

# Create instances of TrackedClass
instance1 = TrackedClass("instance1")

instance2 = TrackedClass("instance2")

instance3 = TrackedClass2("instance3")

instance4 = TrackedClass2("instance3")

instance5 = TrackedClass2("instance3")

instance6 = TrackedClass2("instance3")

instance7 = TrackedClass2("instance3")

instance8 = TrackedClass2("instance3")

from logic import TrackedObjectSet

print(TrackedObjectSet.sets)
