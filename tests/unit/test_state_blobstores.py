from saltext.nexus3.states import nexus3_blobstores


def test_present_in_test_mode_reports_create(monkeypatch):
    monkeypatch.setattr(
        nexus3_blobstores,
        "__salt__",
        {"nexus3_blobstores.describe": lambda _name: {"blobstore": {}}},
        raising=False,
    )
    monkeypatch.setattr(nexus3_blobstores, "__opts__", {"test": True}, raising=False)

    ret = nexus3_blobstores.present(name="blob-a")

    assert ret["result"] is None
    assert "will be created" in ret["comment"]


def test_present_existing_blobstore_no_drift_no_update_call(monkeypatch):
    called = {"update": 0}

    monkeypatch.setattr(
        nexus3_blobstores,
        "__salt__",
        {
            "nexus3_blobstores.describe": lambda _name: {
                "blobstore": {
                    "softQuota": None,
                }
            },
            "nexus3_blobstores.update": lambda *_args, **_kwargs: called.__setitem__("update", 1),
        },
        raising=False,
    )
    monkeypatch.setattr(nexus3_blobstores, "__opts__", {"test": False}, raising=False)

    ret = nexus3_blobstores.present(name="blob-a", quota_type=None)

    assert ret["result"] is True
    assert ret["changes"] == {}
    assert "desired state" in ret["comment"]
    assert called["update"] == 0
