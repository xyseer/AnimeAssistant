import re
import string
from random import sample

from GLOBAL_DEFINE import UNIFIED_TIME_FORMAT
from datetime import datetime
from typing import overload
from dto.SqliteDB import DBManipulator


def adapt_datetime(val: datetime):
    return val.strftime(UNIFIED_TIME_FORMAT)


@overload
def convert_datetime(val: bytes):
    return datetime.strptime(val.decode("utf8"), UNIFIED_TIME_FORMAT)


def convert_datetime(val: str):
    return datetime.strptime(val, UNIFIED_TIME_FORMAT)


def safe_filename(name: str, replacement: str = "_", max_length: int = 255) -> str:
    # Define invalid characters across platforms (especially Windows)
    invalid_chars = r'<>:"/\\|?*\0!'
    # Remove control characters
    name = re.sub(r'[\x00-\x1f\x7f]', replacement, name)
    # Replace invalid characters with replacement
    name = re.sub(f"[{re.escape(invalid_chars)}]", replacement, name)
    name = re.sub(r"\s+", replacement, name)
    # Remove repeated replacements
    name = re.sub(f"{re.escape(replacement)}+", replacement, name)
    # Trim and truncate
    name = name.strip().strip('. ')
    return name[:max_length] or ''.join(sample(string.ascii_letters + string.digits, 16))


def listTostr(l: list, sep: str = ";"):
    result = ""
    for x in l[0:-1]:
        result += x + sep
    result += l[-1]
    return result


def strTolist(s: str, sep: str = ";"):
    result = s.split(";")
    result.remove("") if "" in result else result
    return result


def getValidID():
    ss = DBManipulator()
    seq_tuple = ss.get_cursor().execute("SELECT seq FROM sqlite_sequence WHERE name='nameTable'").fetchone()
    if not seq_tuple:
        seq = 1
    else:
        seq = seq_tuple[0] + 1
    return seq


def getSubscriptionItems() -> list:
    from dao.SubscriptionItem import SubscriptionItem
    ss = DBManipulator()
    item_from_db = ss.get_cursor().execute("SELECT * FROM SubscriptionItem ORDER BY nextUpdateTime DESC;").fetchall()
    del ss
    result_items = []
    for i in item_from_db:
        s = SubscriptionItem(-1)
        if not i[4]:
            continue
        s.id, s.name, starttime, s.totalEpisodes, lastUpdateTime, s.lastUpdateEP, nextUpdateTime, s.nextUpdateEP, s.span, s.type = i
        if not i[2]:
            s.starttime = datetime.now().strftime(UNIFIED_TIME_FORMAT)
        s.starttime, s.lastUpdateTime, s.nextUpdateTime = convert_datetime(starttime), convert_datetime(
            lastUpdateTime), convert_datetime(nextUpdateTime)
        result_items.append(s)
    return result_items


def getDownloadItems() -> list:
    from dao.DownloadItem import DownloadItem, IEItem
    ss = DBManipulator()
    item_from_db = ss.get_cursor().execute("SELECT * FROM DownloadItem ORDER BY nextUpdateTime DESC;").fetchall()
    del ss
    result_items = []
    for i in item_from_db:
        if not i[2]:
            continue
        s = DownloadItem(-1)
        s.id, s.name, lastUpdateTime, s.lastUpdateEP, nextUpdateTime, s.nextUpdateEP, s.span, s.type, s.source, s.directory, filter_name, related_item = i
        s.lastUpdateTime, s.nextUpdateTime = convert_datetime(lastUpdateTime), convert_datetime(nextUpdateTime)
        filter_name_dirty = strTolist(filter_name)
        s.filter_name = filter_name_dirty if len(filter_name_dirty) > 0 else ["default"]
        if related_item:
            try:
                s.related_item = getattr(getattr(__import__(related_item), related_item.split(".")[-1], IEItem),
                                         related_item.split(".")[-1], IEItem)(s.id)
            except ModuleNotFoundError or AttributeError:
                s.related_item = IEItem(s.id)
        else:
            s.related_item = IEItem(s.id)
        result_items.append(s)
    return result_items


def getDownloadItemById(id: int):
    from dao.DownloadItem import DownloadItem, IEItem
    ss = DBManipulator()
    item_from_db = ss.get_cursor().execute("SELECT * FROM DownloadItem WHERE id =?", (id,)).fetchone()
    del ss
    s = DownloadItem(-1)
    if item_from_db is not None:
        s.id, s.name, lastUpdateTime, s.lastUpdateEP, nextUpdateTime, s.nextUpdateEP, s.span, s.type, s.source, s.directory, filter_name, related_item = item_from_db
        s.lastUpdateTime, s.nextUpdateTime = convert_datetime(lastUpdateTime), convert_datetime(nextUpdateTime)
        filter_name_dirty = strTolist(filter_name)
        s.filter_name = filter_name_dirty if len(filter_name_dirty) > 0 else ["default"]
        if related_item:
            try:
                s.related_item = getattr(getattr(__import__(related_item), related_item.split(".")[-1], IEItem),
                                         related_item.split(".")[-1], IEItem)(s.id)
            except ModuleNotFoundError or AttributeError:
                s.related_item = IEItem(s.id)
        else:
            s.related_item = IEItem(s.id)
    return s


def getMetadataItems() -> list:
    from dao.MetaDataItem import MetadataItem
    ss = DBManipulator()
    item_from_db = ss.get_cursor().execute("SELECT * FROM metadataItem ORDER BY id DESC;").fetchall()
    del ss
    result_items = []
    for i in item_from_db:
        s = MetadataItem(-1)
        s.id, s.name, s.img, s.info, s.animedb_id = i
        result_items.append(s)
    return result_items


def getNameItems():
    from dao.NameItem import NameItem
    ss = DBManipulator()
    item_from_db = ss.get_cursor().execute("SELECT * FROM nameTable").fetchall()
    del ss
    result_items = []
    for i in item_from_db:
        s = NameItem(-1)
        s.id, s.name, s.user_level = i
        result_items.append(s)
    return result_items
