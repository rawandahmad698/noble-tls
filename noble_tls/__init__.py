import asyncio
import os

from .updater.file_fetch import (
    download_if_necessary,
    update_if_necessary,
    get_latest_release,
    read_version_info
)
from .utils.asset import generate_asset_name
from .utils.asset import root_dir
from .utils.identifiers import Client
from .sessions import Session


# Huge thanks to:
# tls-client: https://github.com/bogdanfinn/tls-client
# requests: https://github.com/psf/requests
# tls-client: https://github.com/FlorianREGAZ/Python-Tls-Client
