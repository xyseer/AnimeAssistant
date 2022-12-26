from GLOBAL_DEFINE import UNIFIED_TIME_FORMAT
from datetime import datetime
from typing import overload
from dto.SqliteDB import DBManipulator


def adapt_datetime(val: datetime):
    return val.strftime(UNIFIED_TIME_FORMAT)


@overload
def convert_datetime(val: bytes):
    return datetime.strptime(val.decode("utf8"), UNIFIED_TIME_FORMAT)


def convert_datetime(val: str):
    return datetime.strptime(val, UNIFIED_TIME_FORMAT)

def listTostr(l:list,sep:str=";"):
    result=""
    for x in l[0:-1]:
        result+=x+sep
    result+=l[-1]
    return result
def strTolist(s:str,sep:str=";"):
    result = s.split(";")
    result.remove("") if "" in result else result
    return result

def getValidID():
    ss=DBManipulator()
    seq_tuple=ss.get_cursor().execute("SELECT seq FROM sqlite_sequence WHERE name='nameTable'").fetchone()
    if not seq_tuple:
        seq=1
    else:
        seq=seq_tuple[0]
    return seq