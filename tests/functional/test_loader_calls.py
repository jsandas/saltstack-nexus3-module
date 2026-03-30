def test_loader_state_call_anonymous_access_test_mode(loaded_modules, loaded_states):
    loaded_states.opts["test"] = True
    loaded_modules["nexus3_anonymous_access.describe"] = lambda: {
        "anonymous_access": {"enabled": False}
    }

    ret = loaded_states["nexus3_security.anonymous_access"]("set-anon", enabled=True)

    assert ret["result"] is None
    assert "will be set to True" in ret["comment"]


def test_loader_state_call_anonymous_access_apply_mode(loaded_modules, loaded_states):
    loaded_states.opts["test"] = False
    loaded_modules["nexus3_anonymous_access.describe"] = lambda: {
        "anonymous_access": {"enabled": False}
    }
    loaded_modules["nexus3_anonymous_access.enable"] = lambda enabled: {
        "anonymous_access": {"enabled": enabled}
    }

    ret = loaded_states["nexus3_security.anonymous_access"]("set-anon", enabled=True)

    assert ret["result"] is True
    assert ret["changes"]["anonymous_access"]["enabled"] is True
