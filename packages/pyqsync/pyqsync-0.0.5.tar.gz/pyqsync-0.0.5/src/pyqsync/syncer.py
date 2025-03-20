import concurrent.futures
import json
import logging
import os
import csv
import signal
from datetime import datetime, timedelta
from pathlib import Path
from typing import Tuple, Union

from ytils.converters import bytes_into_unit
from ytils.json import DateTimeEncoder, decode_datetime
from ytils.logger import SingletoneLogger
from ytils.perfomance import Profiler
from ytils.threads import ThreadWithResult

from .client_adb import AdbFileTransfer
from .client_lft import LocalFileTransfer
from .client_sftp import SFTPFileTransfer


def init_worker(*args, **kwargs):
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def callback(*args, **kwargs):
    if len(args) == 3:  # adb
        x = args[2]
        y = args[1]
    else:  # sftp
        x = args[0]
        y = args[1]
    dt = datetime.now().strftime("%H:%M:%S")
    print(f"{dt} Transfered {bytes_into_unit(x)}/{bytes_into_unit(y)}           ", end="\r")


class Syncer:
    """Sync files"""

    # TODO: Create functionality to copy .git files when move detected(no move)

    DIRS_IGNORE_MOVE = [".git"]  # TODO create ingore paramtere

    def __init__(
        self,
        local_client: LocalFileTransfer,
        remote_client: Union[LocalFileTransfer, SFTPFileTransfer, AdbFileTransfer],
        caching=False,
    ) -> None:
        """
        Assumes that remote machine is always unix, so we use '/' for remote paths and '\\' or '/' for local machine
        """
        self.LOCAL = local_client
        self.REMOTE = remote_client

        self.caching = caching

        self.logger = SingletoneLogger("Syncer", level=logging.DEBUG)
        self.profiler = Profiler(logger=self.logger)

    def _process_path_in_files(self, path: str, files: dict) -> Tuple[str, dict]:
        processed_path = path.replace("\\", "/")
        processed_files = {}
        for path, attr in files.items():
            processed_files[path.replace("\\", "/").replace(processed_path, "")] = attr

        return processed_path, processed_files

    def _process_paths(self, local_path: str, remote_path: str) -> Tuple[str, str]:
        local_path = self.LOCAL.normpath(local_path)
        local_path = local_path[:-1] if local_path.endswith(self.LOCAL.sep) else local_path
        local_path += self.LOCAL.sep

        remote_path = self.REMOTE.normpath(remote_path)
        remote_path = remote_path[:-1] if remote_path.endswith(self.REMOTE.sep) else remote_path
        remote_path += self.REMOTE.sep

        # lhead, ltail = os.path.split(local_path[:-1])
        # rhead, rtail = os.path.split(remote_path[:-1])
        # assert ltail == rtail, f"Local path and remote path directories differ: '{local_path}' '{remote_path}'"
        return local_path, remote_path

    def _write_cache(self, l_files: dict, r_files: dict):
        with open(".l_files.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(l_files, cls=DateTimeEncoder, ensure_ascii=False))
        with open(".r_files.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(r_files, cls=DateTimeEncoder, ensure_ascii=False))

    def _get_cache(self):
        with open(".l_files.json") as f:
            l_files = json.loads(f.read(), object_hook=decode_datetime)
        with open(".r_files.json") as f:
            r_files = json.loads(f.read(), object_hook=decode_datetime)

        return l_files, r_files

    def fetch(self, l_path: str, r_path: str, use_md5sum=True, use_cache=False) -> Tuple[dict, dict]:
        """
        move_local = True: If detected file move - files will be moved localy, otherwise remotely
        delete_local = True: delete local files if no such file on remote. False - delete remote files if no such file locally
        if_conflict = "ask" : Ask what to do with each conflict file or copy all left(all_l) or all right("all_r)
        """

        if use_cache == True:
            return self._get_cache()

        # l_dirs, l_files = self.LOCAL.list_tree(local_path, hidden=True, add_md5sum=True)
        # r_dirs, r_files = self.REMOTE.list_tree(remote_path, hidden=True, add_md5sum=True)

        t1 = ThreadWithResult(
            target=self.LOCAL.list_tree, args=(l_path,), kwargs={"hidden": True, "add_md5sum": use_md5sum}
        )
        t2 = ThreadWithResult(
            target=self.REMOTE.list_tree, args=(r_path,), kwargs={"hidden": True, "add_md5sum": use_md5sum}
        )
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        l_dirs, l_files = t1.result()
        r_dirs, r_files = t2.result()

        # with concurrent.futures.ThreadPoolExecutor(2) as executor:
        #     # local_future = executor.submit(
        #     #     self.LOCAL.list_tree, str(Path(local_path) / "Private" / "Literature"), hidden=True, add_md5sum=True
        #     # )
        #     # remote_future = executor.submit(
        #     #     self.REMOTE.list_tree, remote_path + "Private/Literature/", hidden=True, add_md5sum=True
        #     # )
        #     local_future = executor.submit(self.LOCAL.list_tree, l_path, hidden=True, add_md5sum=use_md5sum)
        #     remote_future = executor.submit(self.REMOTE.list_tree, r_path, hidden=True, add_md5sum=use_md5sum)

        #     for future in concurrent.futures.as_completed([local_future, remote_future]):
        #         pass

        #     l_dirs, l_files = local_future.result()
        #     r_dirs, r_files = remote_future.result()

        if self.caching:
            self._write_cache(l_files, r_files)

        return l_files, r_files

    def diff(
        self,
        l_path: str,
        r_path: str,
        l_files: dict,
        r_files: dict,
    ) -> list:
        l_path, l_files = self._process_path_in_files(l_path, l_files)
        r_path, r_files = self._process_path_in_files(r_path, r_files)

        diff_files = []

        # remote_files_copy = r_files.copy()
        use_md5sum = None
        for l_key, l_value in l_files.items():
            l_value["path"] = l_path + l_key
            l_value["stem"] = l_path
            l_value["suffix"] = l_key
            r_value = r_files.pop(l_key, None)

            if use_md5sum == None:
                if l_value.get("md5sum"):
                    use_md5sum = True
                else:
                    use_md5sum = False

            # Update exisitng files
            if r_value:
                r_value["path"] = r_path + l_key
                r_value["stem"] = r_path
                r_value["suffix"] = l_key
                # Detect if file changed
                if (use_md5sum and l_value["md5sum"] != r_value["md5sum"]) or (l_value["size"] != r_value["size"]):
                    diff_files.append((l_value, r_value))
                else:
                    pass  # Files are equal
            # Move moved files if move detected
            elif (
                (not any(f"/{d}/" in l_key for d in self.DIRS_IGNORE_MOVE))
                and (not Path(l_key).name.startswith("."))
                and (next((elem for elem in r_files.keys() if l_value["name"] in elem), None))
            ):
                pass
                for r_key_t, r_value_t in r_files.items():
                    # Check if file name and size desn't diff
                    if l_value["name"] in r_key_t and l_value["size"] == r_value_t["size"]:
                        # Doublecheck if files are the same using md5 checksum
                        if (use_md5sum and l_value["md5sum"] == r_value_t["md5sum"]) or (
                            self.LOCAL.md5sum(l_path + l_key) == self.REMOTE.md5sum(r_path + r_key_t)
                        ):
                            r_value_t["path"] = r_path + r_key_t
                            r_value_t["stem"] = r_path
                            r_value_t["suffix"] = r_key_t
                            diff_files.append((l_value, r_value_t))
                            r_files.pop(r_key_t, None)
                            break
                else:
                    diff_files.append((l_value, None))
                    # Upload new files if no move detected
            # Upload new files
            else:
                diff_files.append((l_value, None))

        # Download new files
        for r_key, r_value in r_files.items():
            r_value["path"] = r_path + r_key
            r_value["stem"] = r_path
            r_value["suffix"] = r_key
            diff_files.append((None, r_value))

        return diff_files

    def prepare_operations(
        self,
        l_path: str,
        r_path: str,
        diff_files: list,
        move_on: str,
        update_on: str,
        delete_on: str,
        ask_on_update_size_conflict: bool,
    ):
        pull = {}
        push = {}
        move_local = {}
        move_remote = {}
        delete_local = []
        delete_remote = []

        for local, remote in diff_files:
            if local and remote:
                if local["suffix"] != remote["suffix"]:  # Move / Rename
                    m = move_on
                    if m == "ask":
                        x = input(f"MOVE: '{local['path']}' '{remote['path']}' (l, r)")
                        if x == "l":
                            m = "local"
                        elif x == "r":
                            m = "remote"

                    if m == "local":
                        move_local[local["path"]] = local["stem"] + remote["suffix"]
                    elif m == "remote":
                        move_remote[remote["path"]] = remote["stem"] + local["suffix"]

                else:  # Update
                    u = update_on
                    if u == "auto":
                        if ask_on_update_size_conflict == True:
                            if local["dt"] > remote["dt"] and local["size"] > remote["size"]:
                                u = "remote"
                            elif local["dt"] < remote["dt"] and local["size"] < remote["size"]:
                                u = "local"
                            else:  # Newer but smaller. Can be caused by transfer interruption
                                print(
                                    f'!!! SIZE DIFF: LOCAL: {local["dt"]} size: {local["size"]}b || REMOTE: {remote["dt"]} size: {remote["size"]}b'
                                )
                                u = "ask"
                        else:
                            # Newer file
                            if local["dt"] > remote["dt"]:
                                u = "remote"
                            else:
                                u = "local"

                    if u == "ask":  # auto
                        x = input(f"UPDATE: '{local['path']}' '{remote['path']}' (l, r)")
                        if x == "l":
                            u = "local"
                        elif x == "r":
                            u = "remote"

                    if u == "local":
                        pull[remote["path"]] = local["stem"] + remote["suffix"]
                    elif u == "remote":
                        push[local["path"]] = remote["stem"] + local["suffix"]
            elif local:
                if delete_on == "local":
                    delete_local.append(local["path"])
                elif delete_on == "ask":
                    x = input(f"DELETE (else skip): '{local['path']}' (y, n)")
                    if x.lower() == "y":
                        delete_local.append(local["path"])
                elif delete_on == "skip":
                    pass
                else:  # sync
                    push[local["path"]] = r_path + local["suffix"]
            elif remote:
                if delete_on == "remote":
                    delete_remote.append(remote["path"])
                elif delete_on == "ask":
                    x = input(f"DELETE (else skip): '{remote['path']}' (y, n)")
                    if x.lower() == "y":
                        delete_remote.append(remote["path"])
                elif delete_on == "skip":
                    pass
                else:  # sync
                    pull[remote["path"]] = l_path + remote["suffix"]

        return (pull, push, move_local, move_remote, delete_local, delete_remote)

    def perform_operations(
        self, pull: dict, push: dict, move_local: dict, move_remote: dict, delete_local: list, delete_remote: list
    ):
        self.logger.info("Start: perform_operations")

        previous_dir = ""
        for key, value in pull.items():
            l_path = self.LOCAL.normpath(value)
            r_path = self.REMOTE.normpath(key)
            head, tail = os.path.split(l_path)
            if previous_dir != head:  # Reduce mkdir calls
                self.LOCAL.makedirs(head)
                previous_dir = head
            self.logger.info(f"PULL '{l_path}' to '{r_path}'")
            self.REMOTE.get(r_path, l_path)

        previous_dir = ""
        for key, value in push.items():
            l_path = self.LOCAL.normpath(key)
            r_path = self.REMOTE.normpath(value)
            head, tail = os.path.split(r_path)
            if previous_dir != head:  # Reduce mkdir calls
                self.REMOTE.makedirs(head)
                previous_dir = head
            self.logger.info(f"PUSH '{l_path}' to '{r_path}'")
            self.REMOTE.put(l_path, r_path)

        previous_dir = ""
        for key, value in move_local.items():
            l_path = self.LOCAL.normpath(key)
            r_path = self.LOCAL.normpath(value)
            head, tail = os.path.split(l_path)
            if previous_dir != head:  # Reduce mkdir calls
                self.LOCAL.makedirs(head)
                previous_dir = head
            self.logger.info(f"MOVE '{l_path}' to '{r_path}'")
            self.LOCAL.move(l_path, r_path)

        previous_dir = ""
        for key, value in move_remote.items():
            l_path = self.REMOTE.normpath(key)
            r_path = self.REMOTE.normpath(value)
            head, tail = os.path.split(r_path)
            if previous_dir != head:  # Reduce mkdir calls
                self.REMOTE.makedirs(head)
                previous_dir = head
            self.logger.info(f"MOVE '{l_path}' to '{r_path}'")
            self.REMOTE.move(l_path, r_path)

        for path in delete_local:
            l_path = self.LOCAL.normpath(path)
            self.logger.info(f"DELETE '{l_path}'")
            self.LOCAL.remove(l_path)

        for path in delete_remote:
            r_path = self.REMOTE.normpath(path)
            self.logger.info(f"DELETE '{r_path}'")
            self.REMOTE.remove(r_path)

        return True

    def diff_to_csv(self, local_path: str, remote_path: str, csv_path: str, use_md5sum=True):
        l_path, r_path = self._process_paths(local_path, remote_path)
        l_files, r_files = self.fetch(l_path=l_path, r_path=r_path, use_md5sum=use_md5sum, use_cache=False)
        diff_files = self.diff(l_path=l_path, r_path=r_path, l_files=l_files, r_files=r_files)

        with open(csv_path, mode="w", encoding="utf-8") as f:
            writer = csv.writer(f)
            headers = ["Status", "Local", "Remote"]
            writer.writerow(headers)
            for item in diff_files:
                row = []
                if item[0] and item[1]:
                    row.append("UPDATE")
                    data = {"path": item[0]["path"], "size": item[0]["size"], "dt": item[0]["dt"].isoformat()}
                    row.append(str(data))
                    data = {"path": item[1]["path"], "size": item[1]["size"], "dt": item[1]["dt"].isoformat()}
                    row.append(str(data))
                elif item[0]:
                    row.append("NEW")
                    data = {"path": item[0]["path"], "size": item[0]["size"], "dt": item[0]["dt"].isoformat()}
                    row.append(str(data))
                    row.append("=" * 40)
                elif item[1]:
                    row.append("NEW")
                    row.append("=" * 40)
                    data = {"path": item[1]["path"], "size": item[1]["size"], "dt": item[1]["dt"].isoformat()}
                    row.append(str(data))

                writer.writerow(row)

    def sync(
        self,
        local_path: str,
        remote_path: str,
        move_on="ask",
        update_on="ask",
        delete_on="ask",
        ask_on_update_size_conflict=True,
        use_md5sum=True,
        dry_run=False,
        use_cache=False,
    ):
        """
        move_on: "ask", "local", "remote", "skip"
        update_on: "ask", "local", "remote", "auto", "skip"
        delete_on: "ask", "local", "remote", "sync"(push and pull), "skip"
        """
        self.logger.info(f"START SYNC '{local_path}' AND '{remote_path}'")
        self.profiler.restart()

        l_path, r_path = self._process_paths(local_path, remote_path)

        l_files, r_files = self.fetch(l_path=l_path, r_path=r_path, use_md5sum=use_md5sum, use_cache=use_cache)

        self.profiler.trace("[sync] Fetch files")

        diff_files = self.diff(l_path=l_path, r_path=r_path, l_files=l_files, r_files=r_files)

        self.profiler.trace("[sync] Extract diff")

        pull, push, move_local, move_remote, delete_local, delete_remote = self.prepare_operations(
            l_path=l_path,
            r_path=r_path,
            diff_files=diff_files,
            move_on=move_on,
            update_on=update_on,
            delete_on=delete_on,
            ask_on_update_size_conflict=ask_on_update_size_conflict,
        )

        self.profiler.trace("[sync] Prepare operations")

        if dry_run == False:
            self.perform_operations(
                pull=pull,
                push=push,
                move_local=move_local,
                move_remote=move_remote,
                delete_local=delete_local,
                delete_remote=delete_remote,
            )

            self.profiler.trace("[sync] Perform operations")

        self.profiler.trace("[sync] Finish")
        self.logger.info("FINISH")
