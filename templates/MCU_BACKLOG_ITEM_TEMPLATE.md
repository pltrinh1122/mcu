# [BACKLOG ITEM TITLE]

## Context Memory Unit: backlog-item-[tool]-[YYYY-MM-DD]-[SEQ]
- **Created**: [ISO_UTC]
- **Updated**: [ISO_UTC]
- **Type**: backlog-item
- **Version**: 1.0
- **Project**: MCU
- **Tool**: [TOOL_NAME]
- **Category**: governance
- **Tags**: ["backlog-item", "planning"]

---

## Summary
- Objective:
- Acceptance Criteria:

## Source References (≥1)
- [VIBE_NOTE entry link]

## Lineage (optional)
- Derived-from: [original item link]
- Superseded-by: [links to new or consolidated items]

## Execution Links (optional)
- PLAN: [link]
- POP: [link]
- STATUS: [link]

## Tracks (authoritative on item)
- source_track: [Captured|Curated]
- definition_track: [Triaged|Clarified|Sized|AC-Ready]
- execution_track: [Not-Started|In-Progress|Blocked|Completed]
- validation_track: [Implicit-Validated|Explicit-Accepted]
- docs_track: [Docs-Added|Examples-Linked]
- integration_evidence: [PR/Deploy links]
- defer_track: [Deferred|Permanently-Deferred]
- defer_status: [free-text, e.g., next quarter]
- defer_until: [YYYY-MM-DD]

## Workstreams (read-only, derived from backlog)
- current_workstream_id: [optional]
- completed_workstreams: [ids]

## Storage
- Place this file under `BACKLOGS/ITEMS/` (one file per item)

## Filename Convention
 - Use a concise, unique filename: `BLIT_[systemID]_[timestamp].md` (ISO 8601 UTC with trailing Z; colon-safe: `YYYY-MM-DDTHH-MM-SSZ`). `[systemID]` must be alphanumeric/underscore only (`^[A-Za-z0-9_]+$`).

### Default SystemID (shell)
Pairs may personalize `systemID`; default derivation:

```bash
if command -v hostid >/dev/null 2>&1; then
  SYSTEMID=$(hostid)
elif [ -r /etc/machine-id ]; then
  SYSTEMID=$(cut -c1-8 /etc/machine-id)
else
  SYSTEMID=$(uname -n | tr -c 'A-Za-z0-9' '_' | cut -c1-16)
fi
SYSTEMID=$(echo "$SYSTEMID" | tr '[:lower:]' '[:upper:]')
```

## Disposition (optional, for split/merge outcomes)
- Disposition: [Superseded (Split)|Superseded (Merged)|Superseded (Bundled)]
- Notes: [brief explanation]
