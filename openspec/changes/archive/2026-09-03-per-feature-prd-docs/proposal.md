## Why

Target application documentation must describe each distinct business feature/domain in its own dedicated PRD file under `docs/features/`. Additionally, an overall index and master context document (`docs/features/leiturama.md` or `docs/features/index.md`) is required to summarize the architecture, module goals, and provide links to each individual feature PRD.

## What Changes

- **Per-Feature PRD Generation**: Detect and group target repository functionality by distinct business domain (e.g., authentication, book management, loans/history, shared libraries) and write individual PRDs (`docs/features/<feature-name>.md`).
- **Master Module Context & Index Document**: Create/update the main module overview document (`docs/features/index.md`) containing global architecture context, system objectives, and an indexed catalog of all feature PRDs.

## Capabilities

### New Capabilities
- `per-feature-prd-catalog`: Batch domain feature PRD generation and master index orchestration.

### Modified Capabilities

## Impact

- `docs/features/`: Output directory for per-feature PRDs and the master index overview.
