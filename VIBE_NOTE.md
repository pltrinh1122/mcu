# VIBE NOTE (OPERATOR)

Explicit Operator notes for the repository. Each entry must include an ISO 8601 UTC timestamp.

## How to add a note

## [YYYY-MM-DDTHH:MM:SSZ] Short title
- Scope: area/component
- Decision/Instruction: what was decided or instructed
- Rationale: why
- Actions/Next Steps: who does what, by when
- References: links or file paths

---

## Notes

<!-- Add new notes below this line using the template above -->

## [2025-08-09T16:02:41Z] MCU Type Observations
- Scope: repository, MCU framework
- Decision/Instruction: PLAN and similar artifacts are also MCU types; SPECIFICATION is also a type of MCU; any artifact consumable by both Operator and AI should be modeled as an MCU type.
- Rationale: Ensure consistent governance, metadata, validation, and discoverability across shared artifacts.
- Actions/Next Steps:
  - Proceed with the existing PLAN to introduce the `note` MCU type.
  - Consider analogous updates to enumerate `plan` and `specification` MCU types in the base spec (pending Operator approval).
  - Keep `[LINK]` placeholders as-is and do not modify `__vibew-*` files.
- References: `__vibec-PLAN__vibe_note_mcu_extension.md`, `docs/MCU_SPECIFICATION.md`
