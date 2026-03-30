# Migration Status

This project has migrated to the Salt extension package layout.

## Current state

- New package layout lives under src/saltext/nexus3.
- Legacy file_root sync paths have been removed.
- CI, packaging, and docs now target the package layout.

## Migration phases

1. Establish packaging and loader entry points.
2. Split quality gates into PR, push, and tag workflows.
3. Expand unit and functional coverage while preserving integration tests.
4. Move docs reference to Sphinx autodoc from `src`.
5. Remove legacy loader folders from the repository.

## Compatibility note

- Package-based installation is the only supported path.
- Changes that alter user-facing behavior are tracked through changelog fragments.

## Operational guidance

- Run package-path quality checks before release:

```bash
make test
make docs-sphinx
make changelog-draft
```
