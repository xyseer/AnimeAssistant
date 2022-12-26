from typing import TypeVar
from dto.SqliteDB import DBManipulator
from dao.IEItem import IEItem

_T = TypeVar('_T', bound="MetadataItem")


class NameItem(IEItem):
    def __init__(self, id: int, name: str = ""):
        super(NameItem, self).__init__(id, name)
        self.user_level = 4
        self.fetch()

    def fetch(self) -> _T:
        if self.id == -1:
            return self
        ss = DBManipulator()
        item_from_db = ss.get_cursor().execute("SELECT * FROM nameTable where id=?", (self.id,)).fetchone()
        del ss
        if not item_from_db:
            return self.push()
        self.id, self.name, self.user_level = item_from_db
        return self

    def push(self) -> _T:
        if self.id == -1:
            return self
        ss = DBManipulator()
        if not ss.get_cursor().execute("SELECT * FROM nameTable where id=?", (self.id,)).fetchone():
            ss.get_cursor().execute("INSERT INTO nameTable VALUES(?,?,?)", (self.id, self.name, self.user_level))
            ss.commit()
            del ss
            return self
        else:
            ss.get_cursor().execute("UPDATE nameTable SET name=?,user_level=? WHERE id=?",
                                    (self.name, self.user_level, self.id))
            ss.commit()
            del ss
            return self

    def deleteItem(self):
        if self.id == -1:
            return self
        ss = DBManipulator()
        ss.get_cursor().execute("PRAGMA foreign_keys = true;")
        ss.get_cursor().execute("DELETE FROM nameTable WHERE id=?;", (self.id,))
        ss.commit()
        self.id = -1
        del ss
        return self
