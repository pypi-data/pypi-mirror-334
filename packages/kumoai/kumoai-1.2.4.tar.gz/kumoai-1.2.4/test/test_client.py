import pytest
import requests

from kumoai.client.client import KumoClient
from kumoai.testing import onlyIntegrationTest

GOOD_KEY = "MOCK_GOOD_API_KEY"


@pytest.fixture
def mock_auth(requests_mock):
    r"""Matcher for mock authentication to return a 200 status code on a
    valid API key, 404 otherwise.
    """
    def matcher(req):
        res = requests.Response()
        if req.headers.get("X-API-Key") != GOOD_KEY:
            res.status_code = 404
        else:
            res.status_code = 200
        return res

    requests_mock._adapter.add_matcher(matcher)
    yield


@pytest.mark.parametrize(
    "api_key, ok",
    [("MOCK_BAD_API_KEY", False), (GOOD_KEY, True)],
)
def test_client_creation(api_key: str, ok: bool, mock_auth):
    base_url = "http://kumo.ai"
    api_key = api_key
    client = KumoClient(base_url, api_key)
    assert client.authenticate() is ok


@onlyIntegrationTest
def test_client_creation_integ():
    # TODO(manan): enable testing without AUTH_DISABLED
    base_url = "http://localhost:10002"
    api_key = "test:DISABLED"
    client = KumoClient(base_url, api_key)
    assert client.authenticate()
