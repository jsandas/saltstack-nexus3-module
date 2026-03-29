from saltext.nexus3.states import nexus3_privileges


def test_present_application_requires_domain(monkeypatch):
    monkeypatch.setattr(
        nexus3_privileges,
        "__salt__",
        {
            "nexus3_privileges.describe": lambda _name: {
                "privilege": {
                    "description": "New Nexus privilege",
                    "actions": [],
                    "domain": "users",
                }
            }
        },
        raising=False,
    )
    monkeypatch.setattr(nexus3_privileges, "__opts__", {"test": False}, raising=False)

    ret = nexus3_privileges.present(name="priv-a", type="application", domain=None)

    assert ret["result"] is True
    assert "domain cannot be None" in ret["comment"]


def test_present_in_test_mode_reports_update(monkeypatch):
    monkeypatch.setattr(
        nexus3_privileges,
        "__salt__",
        {
            "nexus3_privileges.describe": lambda _name: {
                "privilege": {
                    "description": "old",
                    "actions": ["READ"],
                    "domain": "users",
                }
            }
        },
        raising=False,
    )
    monkeypatch.setattr(nexus3_privileges, "__opts__", {"test": True}, raising=False)

    ret = nexus3_privileges.present(
        name="priv-a",
        type="application",
        description="new",
        actions=["READ", "UPDATE"],
        domain="users",
    )

    assert ret["result"] is None
    assert "will be updated" in ret["comment"]
    assert "description" in ret["comment"]
