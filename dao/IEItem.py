from typing import TypeVar

_T = TypeVar('_T', bound="IEItem")


class IEItem:
    def __init__(self, id=-1, name=""):
        self.id = id
        self.name = name

    def fetch(self) -> _T:
        return self

    def push(self) -> _T:
        return self
