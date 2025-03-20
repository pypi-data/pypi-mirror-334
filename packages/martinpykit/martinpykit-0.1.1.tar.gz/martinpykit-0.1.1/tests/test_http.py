import pytest  # type: ignore
from martinpykit.utils import HttpClient, AsyncHttpClient


def http_client():
    client = HttpClient(
        base_url="https://jsonplaceholder.typicode.com",
        headers={"User-Agent": "test"},
        timeout=10,
        max_retries=3,
    )
    return client


def test_sync_get():
    with http_client() as client:
        response = client.get("/posts/1")
        assert response is not None
        userId = response.get("userId", None)
        assert userId == 1


def test_sync_post():
    with http_client() as client:
        response = client.post("posts", json={"title": "foo", "body": "bar", "userId": 1})
        assert response is not None
        userId = response.get("userId", None)
        assert userId == 1


def async_http_client():
    aclient = AsyncHttpClient(
        base_url="https://jsonplaceholder.typicode.com",
        headers={"User-Agent": "test"},
        timeout=10,
        max_retries=3,
    )
    return aclient


@pytest.mark.asyncio
async def test_async_get():
    async with async_http_client() as aclient:
        response = await aclient.aget("/posts/1")
        assert response is not None
        userId = response.get("userId", None)
        assert userId == 1


@pytest.mark.asyncio
async def test_async_post():
    async with async_http_client() as aclient:
        response = await aclient.apost(
            "posts", json={"title": "foo", "body": "bar", "userId": 1}
        )
        assert response is not None
        userId = response.get("userId", None)
        assert userId == 1
