import os
import pytest

from demo_app import factories


@pytest.fixture(scope='session')
def app():
    return factories.create_app(testing=True)
