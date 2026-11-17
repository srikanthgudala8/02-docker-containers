import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

import redis  # noqa: E402

import app as app_module  # noqa: E402


class FakeRedis:
    def __init__(self):
        self.count = 0

    def incr(self, key):
        self.count += 1
        return self.count

    def ping(self):
        return True


class BrokenRedis:
    def incr(self, key):
        raise redis.exceptions.ConnectionError("down")

    def ping(self):
        raise redis.exceptions.ConnectionError("down")


def client_with(cache):
    app_module.cache = cache
    app_module.app.config["TESTING"] = True
    return app_module.app.test_client()


def test_counter_increments():
    client = client_with(FakeRedis())
    assert client.get("/").get_json()["visits"] == 1
    assert client.get("/").get_json()["visits"] == 2


def test_index_returns_503_when_cache_down():
    assert client_with(BrokenRedis()).get("/").status_code == 503


def test_health_does_not_depend_on_redis():
    assert client_with(BrokenRedis()).get("/health").status_code == 200


def test_ready_reflects_redis():
    assert client_with(FakeRedis()).get("/ready").status_code == 200
    assert client_with(BrokenRedis()).get("/ready").status_code == 503
