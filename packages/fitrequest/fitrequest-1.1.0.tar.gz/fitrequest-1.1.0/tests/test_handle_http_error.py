from unittest.mock import patch

import httpx
import pytest

from fitrequest.response import Response


def test_handle_http_error():
    httpx_response = httpx.Response(200)
    with patch.object(httpx_response, '_request'):
        try:
            Response(httpx_response=httpx_response).handle_http_error()
        except httpx.HTTPError:
            pytest.fail('Unexpected httpx.HTTPError raised')


def test_handle_response_raise_no_content():
    httpx_response = httpx.Response(404, content=b'')
    mock_url = 'mock.com'

    with (
        patch.object(httpx_response, '_request'),
        patch.object(httpx_response._request, 'url', mock_url),
        pytest.raises(httpx.HTTPError) as excinfo,
    ):
        Response(httpx_response=httpx_response).data

    assert excinfo.value.args[0] == (
        f"Client error '404 Not Found' for url '{mock_url}'\n"
        'For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404'
    )


def test_handle_response_raise_no_content_and_401():
    httpx_response = httpx.Response(401, content=b'')
    with patch.object(httpx_response, '_request'), pytest.raises(httpx.HTTPError) as excinfo:
        Response(httpx_response=httpx_response).data
    assert excinfo.value.args[0] == (
        'Make sure settings are provided during initialization or set as environment variables.'
    )


def test_handle_response_raise_with_content():
    httpx_response = httpx.Response(400, content=b'Custom error message')
    with patch.object(httpx_response, '_request'), pytest.raises(httpx.HTTPError) as excinfo:
        Response(httpx_response=httpx_response).data
    assert excinfo.value.args[0] == 'Custom error message'


def test_handle_response_raise_with_content_and_401():
    httpx_response = httpx.Response(401, content=b'Custom error message')

    with patch.object(httpx_response, '_request'), pytest.raises(httpx.HTTPError) as excinfo:
        Response(httpx_response=httpx_response).data
    assert excinfo.value.args[0] == (
        'Custom error message\nMake sure settings are provided during initialization or set as environment variables.'
    )
