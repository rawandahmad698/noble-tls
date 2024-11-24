from typing import Union, Dict, Any
import json
from .cookies import cookiejar_from_dict
from noble_tls.utils.structures import CaseInsensitiveDict
from typing import Optional
from requests.exceptions import HTTPError


class Response:
    """Represents the response to an HTTP request."""

    def __init__(self):
        self.url: Optional[str] = None
        self.status_code: Optional[int] = None  # The HTTP status code.
        self.text: Optional[str] = None  # The text content of the response.
        self.headers: CaseInsensitiveDict = CaseInsensitiveDict()  # Case-insensitive response headers.
        self.cookies = cookiejar_from_dict({})  # Cookies sent back by the server.
        self._content: Optional[bytes] = None  # The byte content of the response.
        self._content_consumed: bool = False  # Tracks if the content has been consumed.
        self.history = []

    def __enter__(self):
        return self

    def __repr__(self):
        return f"<Response [{self.status_code}]>"

    def json(self, **kwargs) -> Union[Dict, list]:
        """Parses the text content of the response to JSON."""
        return json.loads(self.text, **kwargs)

    def raise_for_status(self):
        """Raises an HTTPError if the HTTP request returned an unsuccessful status code."""
        if 400 <= self.status_code < 500:
            raise HTTPError(f'Client Error: {self.status_code} for url: {self.url}')
        elif 500 <= self.status_code < 600:
            raise HTTPError(f'Server Error: {self.status_code} for url: {self.url}')

    @property
    def content(self) -> bytes:
        """Lazily loads the content of the response, in bytes."""
        if self._content is None:
            if self._content_consumed:
                raise RuntimeError("The content for this response was already consumed.")
            self._content = self.text.encode() if self.status_code != 0 else b""
            self._content_consumed = True
        return self._content


def build_response(res: Dict[str, Any], res_cookies) -> Response:
    """Builds and returns a Response object from given data."""
    response = Response()
    response.url = res.get("target")  # Extract the target URL from the response data.
    response.status_code = res.get("status", 0)  # Default to 0 if status is not provided.
    response.text = res.get("body", "")  # Default to empty string if body is not provided.

    # Process headers, ensuring single values are not wrapped in a list.
    response_headers = CaseInsensitiveDict()
    for key, value in res.get("headers", {}).items():
        response_headers[key] = value[0] if len(value) == 1 else value
    response.headers = response_headers

    response.cookies = res_cookies  # Assign the provided cookies to the response.
    return response
