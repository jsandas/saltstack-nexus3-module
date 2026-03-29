import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

project = "saltext-nexus3"
extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
master_doc = "index"
exclude_patterns = ["_build", "modules", "states"]
html_theme = "alabaster"

# Salt is only available at runtime; mock it so autodoc can import extension modules.
autodoc_mock_imports = ["salt"]

# Render type hints in the description body rather than the signature.
autodoc_typehints = "description"

# Show inherited members and special members.
autodoc_default_options = {
    "members": True,
    "show-inheritance": True,
    "undoc-members": False,
}
