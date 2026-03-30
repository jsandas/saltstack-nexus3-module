"""Salt loader entry points for saltext-nexus3."""

from pathlib import Path

PKG_ROOT = Path(__file__).resolve().parent


def module_dirs():
    return [str(PKG_ROOT / "modules")]


def states_dirs():
    return [str(PKG_ROOT / "states")]


def utils_dirs():
    return [str(PKG_ROOT / "utils")]
