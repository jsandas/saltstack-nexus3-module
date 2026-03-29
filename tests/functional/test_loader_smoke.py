def test_loader_finds_nexus3_modules_and_states(loaded_modules, loaded_states):
    assert "nexus3_users.describe" in loaded_modules
    assert "nexus3_roles.describe" in loaded_modules
    assert "nexus3_users.present" in loaded_states
    assert "nexus3_roles.present" in loaded_states
