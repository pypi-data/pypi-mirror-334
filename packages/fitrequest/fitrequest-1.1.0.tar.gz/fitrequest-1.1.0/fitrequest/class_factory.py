import inspect
from collections.abc import Callable

from pydantic import BaseModel
from typing_extensions import Self

from fitrequest.cli_run import cli_app, cli_run
from fitrequest.fit_config import FitConfig
from fitrequest.generator import Generator
from fitrequest.method_config import MethodConfig, jinja_env
from fitrequest.request_params import extract_params
from fitrequest.session import Session
from fitrequest.utils import is_basemodel_subclass, string_varnames


class ClassFactory(type):
    """Metaclass to create new FitRequest classes."""

    @classmethod
    def get_return_pydantic_model(cls, cls_func: Callable) -> type[BaseModel] | None:
        """
        Inspects the function's return annotation and returns the corresponding Pydantic model
        if the annotation is supported by fitrequest.

        Supported annotation types:
        - list[BaseModel]
        - BaseModel
        """
        return_ann = inspect.get_annotations(cls_func, eval_str=True).get('return')

        if return_ann is None:
            return None

        if (
            hasattr(return_ann, '__origin__')
            and isinstance(return_ann.__origin__, type(list))
            and len(return_ann.__args__) == 1
            and isinstance(return_ann.__args__[0], type(BaseModel))
        ):
            return return_ann.__args__[0]

        if is_basemodel_subclass(return_ann):
            return return_ann

        return None

    @classmethod
    def handle_fit_decorator(cls, session: Session, cls_dict: dict) -> list[dict]:
        """
        Handle methods decorated with `@fit`. This function generates corresponding `fitrequest` methods
        and sets the `shared['generated_method']` attribute on each decorated method.
        The reason we cannot directly add the configuration to `method_config_list`
        is that there may be other decorators applied above `@fit`: any decorators above `@fit` would be ignored,
        leading to unexpected behavior.

        To address this, the `@fit` decorator has two roles:
        1. Marking the function as a "fit" method.
        2. Executing the generated method stored in `cls_func.shared['generated_method']`.

        The execution flow is as follows:
        1. The `@fit` decorator marks the function as a "fit" method.
        2. This function generates the corresponding `fitrequest` method and sets it in `shared['generated_method']`.
        3. The `@fit` decorator executes the generated method stored in `shared['generated_method']`.

        This function returns a list of configurations used to generate the fitrequest methods in a structured format
        (`MethodConfig dumps`).
        """

        config_list = []

        for cls_func in cls_dict.values():
            if not (callable(cls_func) and hasattr(cls_func, 'fit_decorator')):
                continue

            decorator = cls_func.fit_decorator.dump()
            endpoint_varnames = string_varnames(jinja_env, decorator['endpoint'])

            config = decorator | {
                'name': cls_func.__name__,
                'docstring': cls_func.__doc__ or cls_dict.get('method_docstring', ''),
                'base_url': decorator.get('base_url') or cls_dict.get('base_url'),
                'async_method': inspect.iscoroutinefunction(cls_func),
                'response_model': cls.get_return_pydantic_model(cls_func),
                'params_model': extract_params(cls_func, endpoint_varnames),
            }
            method_config = MethodConfig(**config)
            cls_func.shared['generated_method'] = Generator.generate_method(session, method_config)
            cls_func.__doc__ = method_config.docstring
            config_list.append(method_config.model_dump(exclude_none=True))

        return config_list

    def __new__(cls, cls_name: str, supers: tuple, cls_dict: dict) -> type:
        """Generate new class were all fitrequest methods were generated."""

        cls_dict['method_config_list'] = cls_dict.get('method_config_list', [])

        # Generated fitrequest config
        config = FitConfig(
            class_name=cls_name,
            class_docstring=cls_dict.get('__doc__', ''),
            client_name=cls_dict.get('client_name', 'fitrequest'),
            version=cls_dict.get('version', ''),
            method_docstring=cls_dict.get('method_docstring', ''),
            base_url=cls_dict.get('base_url'),
            auth=cls_dict.get('auth', {}),
            method_config_list=cls_dict.get('method_config_list'),
        )

        # Handle @fit decorators
        decorator_configs = cls.handle_fit_decorator(config.session, cls_dict)

        # Implement the fit_config property to expose the configuration utilized for creating the fitrequest methods.
        @property
        def fit_config(_: Self) -> dict:
            """Configuration used by fitrequest to generate the methods."""
            dump = config.model_dump(exclude_none=True)
            dump['method_config_list'] += decorator_configs
            dump['method_config_list'] = sorted(dump['method_config_list'], key=lambda x: x['name'])
            return dump

        # Remove attributes with no meaningful purpose after the client is instantiated
        cls_dict.pop('auth', None)
        cls_dict.pop('method_docstring', None)
        cls_dict.pop('method_config_list', None)

        # Create new type
        fit_attrs = (
            cls_dict
            | config.fit_methods
            | {
                'fit_config': fit_config,
                'session': config.session,
                'cli_app': cli_app,
                'cli_run': cli_run,
            }
        )
        new_class = super().__new__(cls, cls_name, supers, fit_attrs)
        new_class.__doc__ = config.class_docstring
        return new_class
