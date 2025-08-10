#!/usr/bin/env python3
import os
import shutil
import tempfile
import unittest
from pathlib import Path
import json

from blit_convert import md_to_json, json_to_md


SAMPLE_ID = 'BLIT_TESTPAIR_2025-01-01T00-00-00Z'
SAMPLE_CONTEXT_ID = 'backlog-item-mcu-2025-01-01-001'

SAMPLE_MD = f"""# Example Item — Discovery

## Context Memory Unit: {SAMPLE_CONTEXT_ID}
- **Created**: 2025-01-01T00:00:00Z
- **Updated**: 2025-01-01T00:00:00Z
- **Type**: backlog-item
- **Version**: 1.0
- **Project**: MCU
- **Tool**: BACKLOG
- **Category**: governance
- **Tags**: ["backlog-item", "discovery"]

---

## Summary
- Objective: Example objective
- Acceptance Criteria:
  - Link to note
  - Draft scope

## Source References (≥1)
- [VIBE_NOTE: 2025-01-01T00-00-00Z](../../VIBE_NOTE.md#note-2025-01-01T00-00-00Z)

## Execution Links (optional)
- PLAN: 
- POP: 
- STATUS: 

## Tracks (authoritative on item)
- source_track: Captured
- definition_track: Triaged
- execution_track: Not-Started
- validation_track: Implicit-Validated
- docs_track: 
- integration_evidence: 
- defer_track: 
- defer_status: 
- defer_until: 

## Workstreams (read-only, derived from backlog)
- current_workstream_id: 
- completed_workstreams: 
"""


SAMPLE_JSON = {
    "$schema": "blit_schema.json",
    "schema_version": "1.0",
    "id": SAMPLE_ID,
    "title": "Example Item — Discovery",
    "context_unit_id": SAMPLE_CONTEXT_ID,
    "metadata": {
        "Created": "2025-01-01T00:00:00Z",
        "Updated": "2025-01-01T00:00:00Z",
        "Type": "backlog-item",
        "Version": "1.0",
        "Project": "MCU",
        "Tool": "BACKLOG",
        "Category": "governance",
        "Tags": "[\"backlog-item\", \"discovery\"]"
    },
    "summary": {
        "objective": "Example objective",
        "acceptance_criteria": ["Link to note", "Draft scope"]
    },
    "source_references": [
        {"text": "VIBE_NOTE: 2025-01-01T00-00-00Z", "href": "../../VIBE_NOTE.md#note-2025-01-01T00-00-00Z"}
    ],
    "execution_links": {"plan": "", "pop": "", "status": ""},
    "tracks": {
        "source_track": "Captured",
        "definition_track": "Triaged",
        "execution_track": "Not-Started",
        "validation_track": "Implicit-Validated",
        "docs_track": None,
        "integration_evidence": None,
        "defer_track": None,
        "defer_status": None,
        "defer_until": None
    },
    "workstreams": {}
}


class TestBlitConvert(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = Path(tempfile.mkdtemp())
        return super().setUp()

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)
        return super().tearDown()

    def test_md_json_md_semantic_equal(self):
        md_path = self.tmpdir / f"{SAMPLE_ID}.md"
        md_path.write_text(SAMPLE_MD, encoding='utf-8')

        # md -> json
        obj1 = md_to_json(md_path)

        # json -> md
        md2 = json_to_md(obj1)
        md2_path = self.tmpdir / f"J2{SAMPLE_ID}.md"
        md2_path.write_text(md2, encoding='utf-8')

        # Parse both MD to JSON and compare semantic equality
        obj_md_orig = md_to_json(md_path)
        obj_md_round = md_to_json(md2_path)

        self.assertEqual(obj_md_orig, obj_md_round)

    def test_json_md_json_semantic_equal(self):
        json_path = self.tmpdir / f"{SAMPLE_ID}.json"
        json_path.write_text(json.dumps(SAMPLE_JSON, sort_keys=True), encoding='utf-8')

        # json -> md
        md = json_to_md(SAMPLE_JSON)
        md_path = self.tmpdir / f"{SAMPLE_ID}.md"
        md_path.write_text(md, encoding='utf-8')

        # md -> json
        obj2 = md_to_json(md_path)

        # Compare semantic equality of JSON objects
        self.assertEqual(SAMPLE_JSON, obj2)


if __name__ == '__main__':
    unittest.main()


