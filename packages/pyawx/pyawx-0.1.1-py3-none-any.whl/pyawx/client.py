"""Provides a client for interacting with API resources.

The `Client` class simplifies the use of various API resources by initializing
an HTTP client and providing access to resource-specific classes. It supports
both Basic and OAuth2 authentication mechanisms and allows toggling TLS
certificate verification.

To use the client, initialize it with the API's base URL, authentication
credentials, and optionally disable TLS certificate verification. Then, access
the desired resource through the provided attributes.

Usage:
    >>> from client import Client
    >>> client = Client("https://api.example.com", token="your_token_here")
    >>> job_templates = client.job_template.fetch("id")

Warnings:

- Ensure that sensitive data (e.g., API keys, credentials) is securely stored
  and not hardcoded in the source code.
- Always use HTTPS to encrypt communication between the client and the API.
- Disabling TLS certificate verification (`verify_tls=False`) can expose you to
  MITM attacks. Use this option with caution.
"""

from .auth import BasicAuth, OAuth2
from .http import HTTP
from .resources import JobTemplateResource, WorkflowJobTemplateResource


class Client:
    """Client to facilitate the use of the resources.

    This class initializes the HTTP client and provides access to the resources.

    Attributes:
        `_http_client` (`HTTP`): The HTTP client used to send requests.
        `job_template` (`JobTemplateResource`): Resource for job templates.
        `workflow_job_template` (`WorkflowJobTemplateResource`): Resource for
            workflow job templates.
    """

    def __init__(
        self,
        url: str,
        username: str | None = None,
        password: str | None = None,
        token: str | None = None,
        verify_tls: bool = True,
    ) -> None:
        """Initializes the Client with the base URL, API v2, authentication,
        and TLS verification option.

        Args:
            `url` (`str`): The base URL for the API.
            `username` (`str | None`): The username for BasicAuth.
            `password` (`str | None`): The password for BasicAuth.
            `token` (`str | None`): The OAuth2 token.
            `verify_tls` (`bool`): Whether to verify TLS certificates.
        """
        self._auth: OAuth2 | BasicAuth = self._authenticate(username, password, token)
        self._http_client = HTTP(url, "v2", self._auth, verify_tls)
        self.job_template = JobTemplateResource(self._http_client)
        self.workflow_job_template = WorkflowJobTemplateResource(self._http_client)

    @staticmethod
    def _authenticate(
        username: str | None, password: str | None, token: str | None
    ) -> OAuth2 | BasicAuth:
        """Returns the appropriate authentication mechanism based on the
        provided credentials.

        Args:
            `username` (`str | None`): The username for BasicAuth.
            `password` (`str | None`): The password for BasicAuth.
            `token` (`str | None`): The OAuth2 token.

        Returns:
            `OAuth2 | BasicAuth`: The authentication mechanism.

        Raises:
            `ValueError`: If neither token nor both username and password are
                provided.
        """
        if token:
            auth = OAuth2(token)
        elif username and password:
            auth = BasicAuth(username, password)
        else:
            raise ValueError(
                "Authentication failed: Either token or both username and password must be provided"
            )

        return auth
