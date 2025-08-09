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

## [2025-08-09T16:18:55Z] Alignment Observations
- Scope: collaboration, alignment
- Decision/Instruction:
  - MCU serves as scaffolding to enable Operator to keep up and stay aligned with Agent while collaborating.
  - Human Operators have limited memory context, which is a primary cause for misalignment and for falling behind their Agent.
- Rationale: Establish shared mental models and durable context to reduce misalignment risk.
- Actions/Next Steps: Apply MCU structure consistently to shared artifacts to maintain alignment.
- References: `VIBE_CODING.md`, `docs/MCU_SPECIFICATION.md`

## [2025-08-09T16:20:31Z] Foundational Artifacts Inquiry
- Scope: repository, foundations
- Decision/Instruction: Identify foundational artifacts required for effective Operator–Agent collaboration.
- Rationale: Ensure minimum viable scaffolding is in place across repos.
- Actions/Next Steps:
  - Confirm baseline set: `VIBE_NOTE` (note MCU), `VIBE_CODING` (instruction-agent MCU), `MCU_SPECIFICATION` (base spec), `MCU_REFERENCE_SPECIFICATION` (reference spec), `MCU_INSTRUCTION-AGENT_SPECIFICATION` (agent spec), and a plan artifact (`__vibec-PLAN__*`).
  - Decide if additional foundation is required (e.g., `README` alignment section, `CONTRIBUTING` alignment rules).
- References: `VIBE_CODING.md`, `docs/MCU_SPECIFICATION.md`, `reference/MCU_REFERENCE_SPECIFICATION.md`, `instruction/instruction-agent/MCU_INSTRUCTION-AGENT_SPECIFICATION.md`

## [2025-08-09T16:24:48Z] Note Template Enhancement
- Scope: VIBE_NOTE template
- Decision/Instruction: The meta-label "Decision/Instruction" should be more general, e.g., "Body (decision/instruction/observation/etc.)"; consider a more appropriate, concise label.
- Rationale: Improve template flexibility to capture observations and other content types alongside decisions/instructions.
- Actions/Next Steps: Propose an updated template label in a follow-up change (pending Operator approval).
- References: `VIBE_NOTE.md`

## [2025-08-09T16:27:23Z] Note Template Optimization for Operator Consumption
- Scope: VIBE_NOTE template
- Decision/Instruction: Consider optimizing the template to place the most important content first (e.g., the main body text), followed by supporting metadata fields.
- Rationale: Prioritize Operator readability and speed of comprehension during collaboration.
- Actions/Next Steps: Draft a revised template order (body-first) for review and approval.
- References: `VIBE_NOTE.md`

## [2025-08-09T18:37:49Z] README as an MCU Type
- Scope: repository structure, MCU types
- Decision/Instruction: Explore converting `README.md` into an MCU type. How would it differ from other MCUs?
- Rationale: If README is a persistent cross-audience artifact, modeling it as an MCU type may align governance, metadata, and validation.
- Actions/Next Steps:
  - Draft a proposal outlining a `readme` MCU type vs. using existing `reference` type with a special role.
  - Compare metadata, content structure, and quality requirements.
  - Recommend whether to keep README as conventional repo doc or formalize as a specialized MCU.
- References: `README.md`, `docs/MCU_SPECIFICATION.md`, `reference/MCU_REFERENCE_SPECIFICATION.md`

## [2025-08-09T18:42:21Z] Explore Layer for Defining Used MCU Artifacts
- Scope: repository framework, layering
- Decision/Instruction: Explore the right layer (e.g., `VIBE_WORK`) MCU type responsible for defining the set of used MCU artifacts (e.g., `VIBE_CODING`, `VIBE_NOTE`, `README`, etc.).
- Rationale: Centralizing artifact definitions at the proper layer can improve discoverability, governance, and consistency across projects.
- Actions/Next Steps:
  - Draft a `VIBE_WORK` (or similar) MCU type concept with metadata to enumerate adopted artifacts and their roles.
  - Compare against existing `reference`/`instruction` scopes to prevent overlap.
  - Propose directory placement and template changes if adopted.
- References: `VIBE_CODING.md`, `docs/MCU_SPECIFICATION.md`, `README.md`

## [2025-08-09T18:44:12Z] VIBE_NOTE Usage and Roles
- Scope: VIBE_NOTE governance
- Decision/Instruction: Clarify VIBE_NOTE lifecycle and responsibilities.
  - Create: Operator or AI can create entries; AI should propose, Operator approves sensitive items.
  - Update: New entries are appended; existing timestamps are not retroactively changed unless explicitly approved by Operator.
  - Remove: Deletions require explicit Operator approval; AI may propose cleanup.
  - Timestamping: Always use ISO 8601 UTC (e.g., `2025-08-09T18:44:12Z`).
- Rationale: Ensure consistent, auditable collaboration and traceability.
- Actions/Next Steps: Reflect this lifecycle in `VIBE_CODING.md` usage guidance and in any future Note MCU spec.
- References: `VIBE_CODING.md`, `__vibec-PLAN__vibe_note_mcu_extension.md`
