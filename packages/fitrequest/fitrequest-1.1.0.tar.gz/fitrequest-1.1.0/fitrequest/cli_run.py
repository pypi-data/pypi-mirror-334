import asyncio
import inspect
import json
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Annotated, Any, Literal

import makefun
import rich
import typer
from httpx import HTTPError
from pydantic.alias_generators import to_pascal
from strenum import StrEnum

from fitrequest.errors import FitRequestConfigurationError, FitRequestRuntimeError, UnexpectedLiteralTypeError


def run_pretty(func: Callable) -> Callable:
    """
    Simplify running fitrequest methods from the CLI, supporting both synchronous and asynchronous functions.
    The results are pretty-printed using 'rich' for enhanced readability.
    """

    def wrapper(*args, **kwargs) -> None:
        try:
            results = asyncio.run(func(*args, **kwargs)) if inspect.iscoroutinefunction(func) else func(*args, **kwargs)
        except (FitRequestConfigurationError, FitRequestRuntimeError, HTTPError) as err:
            rich.print(err)
            sys.exit(1)

        rich.print(results)

    # Remove **kwargs argument if it exists
    try:
        signed_wrapper = makefun.wraps(func, remove_args=['kwargs'])(wrapper)
    except KeyError:
        signed_wrapper = makefun.wraps(func)(wrapper)
    return signed_wrapper


def add_httpx_args(func: Callable) -> Callable:
    """
    If the signature does not already include these arguments, the function adds some common ``httpx`` parameters.
    These parameters will then be accessible via the CLI.
    They are added only if ``kwargs`` is included in the method's signature.
    """
    old_signature = inspect.signature(func)

    # Current signature doesn't allow httpx kwargs.
    if 'kwargs' not in old_signature.parameters:
        return func

    httpx_params = [
        inspect.Parameter(
            name=name,
            annotation=Annotated[ann, typer.Option(help=desc)],
            default=None,
            kind=inspect.Parameter.KEYWORD_ONLY,
        )
        for ann, name, desc in [
            (Path | None, 'content', 'Path to binary content.'),
            (Path | None, 'data', 'Path to Json file.'),
            (Path | None, 'json', 'Path to Json file. Sets "Content-Type" to "application/json".'),
        ]
        if name not in old_signature.parameters
    ]

    new_parameters = sorted([*old_signature.parameters.values(), *httpx_params], key=lambda p: p.kind)
    new_signature = old_signature.replace(parameters=new_parameters)

    # Only handle arguments added by @add_httpx_args
    def handle_httpx_params(kwargs: dict) -> dict:
        # Read "content" as binary file
        if 'content' not in old_signature.parameters and (source_path := kwargs.get('content')):
            with open(str(source_path), mode='rb') as source_file:
                kwargs['content'] = source_file.read()

        # Read "data", "json" as json files
        for httpx_arg in ['data', 'json']:
            if httpx_arg in old_signature.parameters:
                continue

            if source_path := kwargs.get(httpx_arg):
                with open(str(source_path)) as source_file:
                    kwargs[httpx_arg] = json.load(source_file)
        return kwargs

    @makefun.wraps(func, new_sig=new_signature)
    def wrapper(*args, **kwargs) -> None:
        return func(*args, **handle_httpx_params(kwargs))

    @makefun.wraps(func, new_sig=new_signature)
    async def async_wrapper(*args, **kwargs) -> None:
        return await func(*args, **handle_httpx_params(kwargs))

    return async_wrapper if inspect.iscoroutinefunction(func) else wrapper


def transform_literals(func: Callable) -> Callable:
    """
    Unfortunatly typer doesn't support literals, this decorator transform all literals in signature to enums.
    """
    signature = inspect.signature(func)
    signature_params = signature.parameters.copy()
    new_params = []

    for params in signature_params.values():
        if not getattr(params.annotation, '__origin__', None):
            new_params.append(params)
            continue
        enum_name = to_pascal(f'{params.name}Enum')
        updated_param = params.replace(annotation=literal_to_enum(enum_name, params.annotation))
        new_params.append(updated_param)

    new_signature = signature.replace(parameters=new_params)
    return makefun.create_function(func_signature=new_signature, func_impl=func)


def literal_to_enum(name: str, literal: type[Literal]) -> type[StrEnum]:
    """
    Create an Enum dynamically.
    """
    if not hasattr(literal, '__args__'):
        raise UnexpectedLiteralTypeError(bad_type=literal)

    return StrEnum(name, {val: val for val in literal.__args__})


@classmethod
def cli_app(cls: Any) -> typer.Typer:
    """
    Set up a CLI interface using Typer.
    Instantiates the fitrequest client, registers all its methods as commands, and returns the typer the application.
    """
    app = typer.Typer()
    client = cls()

    for attr_name in dir(client):
        attr = getattr(client, attr_name)

        if callable(attr) and (getattr(attr, 'fit_method', False) or getattr(attr, 'cli_method', False)):
            app.command()(run_pretty(add_httpx_args(transform_literals(attr))))
    return app


@classmethod
def cli_run(cls: Any) -> None:
    """
    Runs the typer application.
    """
    cls.cli_app()()
