from saltext.nexus3.states import nexus3_scripts


def test_base_url_passes_script_payload(monkeypatch):
    captured = {}

    def _processor(script_name, script_data, script_args, ret):
        captured["script_name"] = script_name
        captured["script_data"] = script_data
        captured["script_args"] = script_args
        return ret

    monkeypatch.setattr(nexus3_scripts, "_script_processor", _processor)

    ret = nexus3_scripts.base_url("https://nexus.example.com")

    assert ret["result"] is True
    assert captured["script_name"] == "setup_base_url"
    assert captured["script_args"] == {"baseUrl": "https://nexus.example.com"}


def test_task_passes_script_payload(monkeypatch):
    captured = {}

    def _processor(script_name, script_data, script_args, ret):
        captured["script_name"] = script_name
        captured["script_data"] = script_data
        captured["script_args"] = script_args
        return ret

    monkeypatch.setattr(nexus3_scripts, "_script_processor", _processor)

    ret = nexus3_scripts.task(
        name="db-backup",
        typeId="db.backup",
        taskProperties={"location": "/nexus-data/backup"},
        cron="0 0 21 * * ?",
        setAlertEmail="ops@example.com",
    )

    assert ret["result"] is True
    assert captured["script_name"] == "create_task"
    assert captured["script_args"]["name"] == "db-backup"
    assert captured["script_args"]["setAlertEmail"] == "ops@example.com"
