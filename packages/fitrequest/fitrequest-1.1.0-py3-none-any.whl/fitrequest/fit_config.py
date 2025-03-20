from collections.abc import Callable
from functools import cached_property

from pydantic import ConfigDict
from typing_extensions import Self

from fitrequest.cli_run import cli_app, cli_run
from fitrequest.generator import Generator
from fitrequest.method_config import MethodConfig
from fitrequest.method_config_group import MethodConfigGroup
from fitrequest.session import Session


class FitConfig(MethodConfigGroup):
    """
    Fitrequest configuration model.
    Describes all information needed to generate Fitrequest's class and methods.
    """

    class_name: str = 'FitRequest'
    """Name of the the generated class."""

    class_docstring: str = ''
    """Docstring of the generated class."""

    model_config = ConfigDict(extra='forbid', validate_default=True)

    @cached_property
    def session(self) -> Session:
        return Session(
            client_name=self.client_name,
            version=self.version,
            auth=self.auth,
        )

    @cached_property
    def fit_methods(self) -> dict[str, Callable]:
        """Returns FitConfig generated methods."""
        return {
            method_config.name: Generator.generate_method(self.session, method_config)
            for method_config in self.method_config_list
            if isinstance(method_config, MethodConfig)
        }

    @cached_property
    def fit_class(self) -> type:
        """Create new class from FitConfig."""

        # Implement the fit_config property to expose the configuration utilized for creating the fitrequest methods.
        @property
        def fit_config(_: Self) -> dict:
            """Configuration used by fitrequest to generate the methods."""
            dump = self.model_dump(exclude_none=True)
            dump['method_config_list'] = sorted(dump['method_config_list'], key=lambda x: x['name'])
            return dump

        # Default username/password __init__ for backward compatibility with fitrequest 0.X.X
        def init(self: Self, username: str | None = None, password: str | None = None) -> None:
            """Default __init__ method that allows username/password authentication."""
            if username or password:
                self.session.update(auth={'username': username, 'password': password})
            self.session.authenticate()

        fit_attrs = self.fit_methods | {
            'client_name': self.client_name,
            'version': self.version,
            'base_url': str(self.base_url),
            'fit_config': fit_config,
            'session': self.session,
            'cli_app': cli_app,
            'cli_run': cli_run,
            '__init__': init,
        }
        new_class = type(self.class_name, (object,), fit_attrs)
        new_class.__doc__ = self.class_docstring
        return new_class
