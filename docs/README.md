# GreenLeaf AI Assistant Docs

## Recommended Reading Order

### Core Docs

These are the main documents the team should use day to day:

1. `01-project-overview.md`
2. `02-requirements-specification.md`
3. `03-target-architecture.md`
4. `04-security-access-control.md`
5. `05-qa-test-strategy.md`
6. `06-structured-llm-response-schema.md`
7. `07-backend-implementation-blueprint.md`
8. `backlog.md` in the repository root

### Working Docs

Use these during planning and implementation:

- `09-sprint-1-plan.md`

### Archived / Reference Docs

Older planning notes, duplicate summaries, and reference material live under `docs/90-archive/`.

They are kept for traceability, but they are not the primary source of truth anymore.

## Current Documentation Structure

- `01-project-overview.md`: product scope and business framing
- `02-requirements-specification.md`: functional and non-functional requirements
- `03-target-architecture.md`: architecture, routing, helper AI, and extensibility
- `04-security-access-control.md`: security boundaries and disclosure policy
- `05-qa-test-strategy.md`: QA, evaluation, and release quality checks
- `06-structured-llm-response-schema.md`: structured draft format for the LLM-first architecture
- `07-backend-implementation-blueprint.md`: backend stack, folders, modules, and build order

## Current Diagram Files

The diagram files currently present are:

- `docs/diagrams/01-high-level-system-architecture-diagram.png`
- `docs/diagrams/02-ask-flow-sequence-diagram.png`
- `docs/diagrams/03-validator-decision-flow-diagram.png`

## Documentation Rule

If two docs appear to overlap:

- prefer the document in the `Core Docs` list
- treat `docs/archive/` as historical context, not the active source of truth
