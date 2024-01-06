import asyncio
import os
import ctypes

from noble_tls.exceptions.exceptions import TLSClientException
from noble_tls.updater.file_fetch import read_version_info, download_if_necessary
from noble_tls.utils.asset import generate_asset_name, root_dir


async def check_and_download_dependencies():
    """
    Check if the dependencies folder is empty and download necessary files if it is.
    """
    root_directory = root_dir()
    contains_anything = [file for file in os.listdir(f'{root_directory}/dependencies') if not file.startswith('.')]
    if len(contains_anything) == 0:
        print(">> Dependencies folder is empty. Downloading the latest TLS release...")
        await download_if_necessary()


def run_async_task(task):
    """
    Run an asynchronous task taking into account the current event loop.
    :param task: Coroutine to run.
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(task)
    else:
        if loop.is_running():
            asyncio.ensure_future(task)
        else:
            loop.run_until_complete(task)


def load_asset():
    """
    Load the asset and return its name, download if necessary.
    :return: Name of the asset.
    """
    # Check if dependencies folder exists
    if not os.path.exists(f'{root_dir()}/dependencies'):
        os.mkdir(f'{root_dir()}/dependencies')

    current_asset, current_version = read_version_info()
    if not current_asset or not current_version:
        run_async_task(check_and_download_dependencies())
        current_asset, current_version = read_version_info()
        print(f">> Downloaded asset {current_asset} for version {current_version}.")

    asset_name = generate_asset_name(version=current_version)
    asset_path = f'{root_dir()}/dependencies/{asset_name}'
    if not os.path.exists(asset_path):
        raise TLSClientException(f"Unable to find asset {asset_name} for version {current_version}.")

    return asset_name


def initialize_library():
    """
    Initialize and return the library.
    :return: Loaded library object.
    """
    try:
        asset_name = load_asset()
        library = ctypes.cdll.LoadLibrary(f"{root_dir()}/dependencies/{asset_name}")
        return library
    except TLSClientException as e:
        print(f">> Failed to load the TLS Client asset: {e}")
    except OSError as e:
        print(f">> Failed to load the library: {e}")
        if os.name == "darwin":
            print(">> If you're on macOS, you need to allow the library to be loaded in System Preferences > Security & Privacy > General.")

        exit(1)


library = initialize_library()

# Define the request function from the shared package
request = library.request
request.argtypes = [ctypes.c_char_p]
request.restype = ctypes.c_char_p

free_memory = library.freeMemory
free_memory.argtypes = [ctypes.c_char_p]
free_memory.restype = ctypes.c_char_p
