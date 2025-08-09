# Backlog Item MCU Specification

## Context Memory Unit: spec-backlog-item-2025-08-09-001
- **Created**: 2025-08-09T20:26:34Z
- **Updated**: 2025-08-09T21:59:28Z
- **Type**: specification
- **Version**: 1.0
- **Project**: MCU
- **Tool**: MCU
- **Category**: specification
- **Tags**: ["specification", "backlog-item", "governance"]

---

## Executive Summary

**TL;DR**: Defines the `backlog-item` MCU type to represent a single backlog entry with source lineage and optional execution links to PLAN and STATUS.

---

## Quick Reference

### Essential Requirements
```yaml
type: backlog-item
audience: both
metadata: required
quality: governance
```

### Required Metadata
```yaml
metadata:
  context_unit_id: "backlog-item-[tool]-[YYYY-MM-DD]-[SEQ]"
  created_at: "ISO_TIMESTAMP"
  updated_at: "ISO_TIMESTAMP"
  type: "backlog-item"
  version: "[VERSION]"
  project: "MCU"
  tool: "[TOOL_NAME]"
  category: "governance"
  tags: ["backlog-item", "planning"]
```

---

## Detailed Reference

### Scope and Purpose
- Capture a unit of planned work with clear lineage and potential execution path

### Content Structure
- Summary (title/objective/acceptance criteria)
- Source References (links to `VIBE_NOTE` entries or docs) – at least one required
- Execution Links (optional): PLAN id/path, STATUS id/path
- Tracks (authoritative on item; parallel-capable):
  - source_track: Captured | Curated
  - definition_track: Triaged | Clarified | Sized | AC-Ready
  - execution_track: Not-Started | In-Progress | Blocked | Completed
  - validation_track: Implicit-Validated | Explicit-Accepted
  - docs_track: Docs-Added | Examples-Linked
  - integration_evidence: PR/Deploy links
- Do not duplicate backlog-owned orchestration (priority, scheduling, dependencies, rollups). Link to backlog for those.

### Quality Standards
- At least one source reference present
- If in execution, include PLAN link; if completed/ongoing, include STATUS link
- Timestamp accuracy (ISO 8601 UTC)
- No orchestration fields on item (priority, scheduling, dependency graph, rollup). Those are backlog-owned.

---

## Integration

### Cross-References
- Backward: source notes or docs
- Forward: links to PLAN and STATUS if applicable
- Backlog link: reference the governing backlog that orchestrates this item (optional if single backlog in repo)

### Validation
- Minimal structural checks: Source References section with ≥1 link

---

## Sources & Verification
- Based on MCU governance patterns and VIBE_CODING workflow

---

*Backlog Item MCUs provide lineage and execution linkage for planned work.*
