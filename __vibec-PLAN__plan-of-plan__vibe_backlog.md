# PLAN: Extend MCU with VIBE_BACKLOG and VIBE_BACKLOG_ITEM Types

- Created: 2025-08-09T19:52:30Z
- Owner: Operator
- Status: Draft (awaiting Operator approval)
- Scope: Specification, Templates, Validator, Repository Integration

## 1) Objective
Introduce two new MCU types to formalize backlog management and traceability:
- `VIBE_BACKLOG`: a collection-type MCU governing a set of backlog items
- `VIBE_BACKLOG_ITEM`: an atomic MCU representing a single backlog entry that references source notes and links to PLAN/STATUS

## 2) Current State
- No backlog-specific MCU types exist.
- Notes are captured in `VIBE_NOTE.md`; plans use `__vibec-PLAN__*`; statuses use `__vibew-STATUS__*`.
- Validator recognizes types: reference, instruction, instruction-agent, specification, note.

## 3) Proposed Changes (Files)
- `docs/MCU_SPECIFICATION.md`
  - Add `backlog` and `backlog-item` to the type list and narrative examples
  - Extend inheritance diagram to include Backlog and Backlog Item specifications
- `reference/MCU_BACKLOG_SPECIFICATION.md` (new)
  - Defines metadata, structure, and quality for the collection type
  - Specifies relationships to Backlog Items (composition) and reporting
- `reference/MCU_BACKLOG_ITEM_SPECIFICATION.md` (new)
  - Defines metadata, structure, and quality for atomic backlog items
  - Requires references to sources (e.g., VIBE_NOTE entries), target PLAN, and STATUS
- `templates/MCU_BACKLOG_TEMPLATE.md` (new)
  - Provides a scaffold for a project backlog document with a curated list and cross-links
- `templates/MCU_BACKLOG_ITEM_TEMPLATE.md` (new)
  - Provides a scaffold for a single backlog item with required metadata and links
- `scripts/validate_mcu.py`
  - Add `backlog` and `backlog-item` to valid types
  - Minimal structure checks:
    - Backlog: must have a list/section of item references
    - Backlog Item: must include at least one source reference and optional PLAN/STATUS targets
- Documentation updates
  - `README.md`: document new types and how to create them
  - `reference/README.md`: list the new specifications

## 4) Type Definitions

### 4.1 VIBE_BACKLOG (type: `backlog`)
- Purpose: Govern a collection of backlog items with prioritization and traceability
- Audience: both
- Required metadata (baseline):
  - `context_unit_id`: `backlog-[tool]-[YYYY-MM-DD]-[SEQ]`
  - `created_at`, `updated_at`: ISO 8601 UTC
  - `type`: `backlog`
  - `version`, `project`, `tool`, `category`, `tags`
- Content structure:
  - Executive summary
  - Backlog Overview (policy, prioritization scheme)
  - Items Index (links to VIBE_BACKLOG_ITEM MCUs)
  - Reporting (e.g., counts by status, aging)
- Quality:
  - 100% items listed with valid references
  - Clear prioritization and status signals

### 4.2 VIBE_BACKLOG_ITEM (type: `backlog-item`)
- Purpose: Represent a single backlog entry with full lineage and execution targets
- Audience: both
- Required metadata (baseline):
  - `context_unit_id`: `backlog-item-[tool]-[YYYY-MM-DD]-[SEQ]`
  - `created_at`, `updated_at`: ISO 8601 UTC
  - `type`: `backlog-item`
  - `version`, `project`, `tool`, `category`, `tags`
- Content structure:
  - Summary (title, objective, acceptance criteria)
  - Source references (links to note entries or docs)
  - Execution links (PLAN id/path, STATUS id/path) when applicable
  - Priority and sizing (optional)
- Quality:
  - At least one source reference required
  - If in execution, must link PLAN; if completed/ongoing, link STATUS

## 5) Implementation Steps
1. Update `docs/MCU_SPECIFICATION.md` (types + inheritance diagram)
2. Create `reference/MCU_BACKLOG_SPECIFICATION.md`
3. Create `reference/MCU_BACKLOG_ITEM_SPECIFICATION.md`
4. Add templates: `templates/MCU_BACKLOG_TEMPLATE.md`, `templates/MCU_BACKLOG_ITEM_TEMPLATE.md`
5. Update `scripts/validate_mcu.py` (types + minimal structure checks for backlog/backlog-item)
6. Documentation pass: `README.md`, `reference/README.md`
7. (Optional) Create a seed `VIBE_BACKLOG.md` using the template and link example items

## 6) Validation
- Markdown: `markdownlint --disable MD013`
- Validator:
  - Recognize `backlog` and `backlog-item`
  - Backlog: must include an Items Index section with links
  - Backlog Item: must include a Source References section with at least one link

## 7) Testing
- Focused tests:
  - `python -m py_compile scripts/*.py` if validator changes
  - Spot-run validator on new specs, templates, and any seed backlog docs

## 8) Risks and Mitigations
- Overlap with existing artifacts (PLAN/STATUS):
  - Mitigation: Clear boundaries; backlog is pre-execution governance; PLAN/STATUS are execution artifacts
- Validator strictness:
  - Mitigation: Minimal checks initially; iterate with usage feedback
- Link rot in references:
  - Mitigation: Optional link checker (`scripts/check_links.py`) on demand

## 9) Success Criteria
- Base spec updated to include `backlog` and `backlog-item`
- Backlog and Backlog Item specifications and templates created
- Validator supports both types with minimal structure checks
- Docs updated to explain creation and usage

## 10) Timeline
- Day 0: Approve plan
- Day 1: Implement specs/templates and base spec updates
- Day 2: Update validator and docs; optional seed backlog

## 11) Dependencies and Constraints
- Keep `[LINK]` placeholders until instructed to resolve
- Do not modify `__vibew-*` families; validator already ignores them
- OOP Python patterns apply only to new code
- Timestamp rule: ISO 8601 UTC with trailing Z for new/updated fields

## 12) Open Questions
- Should we seed a `VIBE_BACKLOG.md` at repo root, or place backlogs under a dedicated `backlog/` directory?
- Should backlog prioritization schema be standardized (e.g., MoSCoW) or left flexible?
- Should validator enforce acceptance criteria presence for backlog items?

## 13) Approval
Operator approval required before executing the steps above.
