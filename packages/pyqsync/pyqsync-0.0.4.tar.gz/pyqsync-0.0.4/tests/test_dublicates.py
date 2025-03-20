import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import logging
import os
import time

from ytils.dotenv import load_dotenv
from ytils.logger import SingletoneLogger

from src.pyqsync.client_adb import AdbFileTransfer
from src.pyqsync.client_lft import LocalFileTransfer
from src.pyqsync.client_sftp import SFTPFileTransfer
from src.pyqsync.dubs import Dubs

load_dotenv()


if __name__ == "__main__":
    user = os.environ.get("USER").replace("\r", "")
    host = os.environ.get("HOST").replace("\r", "")
    port = os.environ.get("PORT").replace("\r", "")
    rsa_key = os.environ.get("RSA_KEY").replace("\r", "")
    local_path = os.environ.get("LOCAL_PATH").replace("\r", "")
    remote_path = os.environ.get("REMOTE_PATH").replace("\r", "")

    # local_client = LocalFileTransfer()
    remote_client = AdbFileTransfer(md5sum_progress=True)
    # remote_client = SFTPFileTransfer(
    #     user=user,
    #     host=host,
    #     port=port,
    #     password=None,
    #     pkey=rsa_key,
    #     # callback=callback,
    #     md5sum_progress=True,
    # )

    dubs = Dubs(remote_client)
    dubs.filter("/storage/emulated/0/Literature", by_md5sum=True)
    pass
