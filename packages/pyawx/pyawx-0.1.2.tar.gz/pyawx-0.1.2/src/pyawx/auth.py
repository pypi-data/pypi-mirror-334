"""Provides authentication mechanisms for configuring HTTP sessions auth.

The `auth` module defines an abstract base class `Auth` for implementing custom
authentication strategies and includes built-in implementations for
Basic Authentication (`BasicAuth`) and OAuth2 (`OAuth2`). These classes are
designed to integrate seamlessly with the `requests` library.

To use an authentication method, initialize the corresponding class with the
required credentials or token and call its `apply` method with a `requests.Session`
object.

Usage:
    >>> from auth import BasicAuth
    >>> session = requests.Session()
    >>> auth = BasicAuth("user", "password")
    >>> auth.apply(session)
    >>> response = session.get("https://example.com")
"""

from abc import ABC, abstractmethod

import requests


class Auth(ABC):
    """Defines the interface for implementing custom authentication strategies.
    to be used with HTTP sessions.

    Usage:
        >>> class CustomAuth(Auth):
        >>>     def apply(self, session: requests.Session) -> None:
        >>>         session.headers.update({"Custom-Auth": "Value"})
    """

    @abstractmethod
    def apply(self, session: requests.Session) -> None:
        """Configures the authentication details for a session.

        Args:
            `session` (`requests.Session`): The HTTP session to apply
                authentication to.
        """
        raise NotImplementedError("Subclasses must implement the apply method.")


class BasicAuth(Auth):
    """Authentication using username and password.

    This method sends credentials as plaintext in the request header.
    Ensure you are communicating over HTTPS to prevent interception.
    This approach is simple but may not be suitable for scenarios requiring
    stronger security or token-based mechanisms.

    Attributes:
        `username` (`str`): The username for authentication.
        `password` (`str`): The password for authentication.

    Usage:
        >>> auth = BasicAuth("foo", "***")
        >>> session = requests.Session()
        >>> auth.apply(session)
        >>> response = session.get("https://example.com")
    """

    def __init__(self, username: str, password: str) -> None:
        self.username: str = username
        self.password: str = password

    def apply(self, session: requests.Session) -> None:
        """Configures basic authentication for the session.

        Args:
            `session` (`requests.Session`): The HTTP session to apply
                authentication to.
        """
        session.auth = (self.username, self.password)


class OAuth2(Auth):
    """Authentication using an OAuth2 bearer token.

    OAuth2 tokens should be securely stored and rotated periodically.
    Token-based authentication eliminates the need to transmit usernames and
    passwords, reducing the attack surface. However, be mindful of token
    expiration and ensure token renewal mechanisms are in place if necessary.

    Attributes:
        `token` (`str`): The bearer token for authentication.

    Usage:
        >>> auth = OAuth2("********")
        >>> session = requests.Session()
        >>> auth.apply(session)
        >>> response = session.get("https://example.com")
    """

    def __init__(self, token: str) -> None:
        self.token: str = token

    def apply(self, session: requests.Session) -> None:
        """Configures OAuth2 authentication for the session.

        Args:
            `session` (`requests.Session`): The HTTP session to apply
                authentication to.
        """
        session.headers.update({"Authorization": f"Bearer {self.token}"})
