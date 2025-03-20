import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Tuple, Union

from ytils.logger import SingletoneLogger
from ytils.perfomance import Profiler

from .client_adb import AdbFileTransfer
from .client_lft import LocalFileTransfer
from .client_sftp import SFTPFileTransfer


class Dubs:
    """Find and remove dublicates"""

    IGNORE_DIRS = [".git"]  # TODO create ingore paramtere

    def __init__(
        self,
        client: Union[LocalFileTransfer, SFTPFileTransfer, AdbFileTransfer],
    ) -> None:
        """
        Assumes that remote machine is always unix, so we use '/' for remote paths and '\\' or '/' for local machine
        """
        self.CLIENT = client

        self.logger = SingletoneLogger("Syncer", level=logging.DEBUG)
        self.profiler = Profiler(logger=self.logger)

    def _process_path_in_files(self, path: str, files: dict) -> Tuple[str, dict]:
        processed_path = path.replace("\\", "/")
        processed_files = {}
        for path, attr in files.items():
            processed_files[path.replace("\\", "/").replace(processed_path, "")] = attr

        return processed_path, processed_files

    def _process_path(self, path: str) -> str:
        path = self.CLIENT.normpath(path)
        path = path[:-1] if path.endswith(self.CLIENT.sep) else path
        path += self.CLIENT.sep
        return path

    def fetch(self, path: str, use_md5sum=True) -> dict:
        dirs, files = self.CLIENT.list_tree(path, hidden=True, add_md5sum=use_md5sum)

        return files

    def filter_by_name(self, files: dict) -> dict:
        counter = {}
        for key, value in files.items():
            if counter.get(value["name"]):
                value["path"] = key
                counter[value["name"]].append(value)
            else:
                value["path"] = key
                counter[value["name"]] = [value]

        dubs = {}
        for key, value in counter.items():
            if len(value) > 1:
                dubs[key] = value

        return dubs

    def filter_by_md5sum(self, files: dict) -> dict:
        counter = {}
        for key, value in files.items():
            if "md5sum" in value["md5sum"]:
                continue  # SOME ISSUE THAT SHOULD BE INVESTIGATED

            if counter.get(value["md5sum"]):
                value["path"] = key
                counter[value["md5sum"]].append(value)
            else:
                value["path"] = key
                counter[value["md5sum"]] = [value]

        dubs = {}
        for key, value in counter.items():
            if len(value) > 1:
                dubs[key] = value

        return dubs

    def prepare_operations(self, dubs: dict, on_delete="ask") -> list:
        delete = []
        for key, value in dubs.items():
            print("=" * 10)
            for i, item in enumerate(value):
                print(f"{i + 1}) '{item['path']}'")
            if on_delete == "ask":
                x = input("Which one to leave? ")
                try:
                    value.pop(int(x) - 1)
                    delete.extend(value)
                except Exception as e:
                    pass
            elif on_delete == "auto":
                newer = None
                for item in value:
                    if not newer:
                        newer = item
                        continue
                    if newer["dt"] < item["dt"]:
                        newer = item
                value.remove(newer)
                delete.extend(value)

        return delete

    def perform_operations(self, delete: list):
        for file in delete:
            self.logger.info(f"REMOVE: '{file}'")
            self.CLIENT.remove(file)

    def filter(self, path: str, *, by_name=False, by_size=False, by_md5sum=False, on_delete="ask"):
        """
        _summary_

        Args:
            path (str): _description_
            by_name (bool, optional): _description_. Defaults to False.
            by_size (bool, optional): _description_. Defaults to False.
            by_md5sum (bool, optional): _description_. Defaults to False.
            action (str, optional): What to do with dublicates: ask, auto. Defaults to "ask".

        Returns:
            _type_: _description_
        """
        assert by_name or by_size or by_md5sum

        self.logger.info(f"START DUBS '{path}'")
        self.profiler.restart()

        path = self._process_path(path)

        files = self.fetch(path, use_md5sum=by_md5sum)

        self.profiler.trace("[dubs] Fetch files")

        path, files = self._process_path_in_files(path, files)

        if by_name:
            dubs = self.filter_by_name(files)
        elif by_md5sum:
            dubs = self.filter_by_md5sum(files)

        self.profiler.trace("[dubs] Filter files")

        delete = self.prepare_operations(dubs, on_delete=on_delete)

        self.profiler.trace("[dubs] Prepare operations")

        self.perform_operations(delete)

        self.profiler.trace("[dubs] Perform operations")

        self.profiler.trace("[dubs] Finish")
