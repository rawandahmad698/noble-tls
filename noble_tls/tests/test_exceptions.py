import pytest
from ..exceptions.exceptions import TLSClientException

def test_tls_client_exception():
    with pytest.raises(TLSClientException) as exc_info:
        raise TLSClientException("An error occurred")

    assert "An error occurred" in str(exc_info.value), "The message should be in the exception"
