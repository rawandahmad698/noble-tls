import pytest
from noble_tls.utils.asset import root_dir, generate_asset_name  # Update the import path as necessary

version = '1.7.4'


def test_root_dir():
    # Test that the root_dir function returns the expected path
    # This will be a simple test to check if the returned path ends with the correct folder name
    expected_part = 'noble_tls'  # Assuming the root directory name is 'NobleTLS'
    assert root_dir().endswith(expected_part)


def test_generate_asset_name_linux_amd64(mocker):
    mocker.patch('noble_tls.utils.asset.get_system_platform', return_value='linux')
    mocker.patch('platform.machine', return_value='x86_64')
    mocker.patch('platform.system', return_value='Linux')
    mocker.patch('ctypes.sizeof', return_value=8)  # This will simulate 64-bit architecture
    expected_asset_name = f'tls-client-linux-amd64-{version}.so'
    assert generate_asset_name() == expected_asset_name


def test_generate_asset_name_ubuntu_arm64(mocker):
    mocker.patch('noble_tls.utils.asset.get_system_platform', return_value='ubuntu')
    mocker.patch('noble_tls.utils.asset.get_distro', return_value='ubuntu')
    mocker.patch('platform.machine', return_value='x86_64')
    mocker.patch('platform.system', return_value='Linux')
    expected_asset_name = f"tls-client-linux-ubuntu-amd64-{version}.so"
    assert generate_asset_name() == expected_asset_name


def test_generate_asset_name_windows_x86(mocker):
    mocker.patch('noble_tls.utils.asset.get_system_platform', return_value='win32')
    mocker.patch('platform.system', return_value='Windows')
    mocker.patch('platform.machine', return_value='i686')
    mocker.patch('ctypes.sizeof', return_value=4)  # This will simulate 32-bit architecture
    expected_asset_name = f'tls-client-windows-32-{version}.dll'
    assert generate_asset_name() == expected_asset_name


def test_generate_asset_name_macos_arm64(mocker):
    mocker.patch('noble_tls.utils.asset.get_system_platform', return_value='darwin')
    mocker.patch('platform.system', return_value='Darwin')
    mocker.patch('platform.machine', return_value='arm64')
    expected_asset_name = f'tls-client-darwin-arm64-{version}.dylib'
    assert generate_asset_name() == expected_asset_name


def test_generate_asset_name_unknown_architecture(mocker):
    mocker.patch('noble_tls.utils.asset.get_system_platform', return_value='linux')
    mocker.patch('platform.system', return_value='Linux')
    mocker.patch('platform.machine', return_value='unknown_arch')
    mocker.patch('ctypes.sizeof', return_value=8)  # Assuming 64-bit for an unknown architecture
    expected_asset_name = f'tls-client-linux-amd64-{version}.so'
    assert generate_asset_name() == expected_asset_name
