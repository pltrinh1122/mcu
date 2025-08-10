#!/usr/bin/env python3
"""
Backlog Item Kanban Renderer

Given a backlog item Markdown file (BACKLOGS/ITEMS/*.md), render kanban-style
boards for each workstream, where columns are the states of the relevant tracks
and the item's current state is highlighted.

Usage:
  python3 base/scripts/backlog_kanban.py BACKLOGS/ITEMS/BLIT_<SYSTEMID>_<TS>.md

Notes:
  - Workstreams are orchestration phases; they reference item tracks to define
    entry/exit. This renderer is a view: it does not change item state.
  - Defer is modeled as an overlay workstream with `defer_track`, `defer_status`,
    and optional `defer_until`.
"""

from __future__ import annotations

from pathlib import Path
import re
import sys
from typing import Dict, List, Tuple


def read_item_text(item_path: Path) -> str:
    return item_path.read_text(encoding="utf-8")


def read_tracks(markdown_text: str) -> Dict[str, str]:
    tracks: Dict[str, str] = {}
    in_tracks_section = False
    for line in markdown_text.splitlines():
        if line.strip().startswith("## Tracks"):
            in_tracks_section = True
            continue
        if in_tracks_section:
            if line.strip().startswith("## "):
                break
            match = re.match(r"^-\s*([a-z_]+):\s*(.*)$", line.strip())
            if match:
                track_name = match.group(1)
                track_value = match.group(2)
                tracks[track_name] = track_value
    return tracks


def read_title(markdown_text: str) -> str:
    for line in markdown_text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def render_lane(title: str, columns: List[str], current: str, extra_note: str = "") -> str:
    """Render a single workstream lane as a kanban row.

    - Columns are states. The current state is highlighted with [*state*].
    - extra_note is appended in parentheses at the end of the lane.
    """
    def highlight(state: str) -> str:
        return f"[*{state}*]" if state == current else state

    rendered_columns = " | ".join(highlight(s) for s in columns)
    suffix = f"  ({extra_note})" if extra_note else ""
    return f"{title}:  {rendered_columns}{suffix}"


def main(argv: List[str]) -> int:
    if len(argv) != 2:
        print("Usage: python3 base/scripts/backlog_kanban.py BACKLOGS/ITEMS/<file>.md")
        return 1

    item_path = Path(argv[1]).resolve()
    if not item_path.exists():
        print(f"Item not found: {item_path}")
        return 1

    markdown_text = read_item_text(item_path)
    title = read_title(markdown_text) or item_path.name
    tracks = read_tracks(markdown_text)

    source_track = tracks.get("source_track", "")
    definition_track = tracks.get("definition_track", "")
    execution_track = tracks.get("execution_track", "")
    validation_track = tracks.get("validation_track", "")
    docs_track = tracks.get("docs_track", "")
    defer_track = tracks.get("defer_track", "")
    defer_status = tracks.get("defer_status", "")
    defer_until = tracks.get("defer_until", "")

    header = f"Item: {title}\nPath: {item_path.relative_to(Path(__file__).resolve().parents[2])}"
    print(header)

    # Discovery lane
    print(render_lane(
        title="Discovery",
        columns=["Captured", "Curated"],
        current=source_track,
    ))

    # Definition lane
    print(render_lane(
        title="Definition",
        columns=["Triaged", "Clarified", "Sized", "AC-Ready"],
        current=definition_track,
    ))

    # Planning lane (simple two-state view)
    # This workstream is gated by AC-Ready and plan acceptance (not an item track),
    # so we expose a minimal Waiting → Plan-Accepted view. We infer current as Waiting
    # unless execution is already started and plan was presumably accepted.
    planning_current = "Waiting"
    if definition_track == "AC-Ready" and execution_track in ("", "Not-Started"):
        planning_current = "Waiting"
    elif execution_track in ("In-Progress", "Blocked", "Completed"):
        planning_current = "Plan-Accepted"

    print(render_lane(
        title="Planning",
        columns=["Waiting", "Plan-Accepted"],
        current=planning_current,
    ))

    # Delivery (Execution) lane
    print(render_lane(
        title="Delivery (Execution)",
        columns=["Not-Started", "In-Progress", "Blocked", "Completed"],
        current=execution_track,
    ))

    # Validation lane
    print(render_lane(
        title="Validation",
        columns=["Implicit-Validated", "Explicit-Accepted"],
        current=validation_track,
    ))

    # Release lane (simple two-state view)
    release_current = "Released" if validation_track == "Explicit-Accepted" else "Waiting"
    print(render_lane(
        title="Release",
        columns=["Waiting", "Released"],
        current=release_current,
    ))

    # Defer lane (overlay)
    defer_columns = ["Deferred", "Permanently-Deferred"]
    defer_note_parts = []
    if defer_status:
        defer_note_parts.append(f"status={defer_status}")
    if defer_until:
        defer_note_parts.append(f"until={defer_until}")
    defer_note = ", ".join(defer_note_parts)
    print(render_lane(
        title="Defer (overlay)",
        columns=defer_columns,
        current=defer_track,
        extra_note=defer_note,
    ))

    # Optional: Docs lane if teams want a quick view of documentation status
    if docs_track:
        print(render_lane(
            title="Docs",
            columns=["Docs-Added", "Examples-Linked"],
            current=docs_track,
        ))

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))


