# Installation

This project currently supports two installation models during the migration window.

## Preferred: package-based installation

Use the package path for new deployments and all development workflows.

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

## Legacy: file_root sync installation

Legacy deployment remains supported for transition compatibility.

1. Copy `_modules`, `_states`, and `_utils` to the Salt files root.
2. Run sync on minions.

```bash
salt '*' saltutil.sync_all
```

Use legacy mode only when existing automation depends on the old layout.

## Migration helper for dual-path maintenance

While both layouts coexist, keep the package mirror in sync with:

```bash
make sync-src
```

This command copies legacy loader folders into `src/saltext/nexus3` and applies import rewrites needed by the package layout.
