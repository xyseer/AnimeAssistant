from dao.IEItem import IEItem
from datetime import datetime
from typing import TypeVar
from GLOBAL_DEFINE import UNIFIED_TIME_FORMAT
from dto.SqliteDB import DBManipulator
from dto.dbTools import convert_datetime
from dao.NameItem import NameItem

_T = TypeVar('_T', bound="SubscriptionItem")


class SubscriptionItem(IEItem):
    def __init__(self,
                 id: int,
                 name: str = "",
                 starttime: datetime = None,
                 totalEpisodes: int = 0,
                 lastUpdateTime: datetime = None,
                 lastUpdateEP: int = 0,
                 nextUpdateTime: datetime = None,
                 nextUpdateEP: int = 1,
                 span: int = 168,
                 type: str = "Jackett"):
        super(SubscriptionItem, self).__init__(id, name)
        self.starttime = starttime if starttime is not None else datetime.now()
        self.totalEpisodes = totalEpisodes
        self.lastUpdateTime = lastUpdateTime if lastUpdateTime is not None else datetime.now()
        self.lastUpdateEP = lastUpdateEP
        self.nextUpdateTime = nextUpdateTime if nextUpdateTime is not None else datetime.now()
        self.nextUpdateEP = nextUpdateEP
        self.span = span
        self.type = type
        self.fetch()

    def __repr__(self):
        return f"{self.id, self.name, self.starttime.strftime(UNIFIED_TIME_FORMAT), self.totalEpisodes, self.lastUpdateTime.strftime(UNIFIED_TIME_FORMAT), self.lastUpdateEP, self.nextUpdateTime.strftime(UNIFIED_TIME_FORMAT), self.nextUpdateEP, self.span, self.type}"

    def get_dict(self) -> dict:
        return {"id": self.id,
                "name": self.name,
                "starttime": self.starttime.strftime(UNIFIED_TIME_FORMAT),
                "totalEpisodes": self.totalEpisodes,
                "lastUpdateTime": self.lastUpdateTime.strftime(UNIFIED_TIME_FORMAT),
                "lastUpdateEP": self.lastUpdateEP,
                "nextUpdateTime": self.nextUpdateTime,
                "nextUpdateEP": self.nextUpdateEP,
                "span": self.span,
                "type": self.type}

    def from_dict(self, source_dict: dict) -> _T:
        self.id = source_dict.get("id", self.id)
        self.name = source_dict.get("name", self.name)
        self.starttime = source_dict.get("starttime", self.starttime)
        self.totalEpisodes = source_dict.get("totalEpisodes", self.totalEpisodes)
        self.lastUpdateTime = source_dict.get("lastUpdateTime", self.lastUpdateTime)
        self.lastUpdateEP = source_dict.get("lastUpdateEP", self.lastUpdateEP)
        self.nextUpdateTime = source_dict.get("nextUpdateTime", self.nextUpdateTime)
        self.nextUpdateEP = source_dict.get("nextUpdateEP", self.nextUpdateEP)
        self.span = source_dict.get("span", self.span)
        self.type = source_dict.get("type", self.type)
        return self

    def fetch(self) -> _T:
        if self.id == -1:
            return self
        ss = DBManipulator()
        item_from_db = ss.get_cursor().execute("SELECT * FROM SubscriptionItem WHERE id=?;", (self.id,)).fetchone()
        del ss
        if not item_from_db:
            self.push()
            return self
        if not item_from_db[4]:
            self.push()
            return self
        self.id, self.name, starttime, self.totalEpisodes, lastUpdateTime, self.lastUpdateEP, nextUpdateTime, self.nextUpdateEP, self.span, self.type = item_from_db
        if not item_from_db[2]:
            self.starttime = datetime.now().strftime(UNIFIED_TIME_FORMAT)
        self.starttime, self.lastUpdateTime, self.nextUpdateTime = convert_datetime(starttime), convert_datetime(
            lastUpdateTime), convert_datetime(nextUpdateTime)
        return self

    def push(self) -> _T:
        if self.id == -1:
            return self
        NameItem(self.id,self.name).push()
        ss = DBManipulator()
        if not ss.get_cursor().execute("SELECT * FROM SubscriptionItem WHERE id=?", (self.id,)).fetchone():
            ss.get_cursor().execute("INSERT INTO subscriptionTable VALUES(?,?,?,?,?,?,?,?,?);", (
                self.id, self.starttime.strftime(UNIFIED_TIME_FORMAT), self.totalEpisodes,
                self.lastUpdateTime.strftime(UNIFIED_TIME_FORMAT), self.lastUpdateEP,
                self.nextUpdateTime.strftime(UNIFIED_TIME_FORMAT), self.nextUpdateEP, self.span, self.type))
            ss.commit()
            del ss
            return self
        else:
            ss.get_cursor().execute(
                "UPDATE subscriptionTable SET starttime=?,totalEpisodes=?,lastUpdateTime=?,lastUpdateEP=?,nextUpdateTime=?,nextUpdateEP=?,span=?,type=? WHERE id=?;",
                (self.starttime.strftime(UNIFIED_TIME_FORMAT), self.totalEpisodes,
                 self.lastUpdateTime.strftime(UNIFIED_TIME_FORMAT), self.lastUpdateEP,
                 self.nextUpdateTime.strftime(UNIFIED_TIME_FORMAT), self.nextUpdateEP, self.span, self.type, self.id))
            ss.commit()
            del ss
            return self
