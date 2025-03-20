# -*- coding: utf-8 -*-

import datetime

import pytest


@pytest.fixture(scope="session")
def duration_cache(request):
    """We can't use `cache` fixture because it has function scope. However the `cache`
    fixture simply returns `request.config.cache`, which is available in any scope."""
    key = "duration/testdurations"
    d = request.config.cache.get(key, {})
    yield d
    request.config.cache.set(key, d)


@pytest.fixture(autouse=True)
def check_duration(request, duration_cache):
    """Stores the dureation of each test"""
    d = duration_cache
    nodeid = request.node.nodeid
    start_time = datetime.datetime.now()
    yield
    duration = (datetime.datetime.now() - start_time).total_seconds()
    d[nodeid] = duration


def by_duration(item):
    """Get the duration of a test from the cache"""
    d = item.config.cache.get("duration/testdurations", {}).get(item.nodeid, 0)
    rounding = item.config.getoption("--slow-last-rounding")
    if rounding >= 0:
        return round(d, rounding)
    else:
        return d


def pytest_addoption(parser):
    parser.addoption(
        "--slow-last",
        action="store_true",
        default=False,
        help="Run slowest tests last",
    )
    parser.addoption(
        "--slow-last-rounding",
        action="store",
        default=2,
        type=int,
        help="Number of decimal places to round test durations",
    )

def pytest_collection_modifyitems(items, config):
    """Sort tests by duration"""
    if config.getoption("--slow-last"):
        items.sort(key=by_duration, reverse=False)
