import pytest
from ..response import Response, build_response


def test_response_initialization():
    """Test the initialization and default values of the Response object."""
    response = Response()
    assert response.url is None
    assert response.status_code is None
    assert response.text is None
    assert response.history == []
    assert response.cookies is not None


def test_response_content_consumed():
    """Test that accessing the content after it's been consumed raises an error."""
    response = Response()
    response.text = "Hello, World!"
    response.status_code = 200

    # Access the content once to set _content and _content_consumed
    _ = response.content

    # Set _content back to None and _content_consumed to True to simulate consumed content
    response._content = None
    response._content_consumed = True

    with pytest.raises(RuntimeError):
        _ = response.content


def test_response_json_parsing():
    """Test the JSON parsing method."""
    response = Response()
    response.text = '{"message": "Hello, World!"}'
    json_data = response.json()

    assert json_data['message'] == "Hello, World!", "The message should be correctly parsed from the JSON text"


def test_build_response_function():
    """Test the build_response function."""
    res_data = {
        "target": "https://example.com",
        "status": 200,
        "body": '{"message": "Success"}',
        "headers": {"Content-Type": ["application/json"]}
    }
    res_cookies = None

    response = build_response(res_data, res_cookies)

    assert response.url == "https://example.com"
    assert response.status_code == 200
    assert response.text == '{"message": "Success"}'
    assert response.headers['Content-Type'] == "application/json"
    assert response.json()['message'] == "Success"
