import re
import os
import requests
import feedparser
from dao.DownloadItem import DownloadItem
from parameters import Parameters
from download_tools.IEDownloadMethod import IEDownloadMethod
from logging_module import Logger
from download_tools.Aria2 import Aria2
import urllib.parse

headers_pre={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
             "Sec-Fetch-Dest":"document",
             "Accept":"text/html;application/rss+xml;",
             "Accept-Encoding":"gzip,deflate",
             "Accept-Language":"en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7"
             }


class InnerIndexer(IEDownloadMethod):
    def __init__(self, downloaditem: DownloadItem):
        super(InnerIndexer, self).__init__(downloaditem)

    def download(self) -> bool:
        p = Parameters()
        for i in self.downloaditem.filter_name:
            if checkExist(self.downloaditem.directory, format_episode_str(self.downloaditem.nextUpdateEP),
                          p.FILTER_DICTS.get(i, {"reject_rules": ["720"], "apply_rules": ["1080"]})):
                Logger().info(
                    f"InnerIndexer found {self.downloaditem.name}[{self.downloaditem.nextUpdateEP}] has already in your directory. Updated database and skipped.")
                return True
        Logger().info(f"InnerIndexer checking {self.downloaditem.name}")
        try:
            ori_source=self.downloaditem.source
            if not ori_source:
                ori_source=p.DEFAULT_SOURCE
            for source in ori_source.split(";"):
                # replace series name into blank
                search_url=re.sub(r"(\[])|%%|(\[name])|(%name%)",urllib.parse.quote(self.downloaditem.name),source)
                items=feedparser.parse(search_url).get("entries")
                for item in items:
                    item_title=re.sub("","",str(item.get("title")))
                    for i in self.downloaditem.filter_name:
                        if resolve_regex_match(item_title, format_episode_str(self.downloaditem.nextUpdateEP),
                                               p.FILTER_DICTS.get(i,
                                                                  {"reject_rules": ["720"], "apply_rules": ["1080"]})):
                            for link in item.get("links"):
                                if link.get("type", "") == 'application/x-bittorrent':
                                    if link.get("href", "")!="":
                                        a_d = Aria2(self.downloaditem, link.get("href", ""))
                                        if a_d.download():
                                            return True
                                        else:
                                            continue

            return False
        except Exception as e:
            Logger().error(f"InnerIndexer returned an error:{str(e)}")
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
        title = re.sub(r"^[\W_](.*?(?:组|組|屋|社|動漫|Lab|sub|S(?:UB|ub|tudio)|Raw(?:|s)|Production))[\W_]+(?:[\W_]+\d{1,2}(?:月(?:新|)番|国漫)[\W_]+|)[\[【](.*?)[\]】]",r"[\1] \2",title)
        title = re.sub("(([1-9]|1[0-2])月)|(\d{4}年|\d{2}年)", "", title)
        title = re.sub("(Big5)|(h26\d)|(\d{3}p)|(\d{4}p)|(\d{2}bit)|(\d{1}bit)", "", title, flags=re.I)
        if not re.search(ep, title):
            return False
    return True
