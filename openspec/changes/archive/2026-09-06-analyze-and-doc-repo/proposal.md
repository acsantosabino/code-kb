## Why

The target project/repository needs to be systematically analyzed to identify all existing features, modules, and business capabilities, and document each feature one by one into structured PRDs (Product Requirement Documents) in `docs/features/`. Currently, feature documentation may be missing, partial, or unstandardized. By executing a full repository analysis and leveraging the feature documentation tooling (`rag-legado-doc`), we ensure comprehensive knowledge preservation and clear technical specifications.

## What Changes

- **Repository Analysis & Feature Discovery**: Conduct a full structural and semantic analysis of the target repository to infer all core modules and features.
- **Automated PRD Generation Strategy**: Establish a systematic workflow for iterating through discovered features and generating standardized PRD documentation (`docs/features/<feature-name>.md`) using TDD and RAG-enhanced retrieval.
- **Verification & Gap Filling**: Ensure every inferred feature is fully documented with requirements, architecture, API definitions, test strategies, and business rules.

## Capabilities

### New Capabilities
- `auto-feature-documentation`: Automatic repository feature inference and batch PRD documentation workflow.

### Modified Capabilities

## Impact

- `docs/features/`: Output directory where individual feature PRDs will be stored.
- `rag-legado-doc` skill and underlying tooling: Used for indexing and generating context-aware PRD documentation.
