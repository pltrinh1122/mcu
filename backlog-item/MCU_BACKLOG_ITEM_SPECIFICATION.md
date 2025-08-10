# Backlog Item MCU Specification

## Context Memory Unit: spec-backlog-item-2025-08-09-001
- **Created**: 2025-08-09T20:26:34Z
- **Updated**: 2025-08-09T22:10:36Z
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
- Lineage (optional): Derived-from (links to origin items), Superseded-by (links to successor items)
- Execution Links (optional): PLAN id/path, STATUS id/path
- Tracks (authoritative on item; parallel-capable):
  - source_track: Captured | Curated
  - definition_track: Triaged | Clarified | Sized | AC-Ready
  - execution_track: Not-Started | In-Progress | Blocked | Completed
  - validation_track: Implicit-Validated | Explicit-Accepted
  - docs_track: Docs-Added | Examples-Linked
  - integration_evidence: PR/Deploy links
  - defer_track: Deferred | Permanently-Deferred
  - defer_status (optional): Free-text classification (e.g., "next release", "next quarter")
  - defer_until (optional): ISO date (YYYY-MM-DD)
- Do not duplicate backlog-owned orchestration (priority, scheduling, dependencies, rollups). Link to backlog for those.
 - Workstream annotations (read-only, future-proof):
   - current_workstream_id (optional): set by backlog assignment
   - completed_workstreams (optional set of ids): derived from backlog
   - Note: Items MUST NOT own workstream assignment logic; fields are informational only.

### Quality Standards
- At least one source reference present
- If in execution, include PLAN link; if completed/ongoing, include STATUS link
- Timestamp accuracy (ISO 8601 UTC)
- No orchestration fields on item (priority, scheduling, dependency graph, rollup). Those are backlog-owned.
 - Filename convention: concise and unique `BLIT_[systemID]_[timestamp].md`; timestamp uses colon-safe ISO 8601 with trailing Z (`YYYY-MM-DDTHH-MM-SSZ`); `[systemID]` must match `^[A-Za-z0-9_]+$`
 - If `defer_track` is set to Deferred, it is recommended to set `defer_status` and/or `defer_until` for clarity. `Permanently-Deferred` indicates closure-equivalent intent.
 - Default `systemID` derivation (recommended algorithm):
   - Prefer `hostid`; else first 8 of `/etc/machine-id`; else sanitized `uname -n` (uppercase; non-alphanumerics as underscore; capped length)
 - If an item is split/merged/bundled, original item records a Disposition and Superseded-by links; successor items include Derived-from link(s)

---

## Integration

### Cross-References
- Backward: source notes or docs
- Forward: links to PLAN and STATUS if applicable
- Backlog link: reference the governing backlog that orchestrates this item (optional if single backlog in repo)
 - Storage: items live under `BACKLOGS/ITEMS/` (one file per item)

### Validation
- Minimal structural checks: Source References section with ≥1 link

---

## Sources & Verification
- Based on MCU governance patterns and VIBE_CODING workflow

---

*Backlog Item MCUs provide lineage and execution linkage for planned work.*
