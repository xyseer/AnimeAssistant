# ====================================================================
# Demo Function for importing new anime from xf.hmacg.cn excel file
# This MAY CAUSE INSTABILITY in previous implemented functions
# TAKE RISK if you enable this feature.
# ====================================================================
import json
import random
import string
from datetime import datetime, timedelta
import re

import requests

from parameters import Parameters
from logging_module import Logger
from GLOBAL_DEFINE import UNIFIED_TIME_FORMAT, STATIC_DIR
STATIC_DIR="../static"
from dao.DownloadItem import DownloadItem
from dto.dbTools import safe_filename
from PIL import Image
import io
import base64

MAGIC_SHEET_NUMBER = 1
MAGIC_START_INX = 4
MAGIC_STEP = 6
HMACG_TIME_FORMAT = "%m月%d日\n%H:%M"

def pil_image_to_base64(img: Image.Image, format='PNG') -> str:
    buffer = io.BytesIO()
    img.save(buffer, format=format)
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode('utf-8')

def processing_workbook_to_list(xlsx_path: str) -> list:
    import openpyxl
    from openpyxl_image_loader.sheet_image_loader import SheetImageLoader
    workbook = openpyxl.load_workbook(xlsx_path)
    sheet = workbook.worksheets[MAGIC_SHEET_NUMBER]
    column_d_values = [cell.value for cell in sheet['D']]
    image_loader = SheetImageLoader(sheet)
    info_list = []
    for idx in range(MAGIC_START_INX, len(column_d_values), MAGIC_STEP):
        if column_d_values[idx] is None:
            continue
        else:
            name = column_d_values[idx].split('\n')[0]
            description = sheet[f'E{idx + 1}'].value
            starttime = sheet[f'H{idx + 1}'].value
            totalep = 0
            tmp=re.findall(r"\d+",sheet[f'H{idx + (MAGIC_STEP - 1)}'].value)
            if tmp:
                totalep=int(tmp[0])
            image_base64 = ""
            try:
                image_pillow = image_loader.get(f'C{idx + 1}')
                image_base64=pil_image_to_base64(image_pillow)
            except ValueError:
                pass
            try:
                starttime_d = datetime.strptime(starttime, HMACG_TIME_FORMAT)
                starttime_d = starttime_d.replace(year=datetime.now().year)
                if (starttime_d + timedelta(days=90)) < datetime.now():
                    starttime_d = starttime_d.replace(year=datetime.now().year + 1)
            except ValueError:
                starttime_d = datetime.now()
            info_list.append({
                'name': name,
                'info': description,
                'starttime': starttime_d.strftime(UNIFIED_TIME_FORMAT),
                'lastUpdateTime': starttime_d.strftime(UNIFIED_TIME_FORMAT),
                'nextUpdateTime': starttime_d.strftime(UNIFIED_TIME_FORMAT),
                'totalEpisodes': totalep,
                'lasttUpdateEP': 0,
                'nextUpdateEP': 1,
                'img_base64': image_base64
            })
    return info_list

