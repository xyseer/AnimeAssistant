from dto import dbTools
from dao.dataItems import *
from download_tools.IEDownloadMethod import IEDownloadMethod
from datetime import datetime, timedelta
from parameters import Parameters
from logging_module import Logger
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers import SchedulerNotRunningError, SchedulerAlreadyRunningError
from tzlocal import get_localzone


class SubscribeCore:
    def __init__(self):
        self.download_items = dbTools.getDownloadItems()
        self.scheduler = BackgroundScheduler(timezone=str(get_localzone()) if get_localzone()!=None else "UTC")
        self.remap_scheduler()

    def _fetch_items(self):
        self.download_items = dbTools.getDownloadItems()

    def remap_scheduler(self):
        self._fetch_items()
        self.shutdown_scheduler()
        self.scheduler.remove_all_jobs()
        p = Parameters()
        self.scheduler.add_job(self.remap_scheduler, "interval", hours=p.REGULAR_CHECK_SPAN,id="remap_scheduler")
        for i in self.download_items:
            if i.nextUpdateTime < datetime.now():
                self.scheduler.add_job(self._check_update_done, args=[i],id=str(i.id))
            else:
                self.scheduler.add_job(self._check_update_done, "date", run_date=i.nextUpdateTime, args=[i],id=str(i.id))
        self.start_scheduler()

    def _check_update_done(self, download_item: DownloadItem, times: int = 1):
        if times <= 0:
            return
        p = Parameters()
        if self.single_item_subscribe(download_item):
            if p.REGULAR_CHECK_SPAN > download_item.span:
                self.remap_scheduler()
                return
            else:
                return
        else:
            if times <= 5:
                span_minutes = 1 if int(p.ERROR_RETRY_SPAN * 60 / times) <= 0 else int(p.ERROR_RETRY_SPAN * 60 / times)
                self.scheduler.add_job(self._check_update_done, "date",
                                       run_date=datetime.now() + timedelta(minutes=span_minutes),
                                       args=[download_item, times + 1],id=f"{download_item.id}_retry_{times+1}")
                Logger().warning(
                    f"Subscription {download_item.name} has failed for {times} times. Please check the infos are all correct.")
                return
            else:
                span = int(p.ERROR_RETRY_SPAN * 20)
                Logger().error(
                    f"Subscription {download_item.name} has error fetched for 5 times. This Subscription forced to delay for {span} hours.")
                download_item.nextUpdateTime = download_item.nextUpdateTime + timedelta(hours=span)
                download_item.push()
                return

    def shutdown_scheduler(self):
        try:
            self.scheduler.shutdown()
        except SchedulerNotRunningError:
            pass

    def start_scheduler(self):
        try:
            self.scheduler.start()
        except SchedulerAlreadyRunningError:
            self.shutdown_scheduler()
            self.scheduler.start()

    def __del__(self):
        self.shutdown_scheduler()

    @staticmethod
    def get_type_downloader(download_item: DownloadItem) -> IEDownloadMethod:
        type_name = download_item.type
        if len(type_name.split(".")) < 2:
            type_name = "download_tools." + type_name
        class_name = type_name.split(".")[-1]
        try:
            return getattr(getattr(__import__(type_name), class_name, IEDownloadMethod), class_name, IEDownloadMethod)(
            download_item)
        except ModuleNotFoundError or AttributeError:
            Logger().error(f"{download_item.type} Not Found. Please check the extensions.")
            return IEDownloadMethod(download_item)

    @staticmethod
    def single_item_subscribe(download_item: DownloadItem) -> bool:
        is_download_success = SubscribeCore.get_type_downloader(download_item).download()
        if is_download_success:
            download_item.nextUpdateTime = download_item.nextUpdateTime + timedelta(hours=download_item.span)
            download_item.lastUpdateTime = datetime.now()
            download_item.lastUpdateEP = download_item.nextUpdateEP
            download_item.nextUpdateEP += 1
            download_item.push()
            return True
        return False
