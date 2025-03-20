import concurrent.futures
import os
import sys
import time
from datetime import datetime
from pathlib import PurePosixPath
from typing import Tuple

from ytils.logger import SingletoneLogger

try:
    from rich.progress import Progress
except ImportError:
    print("Tip: pip install rich")


class FileTranferBase:
    ostype = ""
    sep = ""

    def __init__(self, md5sum_progress=False) -> None:
        self.logger = SingletoneLogger("FileTranferBase", level=10)
        self.md5sum_progress = md5sum_progress

    def md5sum(self, paths: str | list) -> str | list:
        raise NotImplementedError()

    def _add_md5sum_to_files(self, files: dict) -> dict:
        start_time = time.time()
        # Split list into chunks with n length
        n = 25
        paths = list(files.keys())
        chunks = [paths[i * n : (i + 1) * n] for i in range((len(paths) + n - 1) // n)]
        checksums = []

        # for chunk in chunks:
        #     checksums += self.md5sum(chunk)

        with concurrent.futures.ThreadPoolExecutor(4) as executor:
            futures = []
            for i, chunk in enumerate(chunks):

                def handler(chunk_var):
                    t = time.time()
                    result = self.md5sum(chunk_var)
                    # DEBUGGING
                    if False and self.md5sum_progress == True:
                        text = f"\nTOOK {chunk_var}\n{time.time() - t}s"
                        self.logger.debug(text)

                    return result

                # handler = lambda chunk_var: self.md5sum(chunk_var)
                future = executor.submit(handler, chunk)
                futures.append(future)

            if self.md5sum_progress == True and "rich" in sys.modules:
                with Progress() as progress:
                    task = progress.add_task("[cian]Progress...", total=len(futures))
                    i = 0
                    for future in concurrent.futures.as_completed(futures):
                        i += 1
                        progress.update(task, advance=1, description=f"{i}/{len(futures)}")
                        pass
            else:
                for future in concurrent.futures.as_completed(futures):
                    pass

            for future in futures:
                checksums += future.result()

        assert len(paths) == len(checksums), "Processed paths and checksums are differ"

        for i, key in enumerate(files.keys()):
            files[key]["md5sum"] = checksums[i]

        diff = time.time() - start_time
        self.logger.debug(f"_add_md5sum_to_files took {diff:.2f} seconds")

        return files

    def _parse_line(self, line: str) -> dict:
        file = {}
        splitted = line.replace("\\ ", " ").split()
        file["name"] = " ".join(splitted[8:])
        file["size"] = int(splitted[4])
        date = splitted[5]
        time = splitted[6][:-3]
        tz = splitted[7]
        file["dt"] = datetime.strptime(f"{date} {time}{tz}", "%Y-%m-%d %H:%M:%S.%f%z")
        return file

    def _parse_dirs_files(self, output: str, platform=sys.platform) -> Tuple[dict, dict]:
        """platform: required to differ local and remote systems"""
        dirs = {}
        files = {}
        parsed_output = output.strip().split("\n\n")
        dirs_files = [i.split("\n") for i in parsed_output]
        for block in dirs_files:
            path = block.pop(0).strip()[:-1]
            block.pop(0)
            for line in block:
                item = self._parse_line(line)
                item_path = str(PurePosixPath(path) / PurePosixPath(item["name"]))

                # Convert path to windows path
                if "win32" in platform:
                    path_split = [i for i in os.path.normpath(item_path).split(os.sep) if i]
                    if len(path_split[0]) == 1:
                        disk = path_split.pop(0).upper() + ":"
                        path_split.insert(0, disk)
                        item_path = os.sep.join(path_split)

                if item["name"].endswith("/"):
                    dirs[item_path] = item
                else:
                    files[item_path] = item
        return dirs, files
