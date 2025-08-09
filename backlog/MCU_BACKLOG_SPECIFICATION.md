# Backlog MCU Specification

## Context Memory Unit: spec-backlog-2025-08-09-001
- **Created**: 2025-08-09T20:26:34Z
- **Updated**: 2025-08-09T22:10:36Z
- **Type**: specification
- **Version**: 1.0
- **Project**: MCU
- **Tool**: MCU
- **Category**: specification
- **Tags**: ["specification", "backlog", "governance"]

---

## Executive Summary

**TL;DR**: Defines the `backlog` MCU type to govern a collection of backlog items with prioritization, traceability, and basic integrity checks, enabling end-to-end flow from Notes → Backlog → Plan → Status.

---

## Quick Reference

### Essential Requirements
```yaml
type: backlog
audience: both
metadata: required
quality: governance
```

### Required Metadata
```yaml
metadata:
  context_unit_id: "backlog-[tool]-[YYYY-MM-DD]-[SEQ]"
  created_at: "ISO_TIMESTAMP"
  updated_at: "ISO_TIMESTAMP"
  type: "backlog"
  version: "[VERSION]"
  project: "MCU"
  tool: "[TOOL_NAME]"
  category: "governance"
  tags: ["backlog", "planning"]
```

---

## Detailed Reference

### Scope and Purpose
- Govern a collection of `backlog-item` MCUs for a repository or component
- Provide prioritization and status signaling; centralize links to items
- Define storage layout: backlog index files reside in `BACKLOGS/` (default: `BACKLOGS/BACKLOG_MAIN.md`); all backlog items reside under `BACKLOGS/ITEMS/` as individual files
 - Support multiple backlog index files in `BACKLOGS/` (e.g., `TEAM_ALPHA.md`, `ROADMAP_2025Q4.md`); when unspecified, `BACKLOGS/BACKLOG_MAIN.md` is the default

### Content Structure
- Executive Summary (purpose and scope)
- Backlog Overview (policy, prioritization scheme)
- Items Index (links to `backlog-item` MCUs)
  - Links MUST be relative paths to files under `ITEMS/` (e.g., `ITEMS/BLIT_SYS123_2025-08-09T23-59-59Z.md`)
- Orchestration Metadata (owned by backlog):
  - Priority/Rank and ordering
  - Scheduling window/milestones; release/PI targets
  - Dependencies (blocks/blocked-by graph)
  - Swimlane/team ownership
  - Program-level risk and aging signals
  - Workstreams (future-proofed):
    - Schema: id, name, exclusive (default true), preconditions, exit_criteria, depends_on (ids)
    - Assignment: active_workstreams[item_id] (enforced exclusive for now)
    - Concurrency: may be enabled later by setting exclusive=false per stream

#### Default Workstreams (recommended)

- Discovery
  - exclusive: true
  - preconditions: none
  - exit_criteria: sources curated (item.source_track == Curated)
- Definition
  - exclusive: true
  - preconditions: item.source_track == Curated
  - exit_criteria: item.definition_track == AC-Ready
- Planning
  - exclusive: true
  - preconditions: item.definition_track == AC-Ready
  - exit_criteria: PLAN linked and accepted (plan_link set; plan_status == Accepted)
- Delivery (Execution)
  - exclusive: true
  - preconditions: PLAN accepted (or Operator override)
  - exit_criteria: item.execution_track == Completed
- Validation
  - exclusive: true
  - preconditions: item.execution_track == Completed
  - exit_criteria: item.validation_track == Explicit-Accepted
- Release
  - exclusive: true
  - preconditions: item.validation_track == Explicit-Accepted
  - exit_criteria: integration evidence shows deployed/monitored
- Closure
  - exclusive: true
  - preconditions: item.validation_track == Explicit-Accepted
  - exit_criteria: item.closure_track == Archived
- Reporting (optional): counts by state, aging metrics, rollups

### Quality Standards
- 100% items listed have valid links
- Clear prioritization cues (field or section)
- Timestamp accuracy (ISO 8601 UTC)
- No duplication of item-owned tracks (execution/definition/validation/docs). Backlog only references item evidence and computes rollups.
 - Index link paths are relative and resolve to files under `BACKLOGS/ITEMS/`

---

## Integration

### Cross-References
- Links to constituent `backlog-item` MCUs stored under `BACKLOGS/ITEMS/`
- Optional links forward to PLAN/STATUS where applicable via items
- Rollups derived from item tracks (e.g., In-Progress, Completed, Accepted) for dashboards

- Minimal structural checks: Items Index present with at least one link when non-empty; referenced items should be under `BACKLOGS/ITEMS/`
- Optional integrity checks (advisory): if orchestration metadata present, ensure referenced items exist; do not require item-level execution fields here

---

## Sources & Verification
- Based on MCU governance patterns and VIBE_CODING workflow

---

*Backlog MCUs establish lightweight governance for pre-execution work management.*
