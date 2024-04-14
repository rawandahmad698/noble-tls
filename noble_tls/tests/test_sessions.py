import asyncio

import pytest
from unittest.mock import patch, MagicMock
from ..sessions import Session
from ..utils.structures import CaseInsensitiveDict

import pytest
from unittest.mock import MagicMock, patch
from ..sessions import Session
import asyncio


@pytest.mark.asyncio
async def test_session_initialization():
    session = Session()
    assert session.timeout_seconds == 30, "Default timeout should be 30 seconds"
    assert isinstance(session.headers, CaseInsensitiveDict), "Headers should be a CaseInsensitiveDict"


@pytest.mark.asyncio
async def test_session_execute_request(mocker):
    # Mock external calls
    mocker.patch('ctypes.string_at', return_value=b'{"status": 200, "body": "OK", "headers": {}, "id": "mock_id"}')
    mocker.patch('ctypes.cdll.LoadLibrary')
    mocker.patch('noble_tls.sessions.free_memory')

    session = Session()

    # Prepare a mock response to be returned by the patched request function
    mock_response = '{"status": 200, "body": "OK", "headers": {}, "id": "mock_id"}'.encode('utf-8')

    # Mock asyncio loop
    mock_loop = MagicMock()
    mocker.patch('asyncio.get_event_loop', return_value=mock_loop)

    # Create a mock future object and set the result to the mock response
    mock_future = asyncio.Future()
    mock_future.set_result(mock_response)

    # Patch loop.run_in_executor to return the mock future
    mock_loop.run_in_executor = MagicMock(return_value=mock_future)

    # Execute a simple GET request
    response = await session.get('http://example.com')

    assert response.status_code == 200, "Response should have a status code of 200"
    assert response.text == 'OK', "Response body should be 'OK'"
