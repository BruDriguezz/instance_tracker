# tests/test_metatrack.py

import pytest
from src.metatrack.track import track


def test_track():
    @track()
    class Foo(object):
        def __init__(self) -> None:
            self.x = 1

    X = Foo()
    Y = Foo()
    Z = Foo()

    assert len(Foo.instances) == 3 # 3 instances of Foo


def test_track_limit():
    with pytest.raises(RuntimeError):
        @track(instance_limit=2)
        class Foo(object):
            def __init__(self) -> None:
                self.x = 1

        X = Foo()
        Y = Foo()
        Z = Foo()  # RuntimeError: Cannot create more than 3 instances of Foo.
