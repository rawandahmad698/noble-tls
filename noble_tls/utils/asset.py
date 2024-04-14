import ctypes
import os
import platform
import sys
import distro


def root_dir():
    # Get the absolute path of the current file
    current_file_path = os.path.abspath(__file__)

    # Get the directory of the current file
    current_dir_path = os.path.dirname(current_file_path)

    # Navigate up one level to get the 'root_dir'
    root_dir = os.path.dirname(current_dir_path)
    return root_dir


def get_system_platform():
    return sys.platform


def get_distro():
    return distro.id()


def generate_asset_name(
        custom_part: str = 'tls-client',
        version: str = '1.7.4'
) -> str:
    """
    Generates an asset name based on the current platform and architecture, including handling for x86 architectures.

    :param custom_part: Custom part of the name specified by the user, e.g., 'tls-client'
    :param version: Version number specified by the user, e.g., '1.7.2'
    :return: Formatted asset name string
    """
    # Get the system's OS name and architecture
    system_os = platform.system().lower()
    architecture = platform.machine().lower()
    sys_platform = get_system_platform()

    # Correct the platform checks and architecture determination
    if sys_platform == 'darwin':
        file_extension = '.dylib'
        asset_arch = 'arm64' if architecture == "arm64" else 'amd64'
    elif sys_platform in ('win32', 'cygwin'):
        file_extension = '.dll'
        asset_arch = '64' if 8 == ctypes.sizeof(ctypes.c_voidp) else '32'

    else:
        # I don't possess a Linux machine to test this on, so I'm not sure if this is correct
        file_extension = '.so'

        if architecture == "aarch64":
            asset_arch = 'arm64'
        elif "x86" in architecture:
            asset_arch = 'amd64'
        else:
            asset_arch = 'amd64'

        if system_os == 'linux':
            distro_name = get_distro()
            if distro_name.lower() in {"ubuntu", "debian"}:
                system_os = f"{system_os}-ubuntu"

    return f"{custom_part}-{system_os}-{asset_arch}-{version}{file_extension}"


if __name__ == "__main__":
    # Example usage:
    custom_part = 'tls-client'
    version = '1.7.4'
    asset_name = generate_asset_name(custom_part, version)
    print(f">> Asset name: {asset_name}")
