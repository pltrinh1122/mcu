# PLAN: Extend MCU Specification with VIBE_NOTE MCU Type

- Created: 2025-08-09T00:00:00Z
- Owner: Operator
- Status: Draft (awaiting Operator approval)
- Scope: Specification, Templates, Validation, Existing file alignment

## 1) Objective
Introduce a new MCU Type, VIBE_NOTE (type: `note`), to formalize Operator notes as first-class MCUs with clear metadata, quality standards, and validation, while preserving the lightweight usage of `VIBE_NOTE.md` at the repo root.

## 2) Current State
- `docs/MCU_SPECIFICATION.md` defines types: `[reference|instruction|instruction-agent]`.
- No `note` type exists; `VIBE_NOTE.md` is an Operator notes file without MCU metadata.
- No template or type-specific quality standards for Operator notes.

## 3) Proposed Changes (Files)
- `docs/MCU_SPECIFICATION.md`
  - Extend type enum to include `note` in metadata examples and narrative.
  - Add `note` to the inheritance hierarchy diagram.
  - Mention Note-type quality extensions and cross-reference foundations.
- `reference/MCU_NOTE_SPECIFICATION.md` (new)
  - Specification for Note MCUs (audience: operator; scope: time-stamped decisions/instructions).
  - Define required metadata, content structure, and quality standards.
- `templates/MCU_NOTE_TEMPLATE.md` (new)
  - Reusable template with metadata header and standardized sections.
- `VIBE_NOTE.md` (existing)
  - Upgrade to a valid Note MCU instance by adding a metadata header (keep current timestamped content).
- `scripts/validate_mcu.py`
  - Recognize `note` as a valid type.
  - Optional: timestamp check for note entries (ISO 8601 UTC) when validating Note MCUs.

## 4) Type Definition: note (VIBE_NOTE)
- Purpose: Capture explicit Operator decisions/instructions with traceability.
- Audience: operator (primary), ai (secondary awareness).
- Required metadata (baseline):
  - `context_unit_id`: `note-[tool]-[date]-[sequence]`
  - `created_at`, `updated_at`: ISO 8601 UTC
  - `type`: `note`
  - `version`, `project`, `tool` (optional), `category`, `tags`
- Content structure:
  - Executive summary (optional for `VIBE_NOTE.md`)
  - Notes section containing timestamped entries
- Quality standards (type-specific):
  - 100% entries include ISO 8601 UTC timestamps in headings
  - Entries include scope and action/decision fields
  - Entries are clearly separated (horizontal rule or heading separation)

## 5) Implementation Steps
1. Update `docs/MCU_SPECIFICATION.md` to include `note` type and hierarchy.
2. Create `reference/MCU_NOTE_SPECIFICATION.md` (detailed spec: scope, metadata, content, quality, verification).
3. Create `templates/MCU_NOTE_TEMPLATE.md` (metadata header + note-entry scaffolding).
4. Update `scripts/validate_mcu.py` (add `note`; optional timestamp validation).
5. Update `VIBE_NOTE.md` (add MCU metadata header; retain current content and template).
6. Documentation pass (add cross-references; keep `[LINK]` placeholders until asked to update).

## 6) Validation
- Markdown: `markdownlint --disable MD013` for new/edited docs.
- Metadata: ensure Note-type required fields present.
- Optional timestamp validation (Operator-driven): regex `^## \[[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z\]` for each entry header.

## 7) Testing
- Focused tests:
  - `python -m py_compile scripts/*.py` if validator changes.
  - `scripts/check_links.py` only on Operator request.
- No CI or pre-commit hooks (per Operator decision).

## 8) Risks and Mitigations
- Naming/Scope drift: Keep `note` narrow—Operator notes only.
- Metadata burden: Allow minimal metadata for `VIBE_NOTE.md` while conforming to MCU.
- Backward compatibility: Preserve existing `VIBE_NOTE.md` content; additive metadata only.
- Tooling availability: Auto-install missing tools; pause if blocked and request Operator approval.

## 9) Success Criteria
- Base spec updated to enumerate `note` type and inheritance.
- New spec (`MCU_NOTE_SPECIFICATION.md`) and template created.
- Validator recognizes `note` type; optional timestamp check available.
- `VIBE_NOTE.md` upgraded with MCU metadata without disrupting usage.

## 10) Timeline (Proposed)
- Day 0: Approve this plan.
- Day 1: Implement docs/spec/template changes.
- Day 2: Update validator and add metadata to `VIBE_NOTE.md`.

## 11) Dependencies and Constraints
- Do not modify or migrate `__vibew-*` files.
- Defer security scanning and CI integration for now.
- OOP Python patterns apply only to new code.
- Maintain `[LINK]` placeholders until explicitly asked to update.

## 12) Open Questions
- Should `VIBE_NOTE.md` remain at repo root or move to `notes/` in future? (Default: remain at root.)
- Should timestamp validation be on by default or Operator-triggered? (Default: Operator-triggered.)

## 13) Approval
Operator approval required before executing the steps above.
