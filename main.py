import sqlite3
import loguru
from datetime import datetime, timedelta
import os
import json
from typing import overload, TypeVar
import random
import string
import requests
import re
import xml.etree.ElementTree
from tzlocal import get_localzone
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers import SchedulerNotRunningError, SchedulerAlreadyRunningError

from launcher import main

if __name__ == '__main__':
    while True:
        main()
