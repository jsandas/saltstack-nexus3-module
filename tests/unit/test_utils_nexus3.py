import importlib
import sys
import types


class _DummyResponse:
    def __init__(self, status_code=200, content=b"ok"):
        self.status_code = status_code
        self.content = content


def _import_utils_module(monkeypatch, config_option_return):
    fake_salt = types.ModuleType("salt")
    fake_salt_config = types.ModuleType("salt.config")
    fake_salt_loader = types.ModuleType("salt.loader")

    fake_salt_config.minion_config = lambda _path: {}
    fake_salt_loader.minion_mods = lambda _opts: {
        "config.option": lambda _name: config_option_return,
    }

    fake_salt.config = fake_salt_config
    fake_salt.loader = fake_salt_loader

    monkeypatch.setitem(sys.modules, "salt", fake_salt)
    monkeypatch.setitem(sys.modules, "salt.config", fake_salt_config)
    monkeypatch.setitem(sys.modules, "salt.loader", fake_salt_loader)

    sys.modules.pop("saltext.nexus3.utils.nexus3", None)
    return importlib.import_module("saltext.nexus3.utils.nexus3")


def test_get_config_uses_defaults_when_missing(monkeypatch):
    mod = _import_utils_module(monkeypatch, config_option_return={})

    config = mod._get_config()

    assert config["hostname"] == "http://127.0.0.1:8081"
    assert config["username"] == ""
    assert config["password"] == ""


def test_post_uses_json_headers(monkeypatch):
    mod = _import_utils_module(
        monkeypatch,
        config_option_return={
            "hostname": "http://nexus:8081",
            "username": "admin",
            "password": "secret",
        },
    )

    captured = {}

    def _fake_post(url, auth, headers, data):
        captured["url"] = url
        captured["auth"] = auth
        captured["headers"] = headers
        captured["data"] = data
        return _DummyResponse(status_code=201, content=b"created")

    monkeypatch.setattr(mod.requests, "post", _fake_post)

    client = mod.NexusClient()
    ret = client.post("v1/test", {"enabled": True})

    assert ret["status"] == 201
    assert ret["body"] == b"created"
    assert captured["url"].endswith("/service/rest/v1/test")
    assert captured["headers"]["Content-type"] == "application/json"


def test_post_uses_text_headers_for_string_payload(monkeypatch):
    mod = _import_utils_module(
        monkeypatch,
        config_option_return={
            "hostname": "http://nexus:8081",
            "username": "admin",
            "password": "secret",
        },
    )

    captured = {}

    def _fake_post(url, auth, headers, data):
        captured["headers"] = headers
        captured["data"] = data
        return _DummyResponse(status_code=204, content=b"")

    monkeypatch.setattr(mod.requests, "post", _fake_post)

    client = mod.NexusClient()
    ret = client.post("v1/test", "plain-text")

    assert ret["status"] == 204
    assert captured["headers"]["Content-type"] == "text/plain"
    assert captured["data"] == "plain-text"
