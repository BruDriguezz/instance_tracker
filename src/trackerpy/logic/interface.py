from abc import ABC, abstractmethod
from typing import Self


class ITrackable(ABC):
    @abstractmethod
    def get(
        self,
        _cls: type,
        /,
        **params,
    ) -> Self:
        pass
        