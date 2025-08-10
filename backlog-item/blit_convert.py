#!/usr/bin/env python3
"""
BLIT converter: Markdown <-> JSON for backlog items

Usage examples:
  # Convert all BLIT_*.md in BACKLOGS/ITEMS/ to JSON (same dir)
  python3 backlog-item/blit_convert.py md-to-json --path BACKLOGS/ITEMS

  # Convert one file
  python3 backlog-item/blit_convert.py md-to-json --path BACKLOGS/ITEMS/BLIT_XXXX.md

  # Convert JSON back to Markdown
  python3 backlog-item/blit_convert.py json-to-md --path BACKLOGS/ITEMS/BLIT_XXXX.json
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def write_text(p: Path, s: str) -> None:
    p.write_text(s, encoding="utf-8")


def parse_metadata_block(lines: List[str], start_idx: int) -> Dict[str, str]:
    meta: Dict[str, str] = {}
    idx = start_idx
    while idx < len(lines):
        line = lines[idx]
        if not line.startswith('- **'):
            break
        m = re.match(r"^- \*\*(.+?)\*\*:\s*(.*)$", line)
        if m:
            meta[m.group(1)] = m.group(2)
        idx += 1
    return meta


def parse_list_items(lines: List[str], start_idx: int) -> Tuple[List[str], int]:
    items: List[str] = []
    idx = start_idx
    while idx < len(lines):
        line = lines[idx].rstrip()
        if line.startswith('- '):
            items.append(line[2:].strip())
            idx += 1
        else:
            break
    return items, idx


def parse_source_refs(lines: List[str], start_idx: int) -> Tuple[List[Dict[str, str]], int]:
    refs: List[Dict[str, str]] = []
    idx = start_idx
    link_re = re.compile(r"^- \[([^\]]+)\]\(([^\)]+)\)")
    while idx < len(lines):
        line = lines[idx].rstrip()
        m = link_re.match(line)
        if not m:
            break
        refs.append({"text": m.group(1), "href": m.group(2)})
        idx += 1
    return refs, idx


def parse_tracks(lines: List[str], start_idx: int) -> Dict[str, str]:
    tracks: Dict[str, str] = {}
    idx = start_idx
    while idx < len(lines):
        line = lines[idx].strip()
        if not line.startswith('- '):
            break
        m = re.match(r"^-\s*([a-z_]+):\s*(.*)$", line)
        if m:
            tracks[m.group(1)] = m.group(2)
        idx += 1
    return tracks


def md_to_json(md_path: Path) -> Dict:
    text = read_text(md_path)
    lines = text.splitlines()
    data: Dict = {
        "id": md_path.stem,
        "title": "",
        "context_unit_id": "",
        "metadata": {},
        "summary": {"objective": "", "acceptance_criteria": []},
        "source_references": [],
        "execution_links": {"plan": "", "pop": "", "status": ""},
        "tracks": {},
        "workstreams": {},
    }

    # Title: first H1
    for line in lines:
        if line.startswith('# '):
            data["title"] = line[2:].strip()
            break

    # Context Memory Unit
    cmu = re.search(r"^## Context Memory Unit:\s*(.+)$", text, re.MULTILINE)
    if cmu:
        data["context_unit_id"] = cmu.group(1).strip()

    # Metadata block (lines starting with - **Key**: Value)
    for i, line in enumerate(lines):
        if line.startswith('- **Created**:'):
            meta = parse_metadata_block(lines, i)
            data["metadata"] = meta
            break

    # Summary
    sum_idx = text.find('\n## Summary')
    if sum_idx != -1:
        # Objective line
        m = re.search(r"## Summary\n-\s*Objective:\s*(.*)", text)
        if m:
            data["summary"]["objective"] = m.group(1).strip()
        # Acceptance Criteria bullets until next H2
        ac = re.search(r"-\s*Acceptance Criteria:\n([\s\S]*?)\n## ", text)
        if not ac:
            ac = re.search(r"-\s*Acceptance Criteria:\n([\s\S]*)$", text)
        if ac:
            ac_block = ac.group(1).splitlines()
            data["summary"]["acceptance_criteria"] = [l[2:].strip() for l in ac_block if l.strip().startswith('- ')]

    # Source References section
    refs_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith('## Source References'):
            refs_idx = i + 1
            break
    if refs_idx is not None:
        refs, _ = parse_source_refs(lines, refs_idx)
        data["source_references"] = refs

    # Execution Links
    el_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith('## Execution Links'):
            el_idx = i + 1
            break
    if el_idx is not None:
        # Expect three lines: PLAN, POP, STATUS
        for j in range(el_idx, min(el_idx + 6, len(lines))):
            l = lines[j].strip()
            if l.startswith('- PLAN:'):
                data["execution_links"]["plan"] = l.split(':', 1)[1].strip()
            elif l.startswith('- POP:'):
                data["execution_links"]["pop"] = l.split(':', 1)[1].strip()
            elif l.startswith('- STATUS:'):
                data["execution_links"]["status"] = l.split(':', 1)[1].strip()

    # Tracks
    tr_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith('## Tracks'):
            tr_idx = i + 1
            break
    if tr_idx is not None:
        data["tracks"] = parse_tracks(lines, tr_idx)

    # Workstreams (optional)
    ws_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith('## Workstreams'):
            ws_idx = i + 1
            break
    if ws_idx is not None:
        ws: Dict[str, str] = {}
        idx = ws_idx
        while idx < len(lines):
            l = lines[idx].strip()
            if not l.startswith('- '):
                break
            m = re.match(r"^-\s*([a-z_]+):\s*(.*)$", l)
            if m:
                ws[m.group(1)] = m.group(2)
            idx += 1
        data["workstreams"] = ws

    return data


def json_to_md(j: Dict) -> str:
    meta = j.get("metadata", {})
    title = j.get("title", j.get("id", ""))
    lines: List[str] = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"## Context Memory Unit: {j.get('context_unit_id','')}")
    for key in ["Created", "Updated", "Type", "Version", "Project", "Tool", "Category", "Tags"]:
        if key in meta:
            lines.append(f"- **{key}**: {meta[key]}")
    lines.append("")
    lines.append("---")
    lines.append("")
    # Summary
    summary = j.get("summary", {})
    lines.append("## Summary")
    lines.append(f"- Objective: {summary.get('objective','')}")
    lines.append("- Acceptance Criteria:")
    for ac in summary.get("acceptance_criteria", []):
        lines.append(f"  - {ac}")
    lines.append("")
    # Source refs
    lines.append("## Source References (≥1)")
    for ref in j.get("source_references", []):
        txt = ref.get("text", "ref")
        href = ref.get("href", "")
        lines.append(f"- [{txt}]({href})")
    lines.append("")
    # Execution links
    el = j.get("execution_links", {})
    lines.append("## Execution Links (optional)")
    lines.append(f"- PLAN: {el.get('plan','')}")
    lines.append(f"- POP: {el.get('pop','')}")
    lines.append(f"- STATUS: {el.get('status','')}")
    lines.append("")
    # Tracks
    lines.append("## Tracks (authoritative on item)")
    for k, v in j.get("tracks", {}).items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    # Workstreams
    if j.get("workstreams"):
        lines.append("## Workstreams (read-only, derived from backlog)")
        for k, v in j.get("workstreams", {}).items():
            lines.append(f"- {k}: {v}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description='Convert BLIT Markdown <-> JSON')
    ap.add_argument('mode', choices=['md-to-json', 'json-to-md'])
    ap.add_argument('--path', required=True, help='File or directory path')
    args = ap.parse_args()

    path = Path(args.path)
    files: List[Path] = []
    if path.is_dir():
        if args.mode == 'md-to-json':
            files = sorted([p for p in path.glob('BLIT_*.md')])
        else:
            files = sorted([p for p in path.glob('BLIT_*.json')])
    else:
        files = [path]

    count = 0
    for fp in files:
        if args.mode == 'md-to-json':
            data = md_to_json(fp)
            out = fp.with_suffix('.json')
            out.write_text(json.dumps(data, indent=2), encoding='utf-8')
        else:
            data = json.loads(read_text(fp))
            out = fp.with_suffix('.md')
            write_text(out, json_to_md(data))
        count += 1
    print(f"Converted {count} file(s)")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())


