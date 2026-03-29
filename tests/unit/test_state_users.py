from saltext.nexus3.states import nexus3_users


def test_present_in_test_mode_reports_create_without_calling_create(monkeypatch):
    called = {"create": False}

    def _describe(_name):
        return {"user": {}}

    def _create(*_args, **_kwargs):
        called["create"] = True
        return {}

    monkeypatch.setattr(
        nexus3_users,
        "__salt__",
        {
            "nexus3_users.describe": _describe,
            "nexus3_users.create": _create,
        },
        raising=False,
    )
    monkeypatch.setattr(nexus3_users, "__opts__", {"test": True}, raising=False)

    ret = nexus3_users.present(
        name="alice",
        password="secret",
        emailAddress="alice@example.com",
        firstName="Alice",
        lastName="Admin",
        roles=["nx-admin"],
        status="active",
    )

    assert ret["result"] is None
    assert "will be created" in ret["comment"]
    assert called["create"] is False


def test_present_existing_user_updates_only_password_when_no_drift(monkeypatch):
    called = {"update_password": 0, "update": 0}

    def _describe(_name):
        return {
            "user": {
                "emailAddress": "alice@example.com",
                "firstName": "Alice",
                "lastName": "Admin",
                "roles": ["nx-admin"],
                "status": "active",
            }
        }

    def _update_password(_name, _password):
        called["update_password"] += 1
        return {"status": 204}

    def _update(*_args, **_kwargs):
        called["update"] += 1
        return {"status": 200}

    monkeypatch.setattr(
        nexus3_users,
        "__salt__",
        {
            "nexus3_users.describe": _describe,
            "nexus3_users.update_password": _update_password,
            "nexus3_users.update": _update,
        },
        raising=False,
    )
    monkeypatch.setattr(nexus3_users, "__opts__", {"test": False}, raising=False)

    ret = nexus3_users.present(
        name="alice",
        password="new-secret",
        emailAddress="alice@example.com",
        firstName="Alice",
        lastName="Admin",
        roles=["nx-admin"],
        status="active",
    )

    assert ret["result"] is True
    assert ret["changes"] == {}
    assert "desired state" in ret["comment"]
    assert called["update_password"] == 1
    assert called["update"] == 0


def test_present_existing_user_updates_when_drift_detected(monkeypatch):
    called = {"update_password": 0, "update": 0}

    def _describe(_name):
        return {
            "user": {
                "emailAddress": "old@example.com",
                "firstName": "Alice",
                "lastName": "Old",
                "roles": ["nx-anonymous"],
                "status": "disabled",
            }
        }

    def _update_password(_name, _password):
        called["update_password"] += 1
        return {"status": 204}

    def _update(*_args, **_kwargs):
        called["update"] += 1
        return {"status": 200}

    monkeypatch.setattr(
        nexus3_users,
        "__salt__",
        {
            "nexus3_users.describe": _describe,
            "nexus3_users.update_password": _update_password,
            "nexus3_users.update": _update,
        },
        raising=False,
    )
    monkeypatch.setattr(nexus3_users, "__opts__", {"test": False}, raising=False)

    ret = nexus3_users.present(
        name="alice",
        password="new-secret",
        emailAddress="alice@example.com",
        firstName="Alice",
        lastName="Admin",
        roles=["nx-admin"],
        status="active",
    )

    assert ret["result"] is True
    assert ret["changes"] == {
        "emailAddress": "alice@example.com",
        "lastName": "Admin",
        "roles": ["nx-admin"],
        "status": "active",
    }
    assert called["update_password"] == 1
    assert called["update"] == 1
