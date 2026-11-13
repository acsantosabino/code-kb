## 1. Validate Planning Artifacts

- [ ] 1.1 Validate that `specs/system-capabilities/spec.md` follows OpenSpec requirements (all requirements have scenarios, proper header formatting)
- [ ] 1.2 Verify that all twelve requirements from the six source specs are present in the consolidated spec
- [ ] 1.3 Verify that `design.md` and `tasks.md` are complete and cross-referenced correctly
- [ ] 1.4 Run `openspec validate --change "consolidate-current-capabilities"` to confirm all planning artifacts pass validation

## 2. Archive and Generate Finalized Spec

- [ ] 2.1 Run `openspec archive --change "consolidate-current-capabilities"` to generate the finalized spec in `openspec/specs/system-capabilities/spec.md`
- [ ] 2.2 Verify that the archived spec exists at `openspec/specs/system-capabilities/spec.md`
- [ ] 2.3 Verify that the change is moved from `openspec/changes/` to `openspec/archive/` with current date stamp
- [ ] 2.4 Review the archived spec to confirm it matches the change's delta spec and all requirements are intact

## 3. Finalization and Documentation

- [ ] 3.1 Verify that `openspec/specs/` now contains the new `system-capabilities/` directory alongside existing capability specs
- [ ] 3.2 (Optional) Update project architecture documentation or README to reference the new unified `system-capabilities` spec
- [ ] 3.3 Confirm no changes were made to implementation code in `rag-legado-skill/` (consolidation is spec-only)
