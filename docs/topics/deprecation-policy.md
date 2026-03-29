# Deprecation Policy

This project follows a staged deprecation process to protect existing Salt deployments while moving to the extension package model.

## Policy goals

- Keep existing environments stable during migration.
- Provide clear advance notice before removals.
- Prefer additive transitions over breaking changes.

## Current policy

- Legacy file_root sync deployment is supported for one migration release window.
- Package-based installation is the strategic path and receives primary documentation and CI coverage.
- New features should target the package layout first.

## Required deprecation lifecycle

1. Announce deprecation in docs and changelog.
2. Keep behavior available through at least one release window.
3. Emit release-note reminders before removal.
4. Remove deprecated paths in a major or clearly signaled breaking release.

## What is currently marked for future removal

- Direct distribution model that requires manually copying `_modules`, `_states`, and `_utils`.
- Legacy-only operational guidance once migration window is closed.

## Compatibility expectations

- Public Salt function and state names should remain stable unless explicitly documented as breaking.
- Any behavior-changing migration must include changelog fragments and migration notes.
