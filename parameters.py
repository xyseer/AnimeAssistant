import json
from dao.IEItem import IEItem
import os
from GLOBAL_DEFINE import CONFIG_DIR,CONFIG_FILE
from logging_module import BaseLogger

class Parameters(IEItem):
    def __init__(self):
        self.DB_PATH=CONFIG_DIR+"/XNT.db"
        self.ARIA2_RPC_SERVER="http://127.0.0.1:6800/jsonrpc"
        self.ARIA2_JSONRPC_TOKEN=""
        self.LOG_DIR=CONFIG_DIR+"/logs/"
        self.LOG_LEVEL="ERROR"
        self.JACKETT_API_LINK_LIST=[]
        self.ERROR_RETRY_SPAN=2
        self.REGULAR_CHECK_SPAN=6
        self.FILTER_DICTS={"default":{"reject_rules":["720"],"apply_rules":["1080"]}}
        self.other={}
        super().__init__()
        self.fetch()

    def fetch(self,file_path=CONFIG_FILE):
        if not os.path.exists(CONFIG_DIR):
            os.mkdir(CONFIG_DIR)
        if not os.path.exists(file_path):
            print(file_path)
            open(file_path, "w").close()
        with open(file_path,"r",encoding="utf8") as fp:
            try:
                paras_json = json.load(fp)
            except Exception:
                paras_json = ""
        if not paras_json:
            if not os.path.exists(self.LOG_DIR):
                os.mkdir(self.LOG_DIR)
                BaseLogger(self.LOG_DIR,self.LOG_LEVEL).error("No Valid Config, using default.")
            self.push(file_path)
        else:
            self.DB_PATH = paras_json.get('DB_PATH', self.DB_PATH)
            self.LOG_DIR = paras_json.get('LOG_DIR', self.LOG_DIR)
            self.LOG_LEVEL = paras_json.get('LOG_DIR', self.LOG_LEVEL)
            self.ERROR_RETRY_SPAN = tryParseInt(paras_json.get('ERROR_RETRY_SPAN', self.ERROR_RETRY_SPAN))
            self.REGULAR_CHECK_SPAN = tryParseInt(paras_json.get('REGULAR_CHECK__SPAN', self.REGULAR_CHECK_SPAN))
            self.ARIA2_RPC_SERVER = paras_json.get('ARIA2_RPC_SERVER', self.ARIA2_RPC_SERVER)
            self.ARIA2_JSONRPC_TOKEN = paras_json.get('ARIA2_JSONRPC_TOKEN', self.ARIA2_JSONRPC_TOKEN)
            self.JACKETT_API_LINK_LIST = paras_json.get('JACKETT_API_LINK_LIST', self.JACKETT_API_LINK_LIST)
            self.FILTER_DICTS = paras_json.get('FILTER_DICTS', self.FILTER_DICTS)
            self.other = paras_json.get('other',self.other)

    def push(self,file_path=CONFIG_FILE):
        with open(file_path, "w") as fp:
            paras_json = {
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
            json.dump(paras_json, fp)
            BaseLogger(self.LOG_DIR,self.LOG_LEVEL).info("Parameters are Saved.")

def tryParseInt(input:str)->int:
    try:
        return int(input)
    except ValueError:
        return 0
