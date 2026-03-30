# Installation

This project is distributed as a Salt extension package.

## Supported installation path

Use the package path for all deployments and development workflows.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -U pip
python -m pip install -e '.[dev,tests,docs]'
```

Package-based installation enables:

- Loader discovery from the extension package.
- Reproducible dependency management.
- CI parity with local development.

## Legacy file_root layout status

The legacy `_modules`, `_states`, and `_utils` file_root layout has been removed.

If you are migrating from that layout, use package installation and loader entry points from `src/saltext/nexus3`.
