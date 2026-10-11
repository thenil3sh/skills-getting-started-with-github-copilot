import copy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


initial_activities = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities = copy.deepcopy(initial_activities)
    yield
    app_module.activities = copy.deepcopy(initial_activities)


@pytest.fixture
def client():
    with TestClient(app_module.app) as test_client:
        yield test_client
