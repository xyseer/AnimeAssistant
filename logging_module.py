from loguru import logger
from os import path
from pathlib import Path

class BaseLogger:
    def __init__(self, log_dir: str, log_level: str):
        log_file = path.join(log_dir, "{time:YY-MM-DD}.log")
        self.logger = writelogger(log_file, log_level)

    def info(self, __message, *args, **kwargs):
        self.logger.info(__message, args, kwargs)

    def debug(self, __message, *args, **kwargs):
        self.logger.debug(__message, args, kwargs)

    def warning(self, __message, *args, **kwargs):
        self.logger.warning(__message, args, kwargs)

    def error(self, __message, *args, **kwargs):
        self.logger.error(__message, args, kwargs)

    def __del__(self):
        logger.remove()


def writelogger(log_file: str, log_level: str):
    logger.add(log_file, encoding="utf-8", rotation="00:00", level=check_level_valid(log_level),
               format='<green>[{time:HH:mm:ss}]</green>[<cyan>{thread.name}</cyan>] <level>{level}</level>:<level>{message}</level>')
    return logger


def check_level_valid(loglevel: str):
    if not loglevel in ["INFO", "DEBUG", "ERROR", "WARNING"]:
        return "DEBUG"
    else:
        return loglevel


def delete_logs_on_schedule():
    from parameters import Parameters
    p = Parameters()
    log_retention = p.REGULAR_CHECK_SPAN
    log_dir = p.LOG_DIR
    log_files = sorted(
        Path(log_dir).glob("*.log"),
        key=lambda f: f.stat().st_mtime,
        reverse=True  # Newest first
    )
    if len(log_files)<log_retention:
        return
    else:
        del_count=0
        for old_file in log_files[log_retention:]:
            try:
                old_file.unlink()
                del_count+=1
            except Exception as e:
                Logger().error(f"[Log Retention]: Failed to delete {old_file.name}: {e}")
        Logger().info(f"[Log Retention]: Successfully removed {del_count} log files.")


class Logger(BaseLogger):
    def __init__(self):
        from parameters import Parameters
        p = Parameters()
        logger.remove()
        super().__init__(p.LOG_DIR, p.LOG_LEVEL)
        del p
