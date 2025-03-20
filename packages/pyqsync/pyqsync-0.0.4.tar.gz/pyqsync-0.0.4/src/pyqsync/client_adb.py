import os
import shlex
import subprocess
import time
from difflib import SequenceMatcher
from typing import Tuple

from ppadb.client import Client as AdbClient
from ppadb.device import Device

from .base import FileTranferBase


def execute_command(cmd: str) -> Tuple[str, str]:
    process = subprocess.Popen(shlex.split(cmd), cwd=os.getcwd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode(), stderr.decode()


class AdbFileTransfer(FileTranferBase):
    "Local File Transfer Client"

    ostype = "adb"
    sep = "/"

    def __init__(self, callback=None, md5sum_progress=False) -> None:
        super().__init__(md5sum_progress=md5sum_progress)
        execute_command("adb devices")
        self.client = AdbClient(host="127.0.0.1", port=5037)
        self.device = self.client.devices()[0] if self.client.devices() else Device()  # If Device() it means eeror

        self._callback = callback if callback else lambda z, y, x: print(f"Transfered {x}b/{y}b", end="\r")

    def list(self, path: str, hidden=False) -> Tuple[dict, dict]:
        start_time = time.time()
        path = path[:-1] if path.endswith("/") else path
        command = f"ls -l{'A' if hidden else ''}p --full-time $PWD/"
        output = self.device.shell(f"cd {path};{command}")
        dirs, files = self._parse_dirs_files(output, platform="remote")

        diff = time.time() - start_time
        self.logger.debug(f"list took {diff:.2f} seconds")

        return dirs, files

    def list_tree(self, path: str, hidden=False, add_md5sum=False) -> Tuple[dict, dict]:
        start_time = time.time()
        path = path[:-1] if path.endswith("/") else path
        command = f"ls -l{'A' if hidden else ''}pR --full-time $PWD/"
        output = self.device.shell(f"cd {path};{command}")
        dirs, files = self._parse_dirs_files(output, platform="remote")

        diff = time.time() - start_time
        self.logger.debug(f"list_tree without md5sum took {diff:.2f} seconds")

        if add_md5sum == True:
            files = self._add_md5sum_to_files(files)

            diff = time.time() - start_time
            self.logger.debug(f"list_tree with md5sum took {diff:.2f} seconds")

        return dirs, files

    def normpath(self, path: str) -> str:
        return path.replace(os.sep, self.sep)

    def joinpath(self, *args) -> str:
        path = ""
        for i in args:
            path = os.path.join(path, os.path.normpath(i))
        return self.normpath(path)

    def md5sum(self, paths: str | list) -> str | list:
        single = False
        if isinstance(paths, str):
            paths = [paths]
            single = True

        paths = [self.normpath(path).replace("`", "\\`") for path in paths]

        command = ""
        for path in paths:
            command = command + f'"{path}" '
        command = f"md5sum " + command

        result = self.device.shell(command)

        checksums = []
        for line in result.split("\n"):
            if not line:
                continue
            checksum = line.split(" ")[0]
            if checksum.startswith("\\"):
                checksum = checksum[1:]
            checksums.append(checksum)

        if single:
            assert checksums[0]
            return checksums[0]

        assert len(paths) == len(checksums), "md5sum paths and checksums differ"

        return checksums

    def get(self, path_from: str, path_to: str):
        self.device.pull(path_from, path_to)

    def put(self, path_from: str, path_to: str):
        path_from = self._fix_missing_space_in_filename(path_from)
        self.device.push(path_from, path_to, progress=self._callback)

    def move(self, path_from: str, path_to: str):
        head, tail = os.path.split(path_to)
        return self.device.shell(f'mv "{path_from}" "{path_to}"')

    def remove(self, path):
        return self.device.shell(f'rm -rf "{path}"')

    def makedirs(self, path: str):
        return self.device.shell(f'mkdir -p "{path}"')

    def _fix_missing_space_in_filename(self, path_from: str) -> str:
        if not os.path.exists(path_from):
            head, tail = os.path.split(path_from)
            ratio = 0
            file_name = ""
            for name in os.listdir(head):
                temp_ratio = SequenceMatcher(None, name, tail).ratio()
                if temp_ratio > ratio:
                    ratio = temp_ratio
                    file_name = name
            path_from = os.path.join(head, file_name)
        return path_from


if __name__ == "__main__":
    REMOTE_PATH = "/storage/emulated/0"
    adb = AdbFileTransfer()
    x, y = adb.list_tree(REMOTE_PATH)
    print(adb.device.shell("echo $OSTYPE"))
    pass
