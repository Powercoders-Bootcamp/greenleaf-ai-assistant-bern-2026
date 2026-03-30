# GreenLeaf AI Assistant Docs

## Recommended Reading Order

### Core Docs

These are the main documents the team should use day to day:

1. `01-project-overview.md`
2. `08-requirements-specification`
3. `10-target-architecture.md`
4. `15-security-access-control.md`
5. `14-qa-test-strategy.md`
6. `17-open-questions-register.md`
7. `22-backend-component-map.md`
8. `24-structured-llm-response-schema.md`
9. `25-backend-implementation-blueprint.md`
10. `26-ask-flow-sequence.md`
11. `backlog.md` in the repository root

### Working Docs

Use these during planning and implementation:

- `05-sprint-1-plan.md`

### Archived / Reference Docs

Older planning notes, duplicate summaries, and reference material live under `docs/archive/`.

They are kept for traceability, but they are not the primary source of truth anymore.

## Current Documentation Structure

- `01-project-overview.md`: product scope and business framing
- `08-requirements-specification`: functional and non-functional requirements
- `10-target-architecture.md`: architecture, routing, helper AI, and extensibility
- `14-qa-test-strategy.md`: QA, evaluation, and release quality checks
- `15-security-access-control.md`: security boundaries and disclosure policy
- `17-open-questions-register.md`: open questions, defaults, and stakeholder checklist
- `22-backend-component-map.md`: backend module map and request flow
- `24-structured-llm-response-schema.md`: structured draft format for the LLM-first architecture
- `25-backend-implementation-blueprint.md`: backend stack, folders, modules, and build order
- `26-ask-flow-sequence.md`: end-to-end backend sequence for a single ask request
- `05-sprint-1-plan.md`: current sprint guidance

## Documentation Rule

If two docs appear to overlap:

- prefer the document in the `Core Docs` list
- treat `docs/archive/` as historical context, not the active source of truth
