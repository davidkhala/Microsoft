from os import PathLike
from typing import Callable, Any

from office365.onedrive.driveitems.driveItem import DriveItem
from office365.onedrive.drives.drive import Drive as RawDrive
from office365.runtime.client_request_exception import ClientRequestException
import requests
from davidkhala.utils.syntax.fs import write


def recurse(item: DriveItem, prefix="", output_func: Callable[[str], Any] = print):
    children = item.children.get().execute_query()

    for child in children:
        if child.is_folder:
            new_prefix = f"{prefix}/{child.name}"
            output_func(new_prefix + "/")
            try:
                recurse(child, new_prefix)
            except ClientRequestException as e:
                if e.code != "BadRequest":
                    # Known issue: SharePoint 中 Viva Engage 会在 Documents 库里创建特殊的隐藏文件夹，这类文件夹在 SDK 的 children 列表里可见（is_folder=True），但实际去读取其子项时 Graph API 会拒绝。
                    raise
        else:
            output_func(f"{prefix}/{child.name}")


class Drive:
    def __init__(self, drive: RawDrive):
        self._ = drive
        self._.get().execute_query()

    @property
    def id(self):
        return self._.id

    @property
    def name(self):
        return self._.name

    def tree(self, prefix=""):
        recurse(self.get(), f"{prefix}{self.name}")

    def get(self, path="") -> DriveItem:
        if not path:
            return self._.root.get().execute_query()
        else:
            return self._.root.get_by_path(path).get().execute_query()

    def download(self, relative_path: str, sink: PathLike):
        item = self.get(relative_path)

        download_url = item.properties.get("@microsoft.graph.downloadUrl")
        r = requests.get(download_url)
        write(sink, r.content, mode='wb')

    def upload(self, source: PathLike, sink_dir="") -> DriveItem:
        item = self.get(sink_dir)
        return item.upload_file(source).execute_query()
