from pathlib import Path

from saltext.nexus3 import loader


def test_loader_paths_exist():
    module_dir = Path(loader.module_dirs()[0])
    states_dir = Path(loader.states_dirs()[0])
    utils_dir = Path(loader.utils_dirs()[0])

    assert module_dir.name == "modules"
    assert states_dir.name == "states"
    assert utils_dir.name == "utils"
    assert module_dir.exists()
    assert states_dir.exists()
    assert utils_dir.exists()
