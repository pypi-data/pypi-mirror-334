import os
import time

import pytest

from solark_cloud import AuthenticationError, SolArkCloud


@pytest.fixture
def client():
    return SolArkCloud()


# TODO: Mock out the live API for the testing.
USERNAME = os.environ.get("SOLARK_USERNAME", "")
PASSWORD = os.environ.get("SOLARK_PASSWORD", "")
PLANT_ID = os.environ.get("SOLARK_PLANT_ID", 0)


def test_login(client):
    if PLANT_ID == 0:
        pytest.skip("Skipping login test")
    result = client.login(USERNAME, PASSWORD)
    assert result
    assert client.access_token
    assert client.refresh_token
    assert client.expires_at > time.time()


def test_plants(client):
    if PLANT_ID == 0:
        pytest.skip("Skipping plants test")
    client.login(USERNAME, PASSWORD)
    result = client.plants()
    assert len(result.plants)


def test_flow(client):
    if PLANT_ID == 0:
        pytest.skip("Skipping flow test")
    client.login(USERNAME, PASSWORD)
    flow = client.flow(PLANT_ID)
    assert flow.battery_power > 0


def test_login_invalid_credentials(client):
    try:
        result = client.login("invalid_username", "invalid_password")
    except AuthenticationError as e:
        assert isinstance(e, AuthenticationError)
        assert e.code == 102
    else:
        assert not result
