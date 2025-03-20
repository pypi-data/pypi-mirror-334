import os
import platform
import shutil
import subprocess
import time
from typing import Tuple

from ytils.logger import SingletoneLogger

from .base import FileTranferBase


class LocalFileTransfer(FileTranferBase):
    "Local File Transfer Client"

    ostype = "local"
    sep = os.sep

    def __init__(self, md5sum_progress=False) -> None:
        """ """
        super().__init__(md5sum_progress=md5sum_progress)
        self.logger = SingletoneLogger("LocalFileTransfer", level=10)

    def list(self, local_path: str, hidden=False) -> Tuple[dict, dict]:
        start_time = time.time()

        local_path = os.path.normpath(local_path)
        local_path = local_path[:-1] if local_path.endswith(os.sep) else local_path
        p = subprocess.Popen("pwd", stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=local_path)
        stdout, stderr = p.communicate()
        pwd = stdout.decode().strip()
        if "Windows" in platform.platform():
            command = f'ls -l{"A" if hidden else ""}p --full-time "{pwd}"'
        else:
            command = ["ls", f"-l{'A' if hidden else ''}p", "--full-time", pwd]
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=local_path)
        stdout, stderr = p.communicate()
        if stderr:
            raise Exception(stderr.decode())

        dirs, files = self._parse_dirs_files(stdout.decode())

        diff = time.time() - start_time
        self.logger.debug(f"list took {diff:.2f} seconds")

        return dirs, files

    def list_tree(self, local_path: str, hidden=False, add_md5sum=False) -> Tuple[dict, dict]:
        start_time = time.time()

        local_path = os.path.normpath(local_path)
        local_path = local_path[:-1] if local_path.endswith(os.sep) else local_path
        p = subprocess.Popen("pwd", stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=local_path)
        stdout, stderr = p.communicate()
        pwd = stdout.decode().strip()
        if "Windows" in platform.platform():
            command = f'ls -l{"A" if hidden else ""}pR --full-time "{pwd}"'
        else:
            command = ["ls", f"-l{'A' if hidden else ''}pR", "--full-time", pwd]
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=local_path)
        stdout, stderr = p.communicate()
        if stderr:
            raise Exception(stderr.decode())

        dirs, files = self._parse_dirs_files(stdout.decode())

        diff = time.time() - start_time
        self.logger.debug(f"list_tree without md5sum took {diff:.2f} seconds")

        if add_md5sum == True:
            files = self._add_md5sum_to_files(files)

            diff = time.time() - start_time
            self.logger.debug(f"list_tree with md5sum took {diff:.2f} seconds")

        return dirs, files

    def normpath(self, path: str) -> str:
        return os.path.normpath(path)

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

        if "Windows" in platform.platform():
            command = ""
            for path in paths:
                command = command + f'"{path}" '
            command = f"md5sum " + command
        else:
            command = ["md5sum", *paths]
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.getcwd())
        stdout, stderr = p.communicate()
        if stderr:
            raise Exception(stderr.decode())
        result = stdout.decode()

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
        """Please use self.put(...)"""
        shutil.copy2(path_from, path_to)

    def put(self, path_from: str, path_to: str):
        shutil.copy2(path_from, path_to)

    def move(self, path_from: str, path_to: str):
        shutil.move(path_from, path_to)

    def remove(self, path: str):
        os.remove(path)

    def makedirs(self, path: str):
        os.makedirs(path, exist_ok=True)


if __name__ == "__main__":
    l = LocalFileTransfer()
    x = l.list_tree("mtp://Hisense_Hisense_6b6889f5/Internal%20shared%20storage/Literature/")  # Not working
    pass
