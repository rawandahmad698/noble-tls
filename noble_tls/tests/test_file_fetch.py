import pytest
from unittest.mock import AsyncMock

from ..exceptions.exceptions import TLSClientException
from ..updater.file_fetch import get_latest_release, download_and_save_asset, read_version_info, download_if_necessary

import pytest
from unittest.mock import MagicMock, patch
from ..updater.file_fetch import get_latest_release


@pytest.mark.asyncio
async def test_get_latest_release_success(mocker):
    # Mock the HTTP response from httpx.AsyncClient
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'tag_name': 'v1.0.0',
        'assets': [{'name': 'some_asset', 'browser_download_url': 'http://example.com/asset'}]
    }

    # Patch the httpx.AsyncClient.get method to return your mocked response
    with patch('httpx.AsyncClient.get', return_value=mock_response):
        version_num, assets = await get_latest_release()

    assert version_num == '1.0.0', "Version number should be parsed correctly"
    assert len(assets) > 0, "Assets list should not be empty"


@pytest.mark.asyncio
async def test_get_latest_release_failure(mocker):
    # Mock the HTTP response to simulate a failure
    mock_response = AsyncMock()
    mock_response.status_code = 404
    mocker.patch('httpx.AsyncClient.get', return_value=mock_response)

    with pytest.raises(TLSClientException):
        await get_latest_release()


def test_read_version_info(mocker):
    # Mock file reading operation
    mocker.patch('builtins.open', mocker.mock_open(read_data="some_asset 1.0.0"))

    asset_name, version = read_version_info()
    assert asset_name == 'some_asset'
    assert version == '1.0.0'


@pytest.mark.asyncio
async def test_download_if_necessary_no_download_needed(mocker):
    # Mock get_latest_release to return the current version
    mocker.patch('noble_tls.updater.file_fetch.get_latest_release',
                 return_value=('1.0.0',
                               [{'name': 'tls-client-darwin-arm64-1.7.2.dylib',
                                 'browser_download_url': 'https://google.com'}
                                ]))

    # Mock os.path.exists to simulate the asset already exists
    mocker.patch('os.path.exists', return_value=True)

    # The function should not attempt to download if the asset already exists
    await download_if_necessary()  # This should not raise
