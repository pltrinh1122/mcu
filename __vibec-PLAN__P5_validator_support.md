# PLAN: P5 – Validator Support for Backlog Types

- Created: 2025-08-09T20:26:34Z
- Owner: Operator
- Status: Draft
- Scope: scripts/validate_mcu.py

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

## Risks
- Over-strict checks causing friction; mitigate by keeping checks minimal initially

## Success Criteria
- Validator accepts both types and enforces minimal structure
