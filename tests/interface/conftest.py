""" Interface Testing is performed to evaluate whether service's internal
    components act as expected.
    These tests (unlike unit tests) should use real entrypoints to trigger
    service's functionality.
    Interface tests will often use real dependencies when appropriate.
    When to use mocked vs real dependencies:
    Use mock for dependencies that deal with external services which are not a
    part of service's bounded context.
    User real dependencies for testing interaction with internal systems that
    you have a full control of like databases and file systems.
    Dependencies themselves should all have their own
    set of unit and interface tests.
"""

import os

import pytest
from installation_requests.service import InstallationRequestsService


@pytest.fixture
def config():
    return {
        "DB_URIS": {
            "installation_requests:Base": "postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}".format(
                db_user=os.getenv("DB_USER", "postgres"),
                db_pass=os.getenv("DB_PASSWORD", "password"),
                db_host=os.getenv("DB_HOST", "localhost"),
                db_port=os.getenv("DB_PORT", "5433"),
                db_name=os.getenv("DB_NAME", "installation_requests_DB"),
            )
        },
        "AMQP_URI": "amqp://{rabbitmq_url}".format(
            rabbitmq_url=os.getenv("RABBITMQ_URL", "guest:guest@127.0.0.1:5672")
        ),
        "serializer": "pickle",
    }


@pytest.fixture
def create_svc(container_factory, config):
    service_container = container_factory(InstallationRequestsService, config)
    service_container.start()
    yield service_container
    service_container.stop()
