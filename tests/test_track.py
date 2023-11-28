import pytest
from src.trackerpy import Tracker


def test_FunctionNotSupported():

    @Tracker
    class defClass:
        pass

    X, Y, Z = defClass(), defClass(), defClass()

    assert len(defClass.instances) == 3

