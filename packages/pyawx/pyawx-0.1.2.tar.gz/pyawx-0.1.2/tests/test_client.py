import pytest

from pyawx.auth import BasicAuth, OAuth2
from pyawx.client import Client


def test_authenticate_with_oauth2() -> None:
    auth: OAuth2 | BasicAuth = Client._authenticate(
        username=None, password=None, token="test_token"
    )
    assert isinstance(auth, OAuth2)
    assert auth.token == "test_token"


def test_authenticate_with_basic_auth() -> None:
    auth: OAuth2 | BasicAuth = Client._authenticate(
        username="user", password="pass", token=None
    )
    assert isinstance(auth, BasicAuth)
    assert auth.username == "user"
    assert auth.password == "pass"


def test_authenticate_failure() -> None:
    with pytest.raises(
        ValueError,
        match="Authentication failed: Either token or both username and password must be provided",
    ):
        Client._authenticate(username=None, password=None, token=None)
