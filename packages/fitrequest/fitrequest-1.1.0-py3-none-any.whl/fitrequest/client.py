from typing import ClassVar

from fitrequest.class_factory import ClassFactory
from fitrequest.session import Session


class FitRequest(metaclass=ClassFactory):
    """Default FitRequest client."""

    # FitRequest Session initialized by the ClassFactory
    session: Session

    client_name: str = 'fitrequest'
    version: str = '{version}'
    method_docstring: str = ''

    base_url: str | None = None
    auth: ClassVar[dict] = {}

    method_config_list: ClassVar[list[dict]] = []

    # Default username/password __init__ for backward compatibility with fitrequest 0.X.X
    def __init__(self, username: str | None = None, password: str | None = None) -> None:
        """Default __init__ method that allows username/password authentication."""
        if username or password:
            self.session.update(auth={'username': username, 'password': password})
        self.session.authenticate()
