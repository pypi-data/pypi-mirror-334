import pytest
import responses
from requests.exceptions import HTTPError

from pyawx.http import HTTP


def test_build_url_without_resource_id(http: HTTP) -> None:
    url: str = http._build_url("resource")
    assert url == "https://api.example.com/api/v1/resource/"


def test_build_url_with_resource_id(http: HTTP) -> None:
    url: str = http._build_url("resource", "123")
    assert url == "https://api.example.com/api/v1/resource/123/"


@responses.activate
def test_request_success(http: HTTP) -> None:
    responses.add(
        responses.GET,
        "https://api.example.com/api/v1/resource/",
        json={"key": "value"},
        status=200,
    )

    response: dict = http._request("GET", "https://api.example.com/api/v1/resource/")
    assert response == {"key": "value"}


@responses.activate
def test_request_http_error(http: HTTP) -> None:
    responses.add(
        responses.GET,
        "https://api.example.com/api/v1/resource/",
        status=404,
    )

    with pytest.raises(HTTPError):
        http._request("GET", "https://api.example.com/api/v1/resource/")


@responses.activate
def test_request_no_content(http: HTTP) -> None:
    responses.add(
        responses.GET,
        "https://api.example.com/api/v1/resource/",
        status=204,
    )

    response: dict = http._request("GET", "https://api.example.com/api/v1/resource/")
    assert response == {}


@responses.activate
def test_is_authenticated_success(http: HTTP) -> None:
    responses.add(
        responses.GET,
        "https://api.example.com",
        status=200,
    )

    assert http.is_authenticated() is True


@responses.activate
def test_is_authenticated_failure(http: HTTP) -> None:
    responses.add(
        responses.GET,
        "https://api.example.com",
        status=401,
    )

    assert http.is_authenticated() is False


@responses.activate
def test_get_request(http: HTTP) -> None:
    responses.add(
        responses.GET,
        "https://api.example.com/api/v1/resource/123/",
        json={"key": "value"},
        status=200,
    )

    response: dict = http.get("resource", "123")
    assert response == {"key": "value"}


@responses.activate
def test_post_request(http: HTTP) -> None:
    responses.add(
        responses.POST,
        "https://api.example.com/api/v1/resource/",
        json={"key": "value"},
        status=201,
    )

    response: dict = http.post("resource", {"key": "value"})
    assert response == {"key": "value"}


@responses.activate
def test_patch_request(http: HTTP) -> None:
    responses.add(
        responses.PATCH,
        "https://api.example.com/api/v1/resource/123/",
        json={"key": "updated_value"},
        status=200,
    )

    response: dict = http.patch("resource", "123", {"key": "updated_value"})
    assert response == {"key": "updated_value"}


@responses.activate
def test_delete_request(http: HTTP) -> None:
    responses.add(
        responses.DELETE,
        "https://api.example.com/api/v1/resource/123/",
        status=204,
    )

    response: None = http.delete("resource", "123")
    assert response is None


@responses.activate
def test_get_request_failure(http: HTTP) -> None:
    responses.add(
        responses.GET,
        "https://api.example.com/api/v1/resource/123/",
        status=404,
    )

    with pytest.raises(ValueError, match="Failed to retrieve resource"):
        http.get("resource", "123")


@responses.activate
def test_post_request_failure(http: HTTP) -> None:
    responses.add(
        responses.POST,
        "https://api.example.com/api/v1/resource/",
        status=400,
    )

    with pytest.raises(ValueError, match="Failed to create resource"):
        http.post("resource", {"key": "value"})


@responses.activate
def test_patch_request_failure(http: HTTP) -> None:
    responses.add(
        responses.PATCH,
        "https://api.example.com/api/v1/resource/123/",
        status=400,
    )

    with pytest.raises(ValueError, match="Failed to update resource"):
        http.patch("resource", "123", {"key": "updated_value"})


@responses.activate
def test_delete_request_failure(http: HTTP) -> None:
    responses.add(
        responses.DELETE,
        "https://api.example.com/api/v1/resource/123/",
        status=400,
    )

    with pytest.raises(ValueError, match="Failed to delete resource"):
        http.delete("resource", "123")
