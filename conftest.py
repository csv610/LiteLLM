import os

import pytest


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "live: marks tests that require live model or network access",
    )


def pytest_collection_modifyitems(config, items):
    # Run all tests including live tests by default
    # To skip live tests, set SKIP_LIVE_TESTS=1
    if os.getenv("SKIP_LIVE_TESTS") == "1":
        skip_live = pytest.mark.skip(
            reason="Live model/network tests are skipped. Set SKIP_LIVE_TESTS=0 to enable them."
        )

        for item in items:
            nodeid = item.nodeid.lower()
            if "live" in nodeid or item.get_closest_marker("live") is not None:
                item.add_marker(skip_live)
