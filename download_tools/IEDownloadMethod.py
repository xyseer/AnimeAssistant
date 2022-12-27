from dao.DownloadItem import DownloadItem


class IEDownloadMethod:
    def __init__(self, downloaditem: DownloadItem):
        self.downloaditem = downloaditem

    def __repr__(self):
        return self.__module__

    def download(self) -> bool:
        return False
