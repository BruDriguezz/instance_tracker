# tests/test_metatrack.py

import pytest
from src.metatrack import track


# Dummy class
@track.track(instance_limit=2)
class Foo:
    def __init__(self, name):
        self.name = name


def test_instance():
    foo = Foo("foo")
    assert foo.name == "foo"


def test_instance_limit():
    foo = Foo("foo")
    bar = Foo("bar")
    with pytest.raises(
        RuntimeError, match="Cannot create more than 2 instances of Foo."
    ):
        baz = Foo("baz")
