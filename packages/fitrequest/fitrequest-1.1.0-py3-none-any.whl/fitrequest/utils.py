import inspect
import re
import types
from collections.abc import Callable
from typing import Any
from urllib.parse import parse_qs, urlparse

import httpx
import jinja2
import jinja2.meta
from pydantic import BaseModel

from fitrequest.errors import ReservedNamesError


def extract_method_params(method: Callable, params: dict) -> dict:
    """Return the parameters used in 'method' found in 'params'."""
    return {field: value for field, value in params.items() if field in inspect.signature(method).parameters}


def format_url(url: str) -> str:
    """Format url to remove redundant / character."""
    return re.sub(r'/+', '/', url).replace(':/', '://')


def string_varnames(jinja_env: jinja2.Environment, template: str) -> set[str]:
    """Extract named variables from template."""
    return jinja2.meta.find_undeclared_variables(jinja_env.parse(template))


def extract_url_params(url: str | None) -> tuple[str | None, dict]:
    """Extract url parameters and return the base url and it's parameters as dict."""
    if not url:
        return None, {}
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme + '://' if parsed_url.scheme else ''

    base_url = scheme + parsed_url.netloc + parsed_url.path
    params = parse_qs(parsed_url.query)

    return base_url, params


def is_basemodel_subclass(obj: Any) -> bool:
    """Return True if the provided object is a subclass of pydantic.BaseModel."""
    return (
        isinstance(obj, type)
        and type(obj) is not types.GenericAlias  # Added for python 3.10 support
        and issubclass(obj, BaseModel)
    )


#: Reserved ``fitrequest`` keywords that cannot be used as endpoint variables or URL parameters.
reserved_fitrequest_names = {'args', 'kwargs', 'raise_for_status', 'filepath'}


#: Reserved ``httpx`` keywords that cannot be used as endpoint variables or URL parameters.
reserved_httpx_names = set(inspect.signature(httpx.request).parameters)


def check_reserved_names(names: set[str]) -> set[str]:
    """
    Raises an error if a reserved name is used as an endpoint variable or request parameter in the generated method.
    Otherwise returns the provided names.
    """
    if bad_names := names.intersection({*reserved_httpx_names, *reserved_fitrequest_names}):
        raise ReservedNamesError(
            reserved_httpx_names=reserved_httpx_names,
            reserved_fitrequest_names=reserved_fitrequest_names,
            bad_names=bad_names,
        )
    return names
