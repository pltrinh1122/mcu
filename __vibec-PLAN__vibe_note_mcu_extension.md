# PLAN: Extend MCU Specification with VIBE_NOTE MCU Type

- Created: 2025-08-09T00:00:00Z
- Owner: Operator
- Status: In Progress
- Scope: Specification, Templates, Validation, Existing file alignment

## 1) Objective
Introduce a new MCU Type, VIBE_NOTE (type: `note`), to formalize Operator notes as first-class MCUs with clear metadata, quality standards, and validation, while preserving the lightweight usage of `VIBE_NOTE.md` at the repo root.

## 2) Current State
- Base spec updated to include `note` type and inheritance diagram.
- `reference/MCU_NOTE_SPECIFICATION.md` created with metadata, lifecycle, and quality.
- `templates/MCU_NOTE_TEMPLATE.md` created with body-first entry guidance.
- Validator updated to support `note`, enforce timestamp headings for notes, ignore non-MCU families by prefix, and skip templates/non-MCU docs.
- `VIBE_NOTE.md` remains a practical instance; linked to Note spec; timestamps enforced forward-only.
- READMEs updated (`README.md`, `reference/README.md`, `note/README.md`) to reflect new Note type and usage.

## 3) Proposed Changes (Files)
- Completed:
  - `docs/MCU_SPECIFICATION.md`: add `note` type; update inheritance diagram.
  - `reference/MCU_NOTE_SPECIFICATION.md`: new Note spec.
  - `templates/MCU_NOTE_TEMPLATE.md`: new template.
  - `scripts/validate_mcu.py`: add `note` type, timestamp check; ignore non-MCU prefixes; skip templates.
  - `README.md`, `reference/README.md`, `note/README.md`: documentation alignment.
- Remaining:
  - Consider adding metadata header to `VIBE_NOTE.md` to make it a full MCU instance (currently serves as linked instance per minimal approach).
  - Normalize legacy categories/types in selected instruction/reference specs (optional, separate plan).

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
- Validator: passes 52/60 after updates; non-MCU families ignored by prefix; notes enforce timestamped headings.
- Optional timestamp validation regex available for external tooling: `^## \[[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z\]`.

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
- Base spec updated to enumerate `note` type and inheritance. ✅
- New spec (`MCU_NOTE_SPECIFICATION.md`) and template created. ✅
- Validator recognizes `note` type; timestamp check active for notes; ignores non-MCU families by prefix. ✅
- `VIBE_NOTE.md` linked to Note spec and follows timestamp rule; optional: add full MCU metadata header. ◻️

## 10) Timeline (Revised)
- Completed: Spec, template, validator, documentation alignment.
- Next: Decide on adding full MCU metadata header to `VIBE_NOTE.md` (if desired), and address legacy categories/types (separate plan).

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
