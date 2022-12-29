from dao.IEItem import IEItem
from datetime import datetime
from typing import TypeVar
from GLOBAL_DEFINE import UNIFIED_TIME_FORMAT
from dto.SqliteDB import DBManipulator
from dto.dbTools import listTostr, strTolist, convert_datetime

_T = TypeVar('_T', bound="DownloadItem")


class DownloadItem(IEItem):
    def __init__(self,
                 id: int,
                 name: str = "",
                 lastUpdateTime: datetime = datetime.now(),
                 lastUpdateEP: int = 0,
                 nextUpdateTime: datetime = datetime.now(),
                 nextUpdateEP: int = 0,
                 span: int = 168,
                 type: str = "jackett",
                 source: str = "",
                 directory: str = "",
                 filter_name=None,
                 related_item: IEItem = None):
        super(DownloadItem, self).__init__(id, name)
        if filter_name is None:
            filter_name = ["dafault"]
        if related_item is None:
            related_item = IEItem()
        self.lastUpdateTime = lastUpdateTime
        self.lastUpdateEP = lastUpdateEP
        self.nextUpdateTime = nextUpdateTime
        self.nextUpdateEP = nextUpdateEP
        self.span = span
        self.type = type
        self.source = source
        self.directory = directory
        self.filter_name = filter_name
        self.related_item = related_item
        self.fetch()

    def __repr__(self):
        return f"{self.id, self.name, self.lastUpdateTime.strftime(UNIFIED_TIME_FORMAT), self.lastUpdateEP, self.nextUpdateTime.strftime(UNIFIED_TIME_FORMAT), self.nextUpdateEP, self.span, self.type, self.source, self.directory, self.filter_name}"

    def get_dict(self) -> dict:
        return {"id": self.id,
                "name": self.name,
                "lastUpdateTime": self.lastUpdateTime.strftime(UNIFIED_TIME_FORMAT),
                "lastUpdateEP": self.lastUpdateEP,
                "nextUpdateTime": self.nextUpdateTime,
                "nextUpdateEP": self.nextUpdateEP,
                "span": self.span,
                "type": self.type,
                "source": self.source,
                "directory": self.directory,
                "filter_name": self.filter_name,
                "related_item": self.related_item.__module__}

    def from_dict(self, source_dict: dict) -> _T:
        self.id = source_dict.get("id", self.id)
        self.name = source_dict.get("name", self.name)
        self.lastUpdateTime = source_dict.get("lastUpdateTime", self.lastUpdateTime)
        self.lastUpdateEP = source_dict.get("lastUpdateEP", self.lastUpdateEP)
        self.nextUpdateTime = source_dict.get("nextUpdateTime", self.nextUpdateTime)
        self.nextUpdateEP = source_dict.get("nextUpdateEP", self.nextUpdateEP)
        self.span = source_dict.get("span", self.span)
        self.type = source_dict.get("type", self.type)
        self.source = source_dict.get("source", self.source)
        self.directory = source_dict.get("directory", self.directory)
        self.filter_name = source_dict.get("filter_name", self.filter_name)
        related_item = source_dict.get("related_item", self.related_item.__module__)
        if related_item:
            try:
                self.related_item = getattr(getattr(__import__(related_item), related_item.split(".")[-1], IEItem),
                                            related_item.split(".")[-1], IEItem)(self.id)
            except ModuleNotFoundError or AttributeError:
                self.related_item = IEItem(self.id)
        else:
            self.related_item = IEItem(self.id)
        return self

    def fetch(self) -> _T:
        if self.id == -1:
            return self
        ss = DBManipulator()
        item_from_db = ss.get_cursor().execute("SELECT * FROM DownloadItem WHERE id=?;", (self.id,)).fetchone()
        del ss
        if not item_from_db:
            self.push()
            return self
        if not item_from_db[2]:
            self.push()
            return self
        self.id, self.name, lastUpdateTime, self.lastUpdateEP, nextUpdateTime, self.nextUpdateEP, self.span, self.type, self.source, self.directory, filter_name, related_item = item_from_db
        self.lastUpdateTime, self.nextUpdateTime = convert_datetime(lastUpdateTime), convert_datetime(nextUpdateTime)
        filter_name_dirty = strTolist(filter_name)
        self.filter_name = filter_name_dirty if len(filter_name_dirty) > 0 else ["default"]
        if related_item:
            try:
                self.related_item = getattr(getattr(__import__(related_item), related_item.split(".")[-1], IEItem),
                                            related_item.split(".")[-1], IEItem)(self.id)
            except ModuleNotFoundError or AttributeError:
                self.related_item = IEItem(self.id)
        else:
            self.related_item = IEItem(self.id)
        return self

    def push(self) -> _T:
        if self.id == -1:
            return self
        ss = DBManipulator()
        if not ss.get_cursor().execute("SELECT * FROM DownloadItem WHERE id=?", (self.id,)).fetchone():
            ss.get_cursor().execute("INSERT INTO nameTable(id,name) VALUES(?,?);", (self.id, self.name))
            ss.get_cursor().execute("INSERT INTO subscriptionTable VALUES(?,?,?,?,?,?,?,?,?);", (
                self.id, datetime.now().strftime(UNIFIED_TIME_FORMAT), self.nextUpdateEP,
                self.lastUpdateTime.strftime(UNIFIED_TIME_FORMAT), self.lastUpdateEP,
                self.nextUpdateTime.strftime(UNIFIED_TIME_FORMAT), self.nextUpdateEP, self.span, self.type))
            ss.get_cursor().execute("INSERT INTO downloadTable VALUES(?,?,?,?,?);",
                                    (self.id, self.source, self.directory, listTostr(self.filter_name),
                                     self.related_item.__module__))
            ss.commit()
            del ss
            return self
        else:
            ss.get_cursor().execute("UPDATE nameTable SET name=? WHERE id=?;", (self.name, self.id))
            ss.get_cursor().execute(
                "UPDATE subscriptionTable SET lastUpdateTime=?,lastUpdateEP=?,nextUpdateTime=?,nextUpdateEP=?,span=?,type=? WHERE id=?;",
                (self.lastUpdateTime.strftime(UNIFIED_TIME_FORMAT), self.lastUpdateEP,
                 self.nextUpdateTime.strftime(UNIFIED_TIME_FORMAT), self.nextUpdateEP, self.span, self.type, self.id))
            ss.get_cursor().execute(
                "UPDATE downloadTable SET source=?,directory=?,filter_name=?,related_table=? WHERE id=?;",
                (self.source, self.directory, listTostr(self.filter_name), self.related_item.__module__, self.id))
            ss.commit()
            del ss
            return self
