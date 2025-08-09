# Note MCUs

## Overview

This directory is reserved for Note MCUs that formalize Operator notes with timestamped entries and lightweight governance.

## Purpose

- Centralize note-type artifacts
- Ensure consistent metadata and timestamping
- Provide clear lifecycle and roles (Operator/AI)

## Getting Started

1. Use `templates/MCU_NOTE_TEMPLATE.md` to create a new Note MCU
2. Follow `reference/MCU_NOTE_SPECIFICATION.md` for required metadata and structure
3. Validate with `python scripts/validate_mcu.py note/` (optional)

## Conventions

- ISO 8601 UTC timestamps in headings: `## [YYYY-MM-DDTHH:MM:SSZ] Title`
- Body-first entry format for Operator readability
- Append new entries; avoid modifying historical timestamps unless approved

---

*Note MCUs implement lightweight governance for Operator-AI collaboration.*
