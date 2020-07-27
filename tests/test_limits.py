import pytest


@pytest.mark.parametrize("endpoint",
                         [("get", "/api/books"),
                          ("post", "/api/books"),
                          ("patch", "/api/books/1"),
                          ("delete", "/api/books/1"),
                          ("get", "/api/subseries"),
                          ("post", "/api/subseries"),
                          ("patch", "/api/subseries/1"),
                          ("delete", "/api/subseries/1"),
                          ])
def test_api_is_rate_limited(client, endpoint):
    method, url = endpoint
    method = getattr(client, method)

    # exhaust available requests to activate rate limiter
    for _ in range(50):
        method(url)

    # make sure the next request is rate limited
    resp = method(url)
    assert resp.status_code == 429
