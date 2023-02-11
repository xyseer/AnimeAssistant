import json
import random
import string

import requests

from parameters import Parameters
from logging_module import Logger
from download_tools.IEDownloadMethod import IEDownloadMethod
from dao.DownloadItem import DownloadItem


class Aria2(IEDownloadMethod):
    def __init__(self, downloaditem: DownloadItem, link: str=""):
        super(Aria2, self).__init__(downloaditem)
        if link:
            self.link=link
        else:
            self.link=self.downloaditem.source

    def download(self) -> bool:
        result = send_download_info_to_aria2(self.link, self.downloaditem.name, self.downloaditem.directory)
        return True if result else False


def send_download_info_to_aria2(download_link: str, title: str = "Untitled", save_dir: str = "/Download"):
    p = Parameters()
    mission_id = "".join(random.sample(string.ascii_letters, 9))
    aria2_rpc_post_dict = {"id": mission_id,
                           "jsonrpc": "2.0",
                           "method": "aria2.addUri",
                           "params": [
                               f"token:{p.ARIA2_JSONRPC_TOKEN}",
                               [
                                   download_link
                               ],
                               {
                                   "dir": save_dir
                               }
                           ]
                           }
    aria2_rpc_post = json.dumps(aria2_rpc_post_dict)
    try:
        response = requests.post(p.ARIA2_RPC_SERVER, aria2_rpc_post)
        response_json = json.loads(response.text)
        if response_json.get("error", ""):
            Logger().error(
                f"Aria2 jsonrpc server return an error when processing '{title}' :{response_json.get('error', '').get('message', '')}")
            return ""
        if response_json.get("result", ""):
            return response_json.get("result", "")
        return ""
    except Exception as e:
        Logger().error(f"ERROR occured when executing '{title}' in send_download_info_to_aria2 :" + str(e))
        return ""
