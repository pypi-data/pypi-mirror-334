from requests import Session

from pyawx.auth import BasicAuth, OAuth2


def test_basic_auth_apply(session: Session, basic_auth: BasicAuth) -> None:
    basic_auth.apply(session)
    assert session.auth == ("user", "password")


def test_oauth2_apply(session: Session, oauth2: OAuth2) -> None:
    oauth2.apply(session)
    assert session.headers["Authorization"] == "Bearer token"
