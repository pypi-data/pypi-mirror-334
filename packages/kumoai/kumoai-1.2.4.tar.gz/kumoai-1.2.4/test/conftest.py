from typing import Generator

import pytest
import requests_mock

from kumoai import global_state, init

# Not mock:// due to https://stackoverflow.com/a/76056002
MOCK_URL = "http://kumo.ai"


@pytest.fixture(scope="class")
def mock_api() -> Generator[requests_mock.Mocker, None, None]:
    with requests_mock.Mocker() as m:
        yield m


@pytest.fixture(scope="class")
def setup_mock_client(mock_api):
    # Create the client:
    mock_api.get(f"{MOCK_URL}/redoc", status_code=200)
    init(url=MOCK_URL, api_key="DISABLED")

    # Run the test:
    yield

    # Cleanup, do not re-use clients across unit tests:
    global_state.clear()


@pytest.fixture(scope="class")
def setup_integration_client():
    # Create the client:
    init(url="http://localhost:10002", api_key="test:DISABLED")

    # Run the test:
    yield

    # Cleanup, do not re-use clients across unit tests:
    global_state.clear()
