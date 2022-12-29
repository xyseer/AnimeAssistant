from dao.IEItem import IEItem
from typing import TypeVar
from dto.SqliteDB import DBManipulator
from dao.NameItem import NameItem

_T = TypeVar('_T', bound="MetadataItem")


class MetadataItem(IEItem):
    def __init__(self,
                 id: int,
                 name: str = "",
                 img: str = "/static/default.jpg",
                 info: str = "",
                 animedb_id: str = ""):
        super(MetadataItem, self).__init__(id, name)
        self.img = img
        self.info = info
        self.animedb_id = animedb_id
        self.fetch()

    def __repr__(self):
        return f"{self.id, self.name, self.img, self.info}"

    def get_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "img": self.img, "info": self.info, "animedb_id": self.animedb_id}

    def from_dict(self, source_dict: dict) -> _T:
        self.id = source_dict.get("id", self.id)
        self.name = source_dict.get("name", self.name)
        self.img = source_dict.get("img", self.img)
        self.info = source_dict.get("info", self.info)
        self.animedb_id = source_dict.get("animedb_id", self.animedb_id)
        return self

    def fetch(self) -> _T:
        if self.id == -1:
            return self
        ss = DBManipulator()
        item_from_db = ss.get_cursor().execute("SELECT * FROM metadataItem WHERE id=?;", (self.id,)).fetchone()
        del ss
        if not item_from_db:
            self.push()
            return self
        self.id, self.name, self.img, self.info, self.animedb_id = item_from_db
        return self

    def push(self) -> _T:
        if self.id == -1:
            return self
        NameItem(self.id,self.name).push()
        ss = DBManipulator()
        if not ss.get_cursor().execute("SELECT * FROM metadataItem WHERE id=?", (self.id,)).fetchone():
            ss.get_cursor().execute("INSERT INTO metadataTable VALUES(?,?,?,?);",
                                    (self.id, self.img, self.info, self.animedb_id))
            ss.commit()
            del ss
            return self
        else:
            ss.get_cursor().execute(
                "UPDATE metadataTable SET img=?,info=?,AnimeDBid=? WHERE id=?;",
                (self.img, self.info, self.animedb_id, self.id))
            ss.commit()
            del ss
            return self
