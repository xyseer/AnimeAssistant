from IEItem import IEItem
from typing import TypeVar
from dto.SqliteDB import DBManipulator

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
        ss = DBManipulator()
        if not ss.get_cursor().execute("SELECT * FROM metadataItem WHERE id=?", (self.id,)).fetchone():
            print("insert")
            ss.get_cursor().execute("INSERT INTO nameTable(id,name) VALUES(?,?);", (self.id, self.name))
            ss.get_cursor().execute("INSERT INTO metadataTable VALUES(?,?,?,?);",
                                    (self.id, self.img, self.info, self.animedb_id))
            ss.commit()
            del ss
            return self
        else:
            print("update")
            ss.get_cursor().execute("UPDATE nameTable SET name=? WHERE id=?;", (self.name, self.id))
            ss.get_cursor().execute(
                "UPDATE metadataTable SET img=?,info=?,AnimeDBid=? WHERE id=?;",
                (self.img, self.info, self.animedb_id, self.id))
            ss.commit()
            del ss
            return self