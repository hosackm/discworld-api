import pytest
from unittest import mock
from werkzeug.exceptions import Forbidden
import discworld.auth


@pytest.fixture
def payload():
    return {
        "permissions": ["permission_1", "permission_2"]
    }


@pytest.fixture
def mock_request():
    m = mock.MagicMock()
    m.fake_token = "abcdefg1234567890"
    m.headers = {"Authorization": f"Bearer {m.fake_token}"}
    with mock.patch("discworld.auth.request", m):
        yield m


def test_auth_get_token_auth_header(app, mock_request):
    assert discworld.auth.get_token_auth_header() == mock_request.fake_token


def test_check_permissions(app, payload):
    assert discworld.auth.check_permissions("permission_1", payload) is True
    assert discworld.auth.check_permissions("permission_2", payload) is True

    missing_perm_key = {"not_permissions": ["foo", "bar"]}
    with pytest.raises(Forbidden):
        discworld.auth.check_permissions("permission_1", missing_perm_key)

    missing_perm_value = {"permissions": ["foo"]}
    with pytest.raises(Forbidden):
        discworld.auth.check_permissions("permission_1", missing_perm_value)
