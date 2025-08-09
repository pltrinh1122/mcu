# PLAN: P5 – Validator Support for Backlog Types
> Archived on 2025-08-09T21:43:16Z – reason: avoid clutter in working directory space

## 0) Plan Status Dashboard
- [ARCHIVE] P5 – Validator Support [`scripts/validate_mcu.py`](scripts/validate_mcu.py)

- Created: 2025-08-09T20:26:34Z
- Owner: Operator
- Status: ARCHIVE
- Scope: scripts/validate_mcu.py
- Orchestration: false
- Plan_Level: 1

## Objective
Add `backlog` and `backlog-item` types and minimal structure checks.

## Steps
1. Extend valid types list
2. Implement minimal checks:
   - Backlog: Items Index section present
   - Backlog Item: Source References section with at least one link
3. Keep templates and non-MCU families ignored

## Validation
- `python -m py_compile scripts/validate_mcu.py`
- Run validator against repo
- Key Consistency: `orchestration: false` must pair with `plan_level: 1`

## Risks
- Over-strict checks causing friction; mitigate by keeping checks minimal initially

## Success Criteria
- Validator accepts both types and enforces minimal structure

