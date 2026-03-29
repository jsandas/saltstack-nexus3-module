from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def salt_loader():
	return pytest.importorskip("salt.loader")


@pytest.fixture
def salt_loader_opts(tmp_path):
	root = Path(__file__).resolve().parents[2]
	cache_dir = tmp_path / "cache"
	sock_dir = tmp_path / "sock"
	extmods_dir = tmp_path / "extmods"
	cache_dir.mkdir(parents=True, exist_ok=True)
	sock_dir.mkdir(parents=True, exist_ok=True)
	extmods_dir.mkdir(parents=True, exist_ok=True)

	return {
		"id": "saltext-nexus3-functional-minion",
		"test": False,
		"cachedir": str(cache_dir),
		"extension_modules": str(extmods_dir),
		"sock_dir": str(sock_dir),
		"file_client": "local",
		"renderer": "jinja|yaml",
		"grains": {},
		"pillar": {},
		"module_dirs": [str(root / "src" / "saltext" / "nexus3" / "modules")],
		"states_dirs": [str(root / "src" / "saltext" / "nexus3" / "states")],
		"utils_dirs": [str(root / "src" / "saltext" / "nexus3" / "utils")],
	}


@pytest.fixture
def loaded_utils(salt_loader, salt_loader_opts):
	return salt_loader.utils(salt_loader_opts)


@pytest.fixture
def loaded_modules(salt_loader, salt_loader_opts, loaded_utils):
	return salt_loader.minion_mods(salt_loader_opts, utils=loaded_utils)


@pytest.fixture
def loaded_states(salt_loader, salt_loader_opts, loaded_modules, loaded_utils):
	return salt_loader.states(salt_loader_opts, functions=loaded_modules, utils=loaded_utils)
