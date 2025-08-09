# PLAN: Plan-of-Plan – VIBE_BACKLOG and VIBE_BACKLOG_ITEM Introduction
> Archived on 2025-08-09T21:38:23Z – reason: avoid clutter in working directory space

- Created: 2025-08-09T19:52:30Z
- Owner: Operator
- Status: ARCHIVE
- Scope: Orchestration of related plans (specs, templates, validator, docs)
- Orchestration: true
- Plan_Level: 2

## 0) Plan Status Dashboard
- Unified view across constituent PLANs (P1–P6):
  - [ACCEPTED] P1 – Base Spec Update [__vibec-PLAN__P1_base_spec_update.md](__vibec-PLAN__P1_base_spec_update.md)
  - [ACCEPTED] P2 – Backlog Specification [__vibec-PLAN__P2_backlog_spec.md](__vibec-PLAN__P2_backlog_spec.md)
  - [ACCEPTED] P3 – Backlog Item Specification [__vibec-PLAN__P3_backlog_item_spec.md](__vibec-PLAN__P3_backlog_item_spec.md)
  - [ACCEPTED] P4 – Backlog Templates [__vibec-PLAN__P4_templates.md](__vibec-PLAN__P4_templates.md)
  - [ACCEPTED] P5 – Validator Support [__vibec-PLAN__P5_validator_support.md](__vibec-PLAN__P5_validator_support.md)
  - [ACCEPTED] P6 – Docs Integration [__vibec-PLAN__P6_docs_integration.md](__vibec-PLAN__P6_docs_integration.md)

## 1) Objective
Coordinate the introduction of two new MCU types and their integration across the repository:
- `VIBE_BACKLOG`: a collection-type MCU governing a set of backlog items
- `VIBE_BACKLOG_ITEM`: an atomic MCU representing a single backlog entry that references source notes and links to PLAN/STATUS

## 1.1 Analysis & Strategy (Why)
- Establish end-to-end traceability from Notes → Backlog → Plan → Status to improve governance and accountability
- Keep validator checks minimal initially to avoid friction while ensuring basic integrity (presence of links/sections)
- Clarify boundaries: backlog is a pre-execution governance artifact; plan/status are execution artifacts
- Alternatives considered: non-MCU backlog (rejected for governance gaps); strict validator (deferred to avoid slowdown)

## 1.2 Constraints & Assumptions
- Keep `[LINK]` placeholders per project policy; ignore `__vibew-*` families in validator
- ISO 8601 UTC timestamps with trailing Z
- No CI/hooks changes in this iteration

## 2) Constituent Plans (Parallel-Capable)
- P1 Base Spec Update → `__vibec-PLAN__P1_base_spec_update.md`
- P2 Backlog Spec → `__vibec-PLAN__P2_backlog_spec.md`
- P3 Backlog Item Spec → `__vibec-PLAN__P3_backlog_item_spec.md`
- P4 Templates → `__vibec-PLAN__P4_templates.md`
- P5 Validator Support → `__vibec-PLAN__P5_validator_support.md`
- P6 Docs Integration → `__vibec-PLAN__P6_docs_integration.md`
- Optional P7 Seed Instance → `VIBE_BACKLOG.md` (using template)

Note: No hard dependencies/gates among constituent PLANs. Soft synchronization is advisory only.

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

## 5) Orchestrated Implementation Steps (High-Level)
- M1 Approve Analysis & Strategy, scope, and naming
- M2 Execute P1 (foundation)
- M3 Execute P2 and P3 in parallel (no gates)
- M4 Execute P4 (templates)
- M5 Execute P5 and P6; run validator for repository-wide sanity
- M6 Optional P7: create seed backlog and example items; run validator

Shared Validations:
- Run validator after M3, M4, M5; use link-checks on demand (`scripts/check_links.py`)

## 6) Validation
- Markdown: `markdownlint --disable MD013`
- Validator:
  - Recognize `backlog` and `backlog-item`
  - Backlog: must include an Items Index section with links
  - Backlog Item: must include a Source References section with at least one link
 - Key Consistency (sub-PLANs): `orchestration: false` is only valid with `plan_level: 1`; this POP uses `orchestration: true` with `plan_level: 2`

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
- Day 0: Approve PLAN-of-PLAN (M1)
- Day 1: M2 (P1) → M3 (P2, P3) → M4 (P4)
- Day 2: M5 (P5, P6) → M6 (P7 optional)

## Conflict Resolution
- Integration conflicts/contention are coordinated in this POP. Agent proposes options with pros/cons; Operator makes final decision.

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
