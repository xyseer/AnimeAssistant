from IEItem import IEItem
from datetime import datetime
from typing import TypeVar
from GLOBAL_DEFINE import UNIFIED_TIME_FORMAT
from dto.SqliteDB import DBManipulator
from dto.dbTools import convert_datetime

_T = TypeVar('_T', bound="SubscriptionItem")


class SubscriptionItem(IEItem):
    def __init__(self,
                 id: int,
                 name: str = "",
                 starttime: datetime = datetime.now(),
                 totalEpisodes: int = 0,
                 lastUpdateTime: datetime = datetime.now(),
                 lastUpdateEP: int = 0,
                 nextUpdateTime: datetime = datetime.now(),
                 nextUpdateEP: int = 1,
                 span: int = 168,
                 type: str = "jackett"):
        super(SubscriptionItem, self).__init__(id, name)
        self.starttime = starttime
        self.totalEpisodes = totalEpisodes
        self.lastUpdateTime = lastUpdateTime
        self.lastUpdateEP = lastUpdateEP
        self.nextUpdateTime = nextUpdateTime
        self.nextUpdateEP = nextUpdateEP
        self.span = span
        self.type = type
        self.fetch()

    def __repr__(self):
        return f"{self.id, self.name, self.starttime.strftime(UNIFIED_TIME_FORMAT), self.totalEpisodes, self.lastUpdateTime.strftime(UNIFIED_TIME_FORMAT), self.lastUpdateEP, self.nextUpdateTime.strftime(UNIFIED_TIME_FORMAT), self.nextUpdateEP, self.span, self.type}"

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
        ss = DBManipulator()
        if not ss.get_cursor().execute("SELECT * FROM SubscriptionItem WHERE id=?", (self.id,)).fetchone():
            ss.get_cursor().execute("INSERT INTO nameTable(id,name) VALUES(?,?);", (self.id, self.name))
            ss.get_cursor().execute("INSERT INTO subscriptionTable VALUES(?,?,?,?,?,?,?,?,?);", (
                self.id, self.starttime.strftime(UNIFIED_TIME_FORMAT), self.totalEpisodes,
                self.lastUpdateTime.strftime(UNIFIED_TIME_FORMAT), self.lastUpdateEP,
                self.nextUpdateTime.strftime(UNIFIED_TIME_FORMAT), self.nextUpdateEP, self.span, self.type))
            ss.commit()
            del ss
            return self
        else:
            ss.get_cursor().execute("UPDATE nameTable SET name=? WHERE id=?;", (self.name, self.id))
            ss.get_cursor().execute(
                "UPDATE subscriptionTable SET starttime=?,totalEpisodes=?,lastUpdateTime=?,lastUpdateEP=?,nextUpdateTime=?,nextUpdateEP=?,span=?,type=? WHERE id=?;",
                (self.starttime.strftime(UNIFIED_TIME_FORMAT), self.totalEpisodes,
                 self.lastUpdateTime.strftime(UNIFIED_TIME_FORMAT), self.lastUpdateEP,
                 self.nextUpdateTime.strftime(UNIFIED_TIME_FORMAT), self.nextUpdateEP, self.span, self.type, self.id))
            ss.commit()
            del ss
            return self
