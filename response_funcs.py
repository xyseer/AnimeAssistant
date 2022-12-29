import json
from dto.dbTools import *
from dao.dataItems import *
from GLOBAL_DEFINE import UNIFIED_TIME_FORMAT, VERSION_INFO


def login(username: str, passwd: str) -> int:
    pass  # for version<1.0, no login method required


def get_all_metadata() -> str:
    items = getMetadataItems()
    metadata_dict_list = []
    for item in items:
        item_dict = item.get_dict()
        metadata_dict_list.append(item_dict)
    response_dict = {"status": 200, "auth": f"xy-nas-tools {VERSION_INFO}",
                     "time": datetime.utcnow().strftime(UNIFIED_TIME_FORMAT) + " UTC",
                     "metadata_dict_list": metadata_dict_list}
    return json.dumps(response_dict)


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
    return json.dumps(response_dict)


def get_subscription_item(id: int) -> str:
    subscription_item = SubscriptionItem(id)
    response_dict = {"status": 200, "auth": f"xy-nas-tools {VERSION_INFO}",
                     "time": datetime.utcnow().strftime(UNIFIED_TIME_FORMAT) + " UTC",
                     "subscription_item": subscription_item.get_dict()}
    return json.dumps(response_dict)

def get_about_info()->str:
    about_info=f"xy-nas-tool/AnimeAssistant\n" \
               f"Version:{VERSION_INFO}\n" \
               f"Original Project Repo in Github: xyseer/AnimeAssistant\n" \
               f"Original Docker Image Repo in DockerHub: xyseer/AnimeAssistant\n" \
               f"Any issue please let me know on Github Project!"
    response_dict = {"status": 200, "auth": f"xy-nas-tools {VERSION_INFO}",
                     "time": datetime.utcnow().strftime(UNIFIED_TIME_FORMAT) + " UTC",
                     "about_info": about_info}
    return json.dumps(response_dict)
