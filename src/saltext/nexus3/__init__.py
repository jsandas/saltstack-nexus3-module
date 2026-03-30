"""Nexus 3 Salt extension package."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("saltext-nexus3")
except PackageNotFoundError:
    __version__ = "0.0.0"
