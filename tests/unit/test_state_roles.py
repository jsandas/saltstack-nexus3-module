from saltext.nexus3.states import nexus3_roles


def test_present_in_test_mode_reports_create_without_calling_create(monkeypatch):
    called = {"create": False}

    def _describe(_name):
        return {"role": {}}

    def _create(*_args, **_kwargs):
        called["create"] = True
        return {}

    monkeypatch.setattr(
        nexus3_roles,
        "__salt__",
        {
            "nexus3_roles.describe": _describe,
            "nexus3_roles.create": _create,
        },
        raising=False,
    )
    monkeypatch.setattr(nexus3_roles, "__opts__", {"test": True}, raising=False)

    ret = nexus3_roles.present(
        name="team-role",
        description="Team role",
        privileges=["nx-repository-view-*-*-read"],
        roles=["nx-anonymous"],
    )

    assert ret["result"] is None
    assert "will be created" in ret["comment"]
    assert called["create"] is False


def test_present_existing_role_no_drift_does_not_call_update(monkeypatch):
    called = {"update": 0}

    def _describe(_name):
        return {
            "role": {
                "description": "Team role",
                "privileges": ["nx-repository-view-*-*-read"],
                "roles": ["nx-anonymous"],
            }
        }

    def _update(*_args, **_kwargs):
        called["update"] += 1
        return {"status": 200}

    monkeypatch.setattr(
        nexus3_roles,
        "__salt__",
        {
            "nexus3_roles.describe": _describe,
            "nexus3_roles.update": _update,
        },
        raising=False,
    )
    monkeypatch.setattr(nexus3_roles, "__opts__", {"test": False}, raising=False)

    ret = nexus3_roles.present(
        name="team-role",
        description="Team role",
        privileges=["nx-repository-view-*-*-read"],
        roles=["nx-anonymous"],
    )

    assert ret["result"] is True
    assert ret["changes"] == {}
    assert "desired state" in ret["comment"]
    assert called["update"] == 0


def test_present_in_test_mode_with_drift_reports_update_plan(monkeypatch):
    called = {"update": 0}

    def _describe(_name):
        return {
            "role": {
                "description": "Old desc",
                "privileges": ["nx-repository-view-*-*-read"],
                "roles": ["nx-anonymous"],
            }
        }

    def _update(*_args, **_kwargs):
        called["update"] += 1
        return {"status": 200}

    monkeypatch.setattr(
        nexus3_roles,
        "__salt__",
        {
            "nexus3_roles.describe": _describe,
            "nexus3_roles.update": _update,
        },
        raising=False,
    )
    monkeypatch.setattr(nexus3_roles, "__opts__", {"test": True}, raising=False)

    ret = nexus3_roles.present(
        name="team-role",
        description="Team role",
        privileges=["nx-repository-view-*-*-read"],
        roles=["nx-anonymous"],
    )

    assert ret["result"] is None
    assert "will be updated" in ret["comment"]
    assert "description" in ret["comment"]
    assert called["update"] == 0
