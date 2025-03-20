from typing import Any

import httpx
import pytest
import respx

from fitrequest.client import FitRequest
from fitrequest.decorators import fit
from fitrequest.errors import FitDecoratorInvalidUsageError


def test_decorator_without_class():
    @fit(endpoint='/item/{item_id}')
    def get_item(item_id: str) -> Any: ...

    with pytest.raises(FitDecoratorInvalidUsageError):
        get_item(item_id=5)


def test_decorator_without_fitrequest_inheritance():
    class RestApiClient:
        @fit(endpoint='/item/{item_id}')
        def get_item(self, item_id: str) -> Any: ...

    client = RestApiClient()
    with pytest.raises(FitDecoratorInvalidUsageError):
        client.get_item(item_id=5)


@respx.mock
def test_decorator_ok():
    item_id = 5
    expected = {'item_id': item_id, 'item_name': 'toto'}

    class RestApiClient(FitRequest):
        client_name = 'rest_api_client_test'
        base_url = 'https://test.skillcorner.fr/'

        @fit(endpoint='/item/{item_id}')
        def get_item(self, item_id: str) -> Any: ...

    respx.get(
        f'https://test.skillcorner.fr/item/{item_id}',
    ).mock(return_value=httpx.Response(200, json=expected))

    client = RestApiClient()
    response = client.get_item(item_id=item_id)
    assert response == expected


@pytest.mark.asyncio
async def test_async_decorator_without_class():
    @fit(endpoint='/item/{item_id}')
    async def get_item(item_id: str) -> Any: ...

    with pytest.raises(FitDecoratorInvalidUsageError):
        await get_item(item_id=5)


@pytest.mark.asyncio
async def test_async_decorator_without_fitrequest_inheritance():
    class RestApiClient:
        @fit(endpoint='/item/{item_id}')
        async def get_item(self, item_id: str) -> Any: ...

    client = RestApiClient()
    with pytest.raises(FitDecoratorInvalidUsageError):
        await client.get_item(item_id=5)


@respx.mock
@pytest.mark.asyncio
async def test_async_decorator_ok():
    item_id = 5
    expected = {'item_id': item_id, 'item_name': 'toto'}

    class RestApiClient(FitRequest):
        client_name = 'rest_api_client_test'
        base_url = 'https://test.skillcorner.fr/'

        @fit(endpoint='/item/{item_id}')
        async def get_item(self, item_id: str) -> Any: ...

    respx.get(
        f'https://test.skillcorner.fr/item/{item_id}',
    ).mock(return_value=httpx.Response(200, json=expected))

    client = RestApiClient()
    response = await client.get_item(item_id=item_id)
    assert response == expected


def test_docstring_priority():
    class RestApiClient(FitRequest):
        client_name = 'rest_api_client_test'
        base_url = 'https://test.skillcorner.fr/'
        method_docstring = 'Default docstring: {endpoint}'

        @fit(endpoint='/item/{item_id}')
        def get_item(self, item_id: str) -> Any: ...

        @fit(endpoint='/items')
        def get_items(self) -> Any:
            """Specific docstring: {endpoint}"""

    client = RestApiClient()
    assert client.get_item.__doc__ == 'Default docstring: /item/{item_id}'
    assert client.get_items.__doc__ == 'Specific docstring: /items'
