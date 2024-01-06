import pytest
from ..utils.asset import root_dir, generate_asset_name


def test_root_dir():
    # Test that the root_dir function returns the expected path
    # This will be a simple test to check if the returned path ends with the correct folder name
    expected_part = 'noble_tls'  # Assuming the root directory name is 'NobleTLS'
    assert root_dir().endswith(expected_part)


def test_generate_asset_name_linux_amd64(mocker):
    mocker.patch('platform.system', return_value='Linux')
    mocker.patch('platform.machine', return_value='amd64')
    # Test that the asset name is correctly generated for Linux amd64
    expected_asset_name = 'tls-client-linux-amd64-v1.7.2.so'
    assert generate_asset_name() == expected_asset_name


def test_generate_asset_name_windows_x86(mocker):
    # Test that the asset name is correctly generated for Windows x86
    mocker.patch('platform.system', return_value='Windows')
    mocker.patch('platform.machine', return_value='i686')
    mocker.patch('platform.architecture', return_value=('32bit', ''))

    expected_asset_name = 'tls-client-windows-x86-v1.7.2-32.dll'
    assert generate_asset_name() == expected_asset_name


def test_generate_asset_name_macos_arm64(mocker):
    # Test that the asset name is correctly generated for macOS arm64
    mocker.patch('platform.system', return_value='Darwin')
    mocker.patch('platform.machine', return_value='arm64')

    expected_asset_name = 'tls-client-darwin-arm64-v1.7.2.dylib'
    assert generate_asset_name() == expected_asset_name


def test_generate_asset_name_unknown_architecture(mocker):
    # Test that the asset name is correctly generated for an unknown architecture
    mocker.patch('platform.machine', return_value='unknown_arch')
    mocker.patch('platform.system', return_value='darwin')

    expected_asset_name = 'tls-client-darwin-unknown-v1.7.2.dylib'
    assert generate_asset_name() == expected_asset_name

