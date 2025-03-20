from http import HTTPStatus

import aiofiles
import httpx
from pydantic import BaseModel

from fitrequest.response_formatter import ResponseFormatter


class Response:
    def __init__(
        self,
        httpx_response: httpx.Response,
        raise_for_status: bool = True,
        json_path: str | None = None,
        response_model: type[BaseModel] | None = None,
    ) -> None:
        self.httpx_response = httpx_response

        if raise_for_status:
            self.handle_http_error()

        formatter = ResponseFormatter(
            httpx_response=httpx_response,
            json_path=json_path,
            response_model=response_model,
        )
        self.data = formatter.data
        self.data_bytes = formatter.data_bytes

    def handle_http_error(self) -> None:
        try:
            self.httpx_response.raise_for_status()
        except httpx.HTTPError as err:
            msg = self.httpx_response.text if self.httpx_response.content else ''

            if self.httpx_response.status_code == HTTPStatus.UNAUTHORIZED:
                msg += '\nMake sure settings are provided during initialization or set as environment variables.'
                msg = msg.strip()

            if not msg:
                raise
            raise httpx.HTTPStatusError(msg, request=self.httpx_response.request, response=self.httpx_response) from err

    def save_data(self, filepath: str, mode: str = 'xb') -> None:
        with open(filepath, mode=mode) as data_file:
            data_file.write(self.data_bytes)

    async def async_save_data(self, filepath: str, mode: str = 'xb') -> None:
        async with aiofiles.open(filepath, mode=mode) as data_file:
            await data_file.write(self.data_bytes)
