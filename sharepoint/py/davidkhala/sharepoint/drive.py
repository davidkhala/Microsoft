from os import PathLike
from typing import Callable, Any

from office365.onedrive.driveitems.driveItem import DriveItem
from office365.onedrive.drives.drive import Drive as RawDrive
import requests
from davidkhala.utils.syntax.fs import write


def recurse(item: DriveItem, prefix="", output_func: Callable[[str], Any] = print):
    children = item.children.get().execute_query()

    for child in children:
        if child.is_folder:
            new_prefix = f"{prefix}/{child.name}"
            output_func(new_prefix + "/")
            recurse(child, new_prefix)
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
        recurse(self._.root.get().execute_query(), f"{prefix}{self.name}")

    def download(self, relative_path: str, sink: PathLike):
        item = self._.root.get_by_path(relative_path).get().execute_query()

        download_url = item.properties.get(
            "@microsoft.graph.downloadUrl"
        )
        r = requests.get(download_url)
        write(sink, r.content, mode='wb')
