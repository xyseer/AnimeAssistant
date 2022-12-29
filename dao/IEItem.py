from typing import TypeVar

_T = TypeVar('_T', bound="IEItem")


class IEItem:
    def __init__(self, id=-1, name=""):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"{(self.id, self.name)}"

    def get_dict(self) -> dict:
        return {"id": self.id, "name": self.name}

    def from_dict(self, source_dict: dict) -> _T:
        self.id = source_dict.get("id", -1)
        self.name = source_dict.get("name", "")
        return self

    def fetch(self) -> _T:
        return self

    def push(self) -> _T:
        return self
