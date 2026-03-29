from saltext.nexus3.states import nexus3_security


def test_anonymous_access_reports_update_in_test_mode(monkeypatch):
    monkeypatch.setattr(
        nexus3_security,
        "__salt__",
        {"nexus3_anonymous_access.describe": lambda: {"anonymous_access": {"enabled": False}}},
        raising=False,
    )
    monkeypatch.setattr(nexus3_security, "__opts__", {"test": True}, raising=False)

    ret = nexus3_security.anonymous_access(name="anon", enabled=True)

    assert ret["result"] is None
    assert "will be set to True" in ret["comment"]


def test_realms_no_update_returns_desired_state(monkeypatch):
    monkeypatch.setattr(
        nexus3_security,
        "__salt__",
        {"nexus3_realms.list_active": lambda: {"realms": ["NexusAuthenticatingRealm"]}},
        raising=False,
    )
    monkeypatch.setattr(nexus3_security, "__opts__", {"test": False}, raising=False)

    ret = nexus3_security.realms(name="realm", realms=["NexusAuthenticatingRealm"])

    assert ret["result"] is True
    assert ret["changes"] == {}
    assert "desired state" in ret["comment"]
