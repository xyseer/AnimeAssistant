import re
import xml.etree.ElementTree as ET
import os
import requests
from dao.DownloadItem import DownloadItem
from parameters import Parameters
from download_tools.IEDownloadMethod import IEDownloadMethod
from logging_module import Logger
from download_tools.Aria2 import Aria2


class Jackett(IEDownloadMethod):
    def __init__(self, downloaditem: DownloadItem):
        super(Jackett, self).__init__(downloaditem)

    def download(self) -> bool:
        p = Parameters()
        for i in self.downloaditem.filter_name:
            if checkExist(self.downloaditem.directory, format_episode_str(self.downloaditem.nextUpdateEP),
                          p.FILTER_DICTS.get(i, {"reject_rules": ["720"], "apply_rules": ["1080"]})):
                Logger().info(
                    f"Jackett check {self.downloaditem.name}[{self.downloaditem.nextUpdateEP}] already in your directory. Updated database and skipped.")
                return True
        Logger().info(f"Jackett start lokking for {self.downloaditem.name}")
        try:
            for api_url in p.JACKETT_API_LINK_LIST:
                api_request_url = api_url + self.downloaditem.source
                r = requests.get(api_request_url).text
                torznab_ns = "{" + p.other.get("torznab_ns", "http://torznab.com/schemas/2015/feed") + "}"
                jackett_result_xml = ET.fromstring(r)
                root = jackett_result_xml.iter("item")
                for child in root:
                    title = ""
                    for e in child.iter("title"):
                        title = e.text
                    for i in self.downloaditem.filter_name:
                        if resolve_regex_match(title, format_episode_str(self.downloaditem.nextUpdateEP),
                                               p.FILTER_DICTS.get(i,
                                                                  {"reject_rules": ["720"], "apply_rules": ["1080"]})):
                            for i in child.iter(f"{torznab_ns}attr"):
                                if i.get("name") == "magneturl":
                                    link = i.get("value")
                                    a_d = Aria2(self.downloaditem, link)
                                    if a_d.download():
                                        return True
                                    else:
                                        continue
            return False

        except Exception as e:
            Logger().error(f"Jackett Module ocurred an error:{str(e)}")
            return False


def format_episode_str(ep: int):
    if ep < 10 and ep > 0:
        return "0" + str(ep)
    elif ep < 0:
        return "01"
    else:
        return str(ep)


def checkExist(directory, ep, filter_dict):
    try:
        files = os.listdir(directory)
        for file in files:
            file_name = re.sub("([^.]\w*$)", "", file)
            if file_name == "" or file_name == ".":
                continue
            else:
                if resolve_regex_match(file_name, ep, filter_dict):
                    return True
        return False
    except FileNotFoundError:
        return False


def resolve_regex_match(title, ep: str, filter_dict):
    for reject_rule in filter_dict.get("reject_rules", []):
        if re.search(reject_rule, title, re.I):
            return False
    for including_rule in filter_dict.get("apply_rules", []):
        if not re.search(including_rule, title, re.I):
            return False
    if not re.search("\[" + ep + "]", title, re.I):
        title = re.sub("(([1-9]|1[0-2])月)|(\d{4}年|\d{2}年)", "", title)
        title = re.sub("(Big5)|(h26\d)|(\d{3}p)|(\d{4}p)|(\d{2}bit)|(\d{1}bit)", "", title, flags=re.I)
        if not re.search(ep, title):
            return False
    return True
