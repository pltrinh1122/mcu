# Note MCU Specification

## Context Memory Unit: spec-note-mcu-2025-08-09-001
- **Created**: 2025-08-09T18:51:20Z
- **Updated**: 2025-08-09T18:51:20Z
- **Type**: specification
- **Version**: 1.0
- **Project**: MCU
- **Tool**: MCU
- **Category**: framework
- **Tags**: ["specification", "note", "governance"]

---

## Executive Summary

**TL;DR**: Defines the Note MCU type for Operator notes and time-stamped guidance with minimal metadata, lifecycle clarity, and auditability.

## Quick Reference

### **Essential Requirements**
```yaml
type: note
audience: [operator|ai|both]
metadata: required
quality: lifecycle_audit
```

### **Required Metadata**
```yaml
metadata:
  context_unit_id: "note-[tool]-[date]-[sequence]"
  created_at: "ISO_TIMESTAMP"
  updated_at: "ISO_TIMESTAMP"
  type: "note"
  version: "[VERSION]"
  project: "MCU"
  tool: "[TOOL_NAME]"
  category: "governance"
  tags: ["note", "operator"]
```

---

## Detailed Reference

### **Scope and Purpose**
- Capture Operator decisions, instructions, and observations with ISO 8601 UTC timestamps
- Provide lightweight governance and traceability for collaboration

### **Content Structure**
- Executive summary (optional)
- Notes section with entries formatted as:
  - `## [YYYY-MM-DDTHH:MM:SSZ] Title`
  - Body
  - Optional: Scope, Rationale, Actions, References

### **Lifecycle and Roles**
- Create: AI may draft; Operator approves sensitive entries
- Update: Append new entries; do not alter prior timestamps unless explicitly approved
- Remove: Requires explicit Operator approval; AI may propose cleanup
- Timestamping: Use ISO 8601 UTC with trailing `Z`

### **Quality Standards**
- 100% entries include ISO 8601 UTC timestamp in the heading
- Clear separation between entries (heading or horizontal rule)
- Entries include sufficient context (body first recommended)

---

## Integration

### **Cross-Reference**
- Link from `VIBE_NOTE.md` to relevant plan, spec, and workflow docs
- Reference from base spec inheritance diagram

### **Verification**
- Optional validator rule to check timestamps on headings

---

## Sources & Verification
- Based on repository governance requirements and `VIBE_CODING.md` timestamp rule

---

*Note MCUs implement lightweight governance for Operator-AI collaboration.*


