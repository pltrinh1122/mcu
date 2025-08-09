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

### Content Structure
- Executive Summary (purpose and scope)
- Backlog Overview (policy, prioritization scheme)
- Items Index (links to `backlog-item` MCUs)
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
- Reporting (optional): counts by state, aging metrics, rollups

### Quality Standards
- 100% items listed have valid links
- Clear prioritization cues (field or section)
- Timestamp accuracy (ISO 8601 UTC)
- No duplication of item-owned tracks (execution/definition/validation/docs). Backlog only references item evidence and computes rollups.

---

## Integration

### Cross-References
- Links to constituent `backlog-item` MCUs
- Optional links forward to PLAN/STATUS where applicable via items
- Rollups derived from item tracks (e.g., In-Progress, Completed, Accepted) for dashboards

### Validation
- Minimal structural checks: Items Index present with at least one link when non-empty
- Optional integrity checks (advisory): if orchestration metadata present, ensure referenced items exist; do not require item-level execution fields here

---

## Sources & Verification
- Based on MCU governance patterns and VIBE_CODING workflow

---

*Backlog MCUs establish lightweight governance for pre-execution work management.*
