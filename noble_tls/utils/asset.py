import os
import platform


def root_dir():
    # Get the absolute path of the current file
    current_file_path = os.path.abspath(__file__)

    # Get the directory of the current file
    current_dir_path = os.path.dirname(current_file_path)

    # Navigate up one level to get the 'root_dir'
    root_dir = os.path.dirname(current_dir_path)
    return root_dir


def generate_asset_name(
        custom_part: str = 'tls-client',
        version: str = '1.7.2'
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

    # Common architecture names to the ones used in the assets
    arch_map = {
        'x86_64': 'amd64',
        'amd64': 'amd64',
        'arm64': 'arm64',
        'aarch64': 'arm64',
        'i386': 'x86',
        'i686': 'x86',
        'x86': 'x86'
    }

    # Check if we have a corresponding architecture in the map
    asset_arch = arch_map.get(architecture, 'unknown')

    # Determine file extension based on OS
    if system_os == 'darwin':  # macOS
        file_extension = '.dylib'
    elif system_os == 'windows':
        # Check pointer size to determine if the architecture is 64-bit or 32-bit
        file_extension = '-64.dll' if platform.architecture()[0] == '64bit' else '-32.dll'
    elif system_os == 'linux':
        file_extension = '.so'
        # Debian
        if 'debian' in platform.version().lower():
            system_os = 'debian'
    else:
        file_extension = '.so'  # Default to .so for other Unix-like systems

    # Handle special case for x86 architecture on non-Windows systems
    if system_os == 'darwin' and 'x86' in architecture:
        asset_arch = 'amd64'

    return f"{custom_part}-{system_os}-{asset_arch}-v{version}{file_extension}"


if __name__ == "__main__":
    # Example usage:
    custom_part = 'tls-client'
    version = '1.7.2'
    asset_name = generate_asset_name(custom_part, version)
    print(f">> Asset name: {asset_name}")
