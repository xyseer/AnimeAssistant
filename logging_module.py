from loguru import logger
from os import path

class BaseLogger:
    def __init__(self,log_dir:str,log_level:str):
        log_file=path.join(log_dir,"{time:YY-MM-DD}.log")
        self.logger=writelogger(log_file,log_level)
    def info(self,__message,*args,**kwargs):
        self.logger.info(__message,args,kwargs)
    def debug(self,__message,*args,**kwargs):
        self.logger.debug(__message,args,kwargs)
    def warning(self,__message,*args,**kwargs):
        self.logger.warning(__message,args,kwargs)
    def error(self,__message,*args,**kwargs):
        self.logger.error(__message,args,kwargs)
    def __del__(self):
        logger.remove()

def writelogger(log_file:str,log_level:str):
    logger.add(log_file,encoding="utf-8", rotation="00:00",retention="10 days",level=check_level_valid(log_level),format='<green>[{time:HH:mm:ss}]</green>[<cyan>{thread.name}</cyan>] <level>{level}</level>:<level>{message}</level>')
    return logger

def check_level_valid(loglevel:str):
    if not loglevel in ["INFO","DEBUG","ERROR","WARNING"]:
        return "DEBUG"
    else:
        return loglevel

class Logger(BaseLogger):
    def __init__(self):
        from parameters import Parameters
        p=Parameters()
        logger.remove()
        super().__init__(p.LOG_DIR,p.LOG_LEVEL)
        del p