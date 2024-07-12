import json
import threading
from dto.dbTools import *
from dao.dataItems import *
from GLOBAL_DEFINE import UNIFIED_TIME_FORMAT, VERSION_INFO
from dto.SqliteDB import DBManipulator
import random
import string
from datetime import timedelta
from SubscribeCore import SubscribeCore
from logging_module import Logger


def login_by_passwd(username: str, passwd: str) -> str:
    ss = DBManipulator()
    user = ss.get_cursor().execute("SELECT * FROM userTable where username=? and passwd=?;",
                                   (username, passwd)).fetchone()
    if not user:
        return ""
    if user[4] == "" or user[3] == "":
        session = "".join(random.sample(string.ascii_letters, 9))
        valid = (datetime.now() + timedelta(weeks=1)).strftime(UNIFIED_TIME_FORMAT)
        ss.get_cursor().execute("UPDATE userTable set session=?,valid_until=?; WHERE ", (session, valid))
        return session
    if datetime.strptime(user[4], UNIFIED_TIME_FORMAT) < datetime.now():
        session = "".join(random.sample(string.ascii_letters, 9))
        valid = (datetime.now() + timedelta(weeks=1)).strftime(UNIFIED_TIME_FORMAT)
        ss.get_cursor().execute("UPDATE userTable set session=?,valid_until=?; WHERE ", (session, valid))
        return session
    else:
        return user[3]


def check_operation_is_legal(session: str, required_min_level: int) -> bool:
    if len(session) < 9:
        return False
    if float(VERSION_INFO[0:3]) < 1.0:
        return True  # for version<1.0 , no login function is using, then this check method always return True
    ss = DBManipulator()
    user = ss.get_cursor().execute("SELECT session,valid_until,user_level FROM userTable where session=?;",
                                   (session,)).fetchone()
    if not user:
        return False
    if datetime.strptime(user[1], UNIFIED_TIME_FORMAT) < datetime.now():
        return False
    if user[2] < required_min_level and (0 < user[2] < 5):
        return True
    else:
        return False


def get_all_metadata() -> str:
    items = getMetadataItems()
    metadata_dict_list = []
    for item in items:
        item_dict = item.get_dict()
        metadata_dict_list.append(item_dict)
    response_dict = {"status": 200, "auth": f"xy-nas-tools {VERSION_INFO}",
                     "time": datetime.utcnow().strftime(UNIFIED_TIME_FORMAT) + " UTC",
                     "metadata_dict_list": metadata_dict_list}
    return json.dumps(response_dict, ensure_ascii=False)


def get_current_metadata() -> str:
    items = getMetadataItems()
    metadata_dict_list = []
    for item in items:
        subscription_item = SubscriptionItem(item.id)
        if subscription_item.totalEpisodes < subscription_item.nextUpdateEP:
            continue
        item_dict = item.get_dict()
        metadata_dict_list.append(item_dict)
    response_dict = {"status": 200, "auth": f"xy-nas-tools {VERSION_INFO}",
                     "time": datetime.utcnow().strftime(UNIFIED_TIME_FORMAT) + " UTC",
                     "metadata_dict_list": metadata_dict_list}
    return json.dumps(response_dict, ensure_ascii=False)


def get_subscription_item(id: int) -> str:
    if not (0 < id < getValidID()):
        return json.dumps({"status": 404, "auth": f"xy-nas-tools {VERSION_INFO}",
                     "time": datetime.utcnow().strftime(UNIFIED_TIME_FORMAT) + " UTC"})
    subscription_item = SubscriptionItem(id)
    response_dict = {"status": 200, "auth": f"xy-nas-tools {VERSION_INFO}",
                     "time": datetime.utcnow().strftime(UNIFIED_TIME_FORMAT) + " UTC",
                     "subscription_item": subscription_item.get_dict()}
    return json.dumps(response_dict, ensure_ascii=False)


def get_about_info() -> str:  # for about method
    about_info = f"xy-nas-tool/AnimeAssistant\r" \
                 f"Version:{VERSION_INFO}\r" \
                 f"Original Project Repo in Github: xyseer/AnimeAssistant\r" \
                 f"Original Docker Image Repo in DockerHub: xyseer/AnimeAssistant\r" \
                 f"Any issue please let me know on Github Project!"
    response_dict = {"status": 200, "auth": f"xy-nas-tools {VERSION_INFO}",
                     "time": datetime.utcnow().strftime(UNIFIED_TIME_FORMAT) + " UTC",
                     "about_info": about_info}
    return json.dumps(response_dict, ensure_ascii=False)


def get_new_subscription_item(session: str = "defaultvalue") -> [MetadataItem, SubscriptionItem]:  # for add method
    if check_operation_is_legal(session, 3):
        new_id = getValidID()
        NameItem(new_id, f"new series {new_id}")
        DownloadItem(new_id, f"new series {new_id}",source='https://nyaa.si/?page=rss&q=[];https://miobt.com/rss-[].xml;https://dmhy.anoneko.com/topics/rss/rss.xml?keyword=[];https://www.tokyotosho.info/rss.php?terms=[]')
        s = SubscriptionItem(new_id, f"new series {new_id}")
        m = MetadataItem(new_id, f"new series {new_id}", info="no information.")
        return [m, s]
    else:
        return None


def delete_item(item_id: int, session: str = "defaultvalue") -> bool:
    if not (0 < item_id < getValidID()):
        return False
    n_m = NameItem(item_id)
    if check_operation_is_legal(session, n_m.user_level):
        n_m.deleteItem()
        del n_m
        return True
    else:
        return False


def modify_item(new_dict: dict, session: str = "defaultvalue") -> bool:
    if new_dict.get("id", -1) < 0:
        return False
    if check_operation_is_legal(session, 3):
        id = new_dict.get("id", -1)
        NameItem(id).from_dict(new_dict).push()
        SubscriptionItem(id).from_dict(new_dict).push()
        DownloadItem(id).from_dict(new_dict).push()
        MetadataItem(id).from_dict(new_dict).push()
        return True
    else:
        return False


def threadDecorator(func):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper


@threadDecorator
def subscribe_immediately(id: int,ss:SubscribeCore) -> bool:
    if 0 < id <= getValidID():
        d = DownloadItem(id)
        if SubscribeCore.single_item_subscribe(d):
            try:
                ss.remap_scheduler()
            except Exception:
                return False
            return True
        else:
            Logger().warning(f"Immediately Subscribe {d.name} failed.")
            return False
    else:
        return False


def download_once(download_item:DownloadItem)->bool:
    try:
        return SubscribeCore.get_type_downloader(download_item).download()
    except:
        return False