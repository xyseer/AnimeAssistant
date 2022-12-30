import json
from dao.IEItem import IEItem
import os
from GLOBAL_DEFINE import CONFIG_DIR, CONFIG_FILE
from logging_module import BaseLogger
from typing import TypeVar

_T = TypeVar('_T', bound="Parameters")


class Parameters(IEItem):
    def __init__(self):
        self.DEFAULT_ADDRESS="0.0.0.0:12138"
        self.DB_PATH = CONFIG_DIR + "/XNT.db"
        self.ARIA2_RPC_SERVER = "http://127.0.0.1:6800/jsonrpc"
        self.ARIA2_JSONRPC_TOKEN = ""
        self.LOG_DIR = CONFIG_DIR + "/logs/"
        self.LOG_LEVEL = "ERROR"
        self.JACKETT_API_LINK_LIST = []
        self.ERROR_RETRY_SPAN = 2
        self.REGULAR_CHECK_SPAN = 24
        self.FILTER_DICTS = {"default": {"reject_rules": ["720"], "apply_rules": ["1080"]}}
        self.other = {}
        super().__init__()
        self.fetch()

    def get_dict(self) -> dict:
        return {
            'DEFAULT_ADDRESS':self.DEFAULT_ADDRESS,
            'DB_PATH': self.DB_PATH,
            'LOG_DIR': self.LOG_DIR,
            'LOG_LEVEL': self.LOG_LEVEL,
            'ERROR_RETRY_SPAN': self.ERROR_RETRY_SPAN,
            'REGULAR_CHECK_SPAN': self.REGULAR_CHECK_SPAN,
            'ARIA2_RPC_SERVER': self.ARIA2_RPC_SERVER,
            'ARIA2_JSONRPC_TOKEN': self.ARIA2_JSONRPC_TOKEN,
            'JACKETT_API_LINK_LIST': self.JACKETT_API_LINK_LIST,
            'FILTER_DICTs': self.FILTER_DICTS,
            'other': self.other
        }

    def from_dict(self, source_dict: dict) -> _T:
        self.DEFAULT_ADDRESS=source_dict.get('DEFAULT_ADDRESS', self.DEFAULT_ADDRESS)
        self.DB_PATH = source_dict.get('DB_PATH', self.DB_PATH)
        self.LOG_DIR = source_dict.get('LOG_DIR', self.LOG_DIR)
        self.LOG_LEVEL = source_dict.get('LOG_DIR', self.LOG_LEVEL)
        self.ERROR_RETRY_SPAN = tryParseInt(source_dict.get('ERROR_RETRY_SPAN', self.ERROR_RETRY_SPAN))
        self.REGULAR_CHECK_SPAN = tryParseInt(source_dict.get('REGULAR_CHECK__SPAN', self.REGULAR_CHECK_SPAN))
        self.ARIA2_RPC_SERVER = source_dict.get('ARIA2_RPC_SERVER', self.ARIA2_RPC_SERVER)
        self.ARIA2_JSONRPC_TOKEN = source_dict.get('ARIA2_JSONRPC_TOKEN', self.ARIA2_JSONRPC_TOKEN)
        self.JACKETT_API_LINK_LIST = source_dict.get('JACKETT_API_LINK_LIST', self.JACKETT_API_LINK_LIST)
        self.FILTER_DICTS = source_dict.get('FILTER_DICTS', self.FILTER_DICTS)
        self.other = source_dict.get('other', self.other)
        return self

    def fetch(self, file_path=CONFIG_FILE) -> _T:
        if not os.path.exists(CONFIG_DIR):
            os.mkdir(CONFIG_DIR)
        if not os.path.exists(file_path):
            print(file_path)
            open(file_path, "w").close()
        with open(file_path, "r", encoding="utf8") as fp:
            try:
                paras_json = json.load(fp)
            except Exception:
                paras_json = ""
        if not paras_json:
            if not os.path.exists(self.LOG_DIR):
                os.mkdir(self.LOG_DIR)
                BaseLogger(self.LOG_DIR, self.LOG_LEVEL).error("No Valid Config, using default.")
            self.push(file_path)
        else:
            try:
                self.from_dict(paras_json)
            except Exception:
                return self
        return self

    def push(self, file_path=CONFIG_FILE) -> _T:
        with open(file_path, "w") as fp:
            paras_json = self.get_dict()
            json.dump(paras_json, fp)
            BaseLogger(self.LOG_DIR, self.LOG_LEVEL).info("Parameters are Saved.")
        return self


def tryParseInt(input: str) -> int:
    try:
        return int(input)
    except ValueError:
        return 0
