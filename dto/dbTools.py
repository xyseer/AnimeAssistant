from GLOBAL_DEFINE import UNIFIED_TIME_FORMAT
from datetime import datetime
from typing import overload


def adapt_datetime(val: datetime):
    return val.strftime(UNIFIED_TIME_FORMAT)


@overload
def convert_datetime(val: bytes):
    return datetime.strptime(val.decode("utf8"), UNIFIED_TIME_FORMAT)


def convert_datetime(val: str):
    return datetime.strptime(val, UNIFIED_TIME_FORMAT)
