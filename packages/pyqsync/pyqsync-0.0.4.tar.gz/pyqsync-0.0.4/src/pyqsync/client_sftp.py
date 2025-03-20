import functools
import io
import os
import time
from typing import Tuple

import paramiko
from paramiko import SSHException
from ytils.logger import SingletoneLogger

from .base import FileTranferBase


class ParamicoConnection:
    def __init__(self, user: str, host: str, port: int, password=None, pkey="") -> None:
        self.user = user
        self.host = host
        self.port = int(port)
        self.password = password

        if "RSA PRIVATE KEY" in pkey:
            self.pkey = paramiko.RSAKey.from_private_key(io.StringIO(pkey))
        else:
            pkey = os.path.expanduser(pkey)
            pkey = os.path.abspath(pkey)
            self.pkey = paramiko.Ed25519Key.from_private_key_file(pkey)
            # self.pkey = paramiko.RSAKey.from_private_key_file(pkey)

    def get(self) -> Tuple[paramiko.SSHClient, paramiko.SFTPClient]:
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.host, self.port, self.user, self.password, self.pkey)
        self.sftp = self.ssh.open_sftp()
        return self.ssh, self.sftp

    def close(self):
        self.sftp.close()
        self.ssh.close()

    def __enter__(self) -> Tuple[paramiko.SSHClient, paramiko.SFTPClient]:
        return self.get()

    def __exit__(self, *args, **kwargs):
        self.close()


class SFTPFileTransfer(FileTranferBase):
    """Secure File Transfer Clent"""

    ostype = "sftp"
    sep = "/"

    retry_attempts = 5

    def __init__(
        self, user: str, host: str, port: int, password=None, pkey="", callback=None, md5sum_progress=False
    ) -> None:
        """
        pkey: path to the rsa key or string as a content of the file
        callback: func that accepts 2 args (x, y) | x = tranfered bytes of y bytes

        Assumes that remote machine is always unix, so we use '/' for remote paths and '\\' or '/' for local machine
        """

        super().__init__(md5sum_progress=md5sum_progress)
        self.logging = SingletoneLogger("SFTPFileTransfer", level=10)

        self._user = user
        self._host = host
        self._port = port
        self._password = password
        self._pkey = pkey
        self._callback = callback if callback else lambda x, y: print(f"Transfered {x}b/{y}b", end="\r")

        self.connection = ParamicoConnection(user, host, port, password, pkey)
        (self.ssh, self.sftp) = self.connection.get()

    def fix_connection_timeout(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except SSHException as e:
                self.logger.debug(f"General SSHException: {e}")
                (self.ssh, self.sftp) = self.connection.get()
                return func(self, *args, **kwargs)

        return wrapper

    @fix_connection_timeout
    def list(self, remote_path: str, hidden=False) -> Tuple[dict, dict]:
        start_time = time.time()

        remote_path = remote_path[:-1] if remote_path.endswith("/") else remote_path
        command = f"ls -l{'A' if hidden else ''}p --full-time $PWD/"
        stdin, stdout, stderr = self.ssh.exec_command(f"cd {remote_path};{command}")
        output = stdout.read().decode()
        dirs, files = self._parse_dirs_files(output, platform="remote")

        diff = time.time() - start_time
        self.logging.debug(f"list took {diff:.2f} seconds")

        return dirs, files

    @fix_connection_timeout
    def list_tree(self, remote_path: str, hidden=False, add_md5sum=False) -> Tuple[dict, dict]:
        start_time = time.time()

        remote_path = remote_path[:-1] if remote_path.endswith("/") else remote_path
        command = f"ls -l{'A' if hidden else ''}pR --full-time $PWD/"
        stdin, stdout, stderr = self.ssh.exec_command(f"cd {remote_path};{command}")
        output = stdout.read().decode()
        dirs, files = self._parse_dirs_files(output, platform="remote")

        diff = time.time() - start_time
        self.logging.debug(f"list_tree without md5sum took {diff:.2f} seconds")

        if add_md5sum == True:
            files = self._add_md5sum_to_files(files)

            diff = time.time() - start_time
            self.logging.debug(f"list_tree with md5sum took {diff:.2f} seconds")

        return dirs, files

    def normpath(self, path: str) -> str:
        return path.replace(os.sep, self.sep)

    def joinpath(self, *args) -> str:
        path = ""
        for i in args:
            path = os.path.join(path, os.path.normpath(i))
        return self.normpath(path)

    @fix_connection_timeout
    def _md5sum(self, paths: str | list) -> str | list:
        single = False
        if isinstance(paths, str):
            paths = [paths]
            single = True

        paths = [self.normpath(path).replace("`", "\\`") for path in paths]

        command = ""
        for path in paths:
            command = command + f'"{path}" '
        command = f"md5sum " + command

        stdin, stdout, stderr = self.ssh.exec_command(command)
        stdout.channel.settimeout(60 * 5)  # 5 Minutes timeout
        try:
            result = stdout.read().decode()
        except TimeoutError:
            self.logging.debug(f"_md5sum timeout happened, retrying")
            return self._md5sum(paths)

        if not result:
            raise Exception(stderr.read().decode())

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

        """
        Reasons why assertion error can happen:
        1) Incorrect path syntax because of special symbols like "`"
        2) ssh connection broke and stdout returned for files that was processed
        
        for path in paths:
            if path not in result:
                print(path)
        """
        assert len(paths) == len(checksums), "md5sum paths and checksums differ"

        return checksums

    def md5sum(self, paths: str | list) -> str | list:
        try:
            return self._md5sum(paths)
        except AssertionError:
            """
            Perhaps it is temporary connection error
            If persists - lower amount of workers for ThreadPoolExecutor
            """
            return self._md5sum(paths)

    @fix_connection_timeout
    def get(self, path_from: str, path_to: str):
        for i in range(self.retry_attempts):
            try:
                self.sftp.get(path_from, path_to, self._callback)
                return True
            except Exception as e:
                self.logging.debug(f"RETRY ({i}): {e}")
                time.sleep(0.5)
                if i == self.retry_attempts - 1:
                    raise e

    @fix_connection_timeout
    def put(self, path_from: str, path_to: str):
        for i in range(self.retry_attempts):
            try:
                self.sftp.put(path_from, path_to, self._callback)
                return True
            except Exception as e:
                self.logging.debug(f"RETRY ({i}): {e}")
                time.sleep(0.5)
                if i == self.retry_attempts - 1:
                    raise e

    @fix_connection_timeout
    def move(self, path_from: str, path_to: str):
        for i in range(self.retry_attempts):
            try:
                self.sftp.rename(path_from, path_to)
                return True
            except Exception as e:
                self.logging.debug(f"RETRY ({i}): {e}")
                time.sleep(0.5)
                if i == self.retry_attempts - 1:
                    raise e

    @fix_connection_timeout
    def remove(self, path: str):
        for i in range(self.retry_attempts):
            try:
                self.sftp.remove(path)
                return True
            except Exception as e:
                self.logging.debug(f"RETRY ({i}): {e}")
                time.sleep(0.5)
                if i == self.retry_attempts - 1:
                    raise e

    @fix_connection_timeout
    def makedirs(self, path: str):
        stdin, stdout, stderr = self.ssh.exec_command(f'mkdir -p "{path}"')
        error = stderr.read().decode()
        assert not error, error
        pass


if __name__ == "__main__":
    pass
