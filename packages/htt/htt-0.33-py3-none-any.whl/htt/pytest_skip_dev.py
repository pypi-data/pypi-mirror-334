import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "dev: mark test as dev")


def pytest_addoption(parser):
    parser.addoption("--dev", action="store_true", help="enable dev tests")


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--dev"):
        skip_dev = pytest.mark.skip(reason="need --dev option to run")
        for item in items:
            if item.get_closest_marker("dev"):
                item.add_marker(skip_dev)
