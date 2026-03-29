# Migration Status

This project is migrating to the Salt extension package layout.

## Current transition choices

- New package layout lives under src/saltext/nexus3.
- Legacy file_root sync paths remain available during the migration window.
- Modern CI and packaging are being introduced incrementally.

## Migration phases

1. Establish packaging and loader entry points.
2. Mirror legacy modules/states/utils into package layout.
3. Split quality gates into PR, push, and tag workflows.
4. Expand unit and functional coverage while preserving integration tests.
5. Phase out legacy deployment guidance after the compatibility window.

## Compatibility window

- Legacy sync deployment remains available for one release window.
- Package-based installation is the preferred path for new and existing environments.
- Changes that alter user-facing behavior must be tracked through changelog fragments.

## Operational guidance

- Keep package mirror in sync during transition:

```bash
make sync-src
```

- Run package-path quality checks before release:

```bash
make test
make docs-sphinx
make changelog-draft
```
