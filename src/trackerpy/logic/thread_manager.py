from threading import RLock, get_ident
from contextlib import contextmanager


class ThreadControl:
    """
    A class that manages thread control and synchronization.

    Attributes:
        LOCK (RLock): A reentrant lock used for thread synchronization.

    Methods:
        lock(): A context manager that acquires the lock and yields control.
    """

    LOCK = RLock()

    @classmethod
    @contextmanager
    def lock(cls) -> RLock:
        with cls.LOCK:
            yield
