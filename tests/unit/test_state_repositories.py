from saltext.nexus3.states import nexus3_repositories


def test_absent_in_test_mode_reports_delete(monkeypatch):
    monkeypatch.setattr(
        nexus3_repositories,
        "__salt__",
        {"nexus3_repositories.describe": lambda **_kwargs: {"repository": {"name": "repo-a"}}},
        raising=False,
    )
    monkeypatch.setattr(nexus3_repositories, "__opts__", {"test": True}, raising=False)

    ret = nexus3_repositories.absent("repo-a")

    assert ret["result"] is None
    assert "will be deleted" in ret["comment"]


def test_present_rejects_type_or_format_change(monkeypatch):
    monkeypatch.setattr(
        nexus3_repositories,
        "__salt__",
        {
            "nexus3_repositories.describe": lambda **_kwargs: {
                "repository": {
                    "type": "proxy",
                    "format": "maven2",
                    "storage": {
                        "blobStoreName": "default",
                        "strictContentTypeValidation": True,
                    },
                }
            }
        },
        raising=False,
    )
    monkeypatch.setattr(nexus3_repositories, "__opts__", {"test": False}, raising=False)

    ret = nexus3_repositories.present(name="repo-a", type="hosted", format="maven2")

    assert ret["result"] is False
    assert "cannot modified" in ret["comment"]


def test_present_group_no_drift_returns_desired_state(monkeypatch):
    called = {"group": 0}

    def _group(*_args, **_kwargs):
        called["group"] += 1
        return {"repository": {"name": "repo-a"}}

    monkeypatch.setattr(
        nexus3_repositories,
        "__salt__",
        {
            "nexus3_repositories.describe": lambda **_kwargs: {
                "repository": {
                    "type": "group",
                    "format": "maven2",
                    "storage": {
                        "blobStoreName": "default",
                        "strictContentTypeValidation": True,
                    },
                    "group": {"memberNames": []},
                }
            },
            "nexus3_repositories.group": _group,
        },
        raising=False,
    )
    monkeypatch.setattr(nexus3_repositories, "__opts__", {"test": False}, raising=False)

    ret = nexus3_repositories.present(name="repo-a", type="group", format="maven2")

    assert ret["result"] is True
    assert "desired state" in ret["comment"]
    assert called["group"] == 0
