from saltext.nexus3.states import nexus3_email


def test_clear_in_test_mode(monkeypatch):
    monkeypatch.setattr(nexus3_email, "__opts__", {"test": True}, raising=False)

    ret = nexus3_email.clear("clear-email")

    assert ret["result"] is None
    assert "reset to defaults" in ret["comment"]


def test_configure_reports_update_in_test_mode(monkeypatch):
    monkeypatch.setattr(
        nexus3_email,
        "__salt__",
        {
            "nexus3_email.describe": lambda: {
                "email": {
                    "enabled": False,
                    "fromAddress": "nexus@example.org",
                    "host": "localhost",
                    "nexusTrustStoreEnabled": False,
                    "password": None,
                    "port": 25,
                    "sslOnConnectEnabled": False,
                    "sslServerIdentityCheckEnabled": False,
                    "startTlsEnabled": False,
                    "startTlsRequired": False,
                    "subjectPrefix": None,
                    "username": "",
                }
            }
        },
        raising=False,
    )
    monkeypatch.setattr(nexus3_email, "__opts__", {"test": True}, raising=False)

    ret = nexus3_email.configure(name="set-email", enabled=True, port=587, host="smtp.example.com")

    assert ret["result"] is None
    assert "will be updated" in ret["comment"]
    assert "enabled" in ret["comment"]


def test_configure_no_drift_is_desired_state(monkeypatch):
    monkeypatch.setattr(
        nexus3_email,
        "__salt__",
        {
            "nexus3_email.describe": lambda: {
                "email": {
                    "enabled": True,
                    "fromAddress": "nexus@example.org",
                    "host": "localhost",
                    "nexusTrustStoreEnabled": False,
                    "password": None,
                    "port": 0,
                    "sslOnConnectEnabled": False,
                    "sslServerIdentityCheckEnabled": False,
                    "startTlsEnabled": False,
                    "startTlsRequired": False,
                    "subjectPrefix": None,
                    "username": "",
                }
            }
        },
        raising=False,
    )
    monkeypatch.setattr(nexus3_email, "__opts__", {"test": False}, raising=False)

    ret = nexus3_email.configure(name="set-email", enabled=True)

    assert ret["result"] is True
    assert ret["changes"] == {}
    assert "desired state" in ret["comment"]
