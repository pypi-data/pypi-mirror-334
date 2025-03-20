from collections.abc import Callable
from functools import reduce, wraps
from typing import Any

import httpx
from makefun import with_signature

from fitrequest.errors import UnrecognizedParametersError
from fitrequest.method_config import MethodConfig
from fitrequest.session import Session
from fitrequest.utils import extract_method_params


class Generator:
    @staticmethod
    def format_params(request_method: Callable, method_config: MethodConfig, **kwargs) -> dict:
        """Format and check params of generated method, raise on unrecognized arguments."""
        frozen_params = {'method_config': method_config}
        endpoint_params = {field: value for field, value in kwargs.items() if field in method_config.endpoint_varnames}

        # Params in method signature have priority over params in kwargs.
        url_params = {
            'params': (
                kwargs.get('params', {})
                | {field: value for field, value in kwargs.items() if field in method_config.params_varnames}
            )
        }

        # Filter out unknown args and freeze method_config argument
        request_method_params = (
            extract_method_params(httpx.request, kwargs)
            | extract_method_params(request_method, kwargs)
            | endpoint_params
            | frozen_params
            | url_params
        )
        if diff := set(kwargs).difference(request_method_params).difference({'self', *method_config.params_varnames}):
            raise UnrecognizedParametersError(
                method_name=method_config.name,
                unrecognized_arguments=diff,
            )
        return request_method_params

    @classmethod
    def generate_method(cls, session: Session, method_config: MethodConfig) -> Callable:
        """Generate method from configuration with correct signature."""
        # Add some common modules to makefun environment
        import datetime  # noqa: F401
        import enum  # noqa: F401
        import typing  # noqa: F401

        @with_signature(method_config.signature, doc=method_config.docstring)
        def generated_method(*args, **kwargs) -> Any:
            method_params = cls.format_params(session.request, method_config, **kwargs)
            return session.request(*args, **method_params)

        @with_signature(method_config.signature, doc=method_config.docstring)
        async def generated_async_method(*args, **kwargs) -> Any:
            method_params = cls.format_params(session.async_request, method_config, **kwargs)
            return await session.async_request(*args, **method_params)

        # Select between async/sync method, and apply decorators
        new_method = generated_async_method if method_config.async_method else generated_method
        new_method.fit_method = True
        decorators = reversed(method_config.decorators)
        return reduce(lambda func, decorator: wraps(func)(decorator(func)), [new_method, *decorators])
