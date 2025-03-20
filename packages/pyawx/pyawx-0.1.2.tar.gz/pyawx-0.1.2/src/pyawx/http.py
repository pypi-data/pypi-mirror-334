"""Provides an HTTP client for interacting with RESTful APIs.

The `HTTP` class simplifies API interactions by abstracting HTTP methods
(GET, POST, PATCH, DELETE) and constructing resource-specific endpoints dynamically.
It integrates seamlessly with authentication mechanisms defined in the `pyawx.auth`
module.

To use the HTTP client, initialize it with the API's base URL, the API version,
an authentication method, and optionally disable TLS certificate verification.
Then, call the respective methods to perform operations on resources.

Usage:
    >>> from http import HTTP
    >>> from auth import BasicAuth
    >>> auth = BasicAuth("username", "password")
    >>> client = HTTP("https://api.example.com", "v1", auth, verify_tls=False)
    >>> response = client.get("resource", "id")

Notes:

- The client expects JSON responses from the API.
- HTTP error handling is automatically managed using `response.raise_for_status()`.
- All payloads are sent as JSON.

Warnings:

- Ensure that sensitive data (e.g., API keys, credentials) is securely stored
  and not hardcoded in the source code.
- Always use HTTPS to encrypt communication between the client and the API.
- Disabling TLS certificate verification (`verify_tls=False`) can expose you to
  MITM attacks. Use this option with caution.
"""

import requests

from .auth import Auth


class HTTP:
    """HTTP client for making API requests.

    The client maintains a persistent session for efficiency.
    Authentication is applied during initialization.
    Dynamic URL construction ensures compatibility with versioned APIs.

    Attributes:
        `url` (`str`): The base URL for the API.
        `api_version` (`str`): The version of the API being used.
        `session` (`requests.Session`): The HTTP session for making requests.
    """

    def __init__(
        self, url: str, api_version: str, auth: Auth, verify_tls: bool
    ) -> None:
        """Initializes the HTTP client with the base URL, API version,
        authentication, and TLS verification option.

        Args:
            `url` (`str`): The base URL for the API.
            `api_version` (`str`): The version of the API being used.
            `auth` (`Auth`): The authentication mechanism for the API.
            `verify_tls` (`bool`): Whether to verify TLS certificates.
        """
        self.url: str = url.rstrip("/")
        self.api_version: str = api_version
        self.session = requests.Session()
        self.session.verify = verify_tls
        auth.apply(self.session)

    def _build_url(self, resource: str, resource_id: str | None = None) -> str:
        """Constructs the full URL for a given resource and optional resource ID.

        The constructed URL includes the base URL, API version, and resource.
        Resource identifiers are appended to the URL if provided.

        Args:
            `resource` (`str`): The resource path.
            `resource_id` (str | None): The optional resource identifier.

        Returns:
            `str`: The constructed URL.
        """
        url: str = f"{self.url}/api/{self.api_version}/{resource}/"
        return url if not resource_id else f"{url}{resource_id}/"

    def _request(self, method: str, url: str, data: dict | None = None) -> dict:
        """Sends an HTTP request to the specified URL.

        Non-2xx responses raise `HTTPError`.
        APIs that return non-JSON responses may cause unexpected behavior.

        Args:
            `method` (`str`): The HTTP method (GET, POST, PATCH, DELETE).
            `url` (`str`): The URL to send the request to.
            `data` (`dict | None`): Optional JSON payload.

        Returns:
            `dict`: The JSON response.

        Raises:
            `HTTPError`: If the HTTP response status code is not 2xx.
        """
        response: requests.Response = self.session.request(method, url, json=data)
        response.raise_for_status()
        return response.json() if response.content else {}

    def is_authenticated(self) -> bool:
        """Checks if the HTTP client is authenticated.

        Returns:
            `bool`: True if the client is authenticated, False otherwise.
        """
        try:
            self._request("GET", self.url)
            return True
        except requests.HTTPError:
            return False

    def get(self, resource: str, resource_id: str | None = None) -> dict:
        """Retrieves a resource, optionally by its identifier.

        Args:
            `resource` (`str`): The resource type.
            `resource_id` (`str | None`): The resource identifier.

        Returns:
            `dict`: The retrieved resource.

        Raises:
            `ValueError`: If the resource retrieval fails.

        Examples:
            >>> response = client.get("resource", "id")
            >>> response = client.get("resource")
        """
        try:
            url: str = self._build_url(resource, resource_id)
            return self._request("GET", url)
        except requests.HTTPError as e:
            raise ValueError(f"Failed to retrieve resource: {e}")

    def post(self, resource: str, data: dict) -> dict:
        """Creates a new resource.

        Args:
            `resource` (`str`): The resource type.
            `data` (`dict`): The payload for the new resource.

        Returns:
            `dict`: The created resource.

        Raises:
            `ValueError`: If the resource creation fails.

        Examples:
            >>> response = client.post("resource", {"foo": "bar"})
        """
        try:
            url: str = self._build_url(resource)
            return self._request("POST", url, data)
        except requests.HTTPError as e:
            raise ValueError(f"Failed to create resource: {e}")

    def patch(self, resource: str, resource_id: str, data: dict) -> dict:
        """Updates an existing resource by its identifier.

        Args:
            `resource` (`str`): The resource type.
            `resource_id` (`str`): The resource identifier.
            `data` (`dict`): The payload with updates.

        Returns:
            `dict`: The updated resource.

        Raises:
            `ValueError`: If the resource update fails.

        Examples:
            >>> response = client.patch("resource", "id", {"foo": "updated_bar"})
        """
        try:
            url: str = self._build_url(resource, resource_id)
            return self._request("PATCH", url, data)
        except requests.HTTPError as e:
            raise ValueError(f"Failed to update resource: {e}")

    def delete(self, resource: str, resource_id: str) -> None:
        """Deletes a specific resource by its identifier.

        Args:
            `resource` (`str`): The resource type.
            `resource_id` (`str`): The resource identifier.

        Raises:
            `ValueError`: If the resource deletion fails.

        Examples:
            >>> client.delete("resource", "id")
        """
        try:
            url: str = self._build_url(resource, resource_id)
            self._request("DELETE", url)
        except requests.HTTPError as e:
            raise ValueError(f"Failed to delete resource: {e}")
