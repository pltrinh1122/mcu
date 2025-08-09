# [BACKLOG TITLE]

## Context Memory Unit: backlog-[tool]-[YYYY-MM-DD]-[SEQ]
- **Created**: [ISO_UTC]
- **Updated**: [ISO_UTC]
- **Type**: backlog
- **Version**: 1.0
- **Project**: MCU
- **Tool**: [TOOL_NAME]
- **Category**: governance
- **Tags**: ["backlog", "planning"]

---

## Executive Summary
[One-liner purpose of the backlog]

## Backlog Overview
- Policy/prioritization scheme:
- Signals/labels:

## Workstreams (recommended defaults; edit as needed)
- Discovery: exclusive=true; pre: none; exit: source_track == Curated
- Definition: exclusive=true; pre: source_track == Curated; exit: definition_track == AC-Ready
- Planning: exclusive=true; pre: definition_track == AC-Ready; exit: PLAN linked & accepted
- Delivery (Execution): exclusive=true; pre: PLAN accepted; exit: execution_track == Completed
- Validation: exclusive=true; pre: execution_track == Completed; exit: validation_track == Explicit-Accepted
- Release: exclusive=true; pre: validation_track == Explicit-Accepted; exit: deployed/monitored
- Closure: exclusive=true; pre: validation_track == Explicit-Accepted; exit: closure_track == Archived

## Items Index
- [ ] [backlog-item-...](ITEMS/path-to-item.md)
- [ ] [backlog-item-...](ITEMS/path-to-item.md)

## Conventions
- Place this index file in `BACKLOGS/` (default index: `BACKLOG_MAIN.md`).
- Item links MUST be relative paths to `ITEMS/`.

## Reporting (optional)
- Counts by state:
- Aging metrics:
