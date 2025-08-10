#!/usr/bin/env python3
"""
Backlog CSV Reports

Reads BACKLOGS/ITEMS/*.md and emits two CSV reports to stdout:
1) Grouped by Workstream (one row per item, with all track states)
2) Grouped by Tracks (one row per item per track state)

Inference rules for workstream (best-effort):
- Discovery: source_track == Captured
- Definition: source_track == Curated and definition_track != AC-Ready
- Planning: definition_track == AC-Ready and execution_track in {Not-Started, ''}
- Delivery (Execution): execution_track in {In-Progress, Blocked}
- Validation: execution_track == Completed and validation_track != Explicit-Accepted
- Release: validation_track == Explicit-Accepted

If tracks are missing or ambiguous, items are placed under "Unassigned".
"""

from pathlib import Path
import re
import sys
from typing import Dict, List, Tuple
import csv
import json
import argparse


def read_tracks(md_text: str) -> Dict[str, str]:
    tracks: Dict[str, str] = {}
    in_tracks = False
    for line in md_text.splitlines():
        if line.strip().startswith('## Tracks'):
            in_tracks = True
            continue
        if in_tracks:
            if line.strip().startswith('## '):
                break
            m = re.match(r'^-\s*([a-z_]+):\s*(.*)$', line.strip())
            if m:
                tracks[m.group(1)] = m.group(2)
    return tracks


def read_title(md_text: str) -> str:
    for line in md_text.splitlines():
        if line.startswith('# '):
            return line[2:].strip()
    return ''


def infer_workstream(tracks: Dict[str, str]) -> str:
    source = tracks.get('source_track', '')
    definition = tracks.get('definition_track', '')
    execution = tracks.get('execution_track', '')
    validation = tracks.get('validation_track', '')

    if source == 'Captured':
        return 'Discovery'
    if source == 'Curated' and definition != 'AC-Ready':
        return 'Definition'
    if definition == 'AC-Ready' and execution in ('', 'Not-Started'):
        return 'Planning'
    if execution in ('In-Progress', 'Blocked'):
        return 'Delivery (Execution)'
    if execution == 'Completed' and validation != 'Explicit-Accepted':
        return 'Validation'
    if validation == 'Explicit-Accepted':
        return 'Release'
    return 'Unassigned'


def _collect_rows(items_dir: Path, repo_root: Path) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    rows_ws: List[Dict[str, str]] = []
    rows_tracks: List[Dict[str, str]] = []
    for md_file in sorted(items_dir.glob('*.md')):
        text = md_file.read_text(encoding='utf-8')
        tracks = read_tracks(text)
        ws = infer_workstream(tracks)
        title = read_title(text) or md_file.name
        rel = md_file.relative_to(repo_root).as_posix()

        # Workstream CSV row (one row per item)
        rows_ws.append({
            'workstream': ws,
            'title': title,
            'path': rel,
            'source_track': tracks.get('source_track', ''),
            'definition_track': tracks.get('definition_track', ''),
            'execution_track': tracks.get('execution_track', ''),
            'validation_track': tracks.get('validation_track', ''),
            'docs_track': tracks.get('docs_track', ''),
            'defer_track': tracks.get('defer_track', ''),
            'defer_status': tracks.get('defer_status', ''),
            'defer_until': tracks.get('defer_until', ''),
        })

        # Tracks CSV rows (one row per item per track with a value)
        for track_name in ['source_track', 'definition_track', 'execution_track', 'validation_track', 'docs_track', 'defer_track']:
            value = tracks.get(track_name, '')
            if value:
                row = {
                    'track': track_name,
                    'state': value,
                    'title': title,
                    'path': rel,
                    'workstream': ws,
                }
                if track_name == 'defer_track':
                    row['defer_status'] = tracks.get('defer_status', '')
                    row['defer_until'] = tracks.get('defer_until', '')
                rows_tracks.append(row)

    # Sort rows for stable grouping
    ws_order = ['Discovery', 'Definition', 'Planning', 'Delivery (Execution)', 'Validation', 'Release', 'Unassigned']
    rows_ws.sort(key=lambda r: (ws_order.index(r['workstream']) if r['workstream'] in ws_order else len(ws_order), r['title']))
    rows_tracks.sort(key=lambda r: (r['track'], r.get('state', ''), r['title']))

    return rows_ws, rows_tracks


def _emit_csv(rows: List[Dict[str, str]], fieldnames: List[str], out_path: Path | None):
    out_file = sys.stdout if out_path is None else open(out_path, 'w', encoding='utf-8', newline='')
    try:
        writer = csv.DictWriter(out_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({fn: row.get(fn, '') for fn in fieldnames})
    finally:
        if out_file is not sys.stdout:
            out_file.close()


def _emit_json(rows: List[Dict[str, str]], out_path: Path | None):
    out_file = sys.stdout if out_path is None else open(out_path, 'w', encoding='utf-8')
    try:
        json.dump(rows, out_file, indent=2)
        if out_file is sys.stdout:
            print()
    finally:
        if out_file is not sys.stdout:
            out_file.close()


def _emit_md(rows: List[Dict[str, str]], fieldnames: List[str], out_path: Path | None, title: str):
    out_file = sys.stdout if out_path is None else open(out_path, 'w', encoding='utf-8')
    try:
        print(f"# {title}", file=out_file)
        # Header
        print("| " + " | ".join(fieldnames) + " |", file=out_file)
        print("| " + " | ".join(['---'] * len(fieldnames)) + " |", file=out_file)
        for row in rows:
            print("| " + " | ".join((str(row.get(fn, '')) for fn in fieldnames)) + " |", file=out_file)
    finally:
        if out_file is not sys.stdout:
            out_file.close()


def main() -> int:
    parser = argparse.ArgumentParser(description='Generate backlog reports (workstream and tracks).')
    parser.add_argument('--items-dir', default=None, help='Path to BACKLOGS/ITEMS directory (default: repo BACKLOGS/ITEMS)')
    parser.add_argument('--ws-out', default=None, help='Output file for Workstream report')
    # New preferred flags for tracks: --tr-*
    parser.add_argument('--tr-out', default=None, help='Output file for Tracks (TR) report')
    parser.add_argument('--ws-format', default='csv', choices=['csv', 'json', 'md'], help='Format for Workstream report (default: csv)')
    parser.add_argument('--tr-format', default=None, choices=['csv', 'json', 'md'], help='Format for Tracks (TR) report (default: csv)')
    # Back-compat aliases (deprecated): --tracks-*
    parser.add_argument('--tracks-out', default=None, help=argparse.SUPPRESS)
    parser.add_argument('--tracks-format', default=None, choices=['csv', 'json', 'md'], help=argparse.SUPPRESS)
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    items_dir = Path(args.items_dir) if args.items_dir else (repo_root / 'BACKLOGS' / 'ITEMS')
    if not items_dir.exists():
        print(f"Items directory not found: {items_dir}")
        return 1

    rows_ws, rows_tracks = _collect_rows(items_dir, repo_root)

    ws_fields = ['workstream', 'title', 'path', 'source_track', 'definition_track', 'execution_track', 'validation_track', 'docs_track', 'defer_track', 'defer_status', 'defer_until']
    tracks_fields = ['track', 'state', 'title', 'path', 'workstream', 'defer_status', 'defer_until']

    ws_out = Path(args.ws_out) if args.ws_out else None
    # Resolve TR output and format with back-compat flags
    tr_out_arg = args.tr_out if args.tr_out is not None else args.tracks_out
    tr_fmt_arg = args.tr_format if args.tr_format is not None else args.tracks_format
    tr_out = Path(tr_out_arg) if tr_out_arg else None

    # Emit Workstream report
    if args.ws_format == 'csv':
        _emit_csv(rows_ws, ws_fields, ws_out)
    elif args.ws_format == 'json':
        _emit_json(rows_ws, ws_out)
    else:
        _emit_md(rows_ws, ws_fields, ws_out, title='Report: Grouped by Workstream')

    # Spacer for stdout when both go to stdout and formats are CSV
    if ws_out is None and tr_out is None:
        print()

    # Emit Tracks report
    tr_format = (tr_fmt_arg or 'csv')
    if tr_format == 'csv':
        _emit_csv(rows_tracks, tracks_fields, tr_out)
    elif tr_format == 'json':
        _emit_json(rows_tracks, tr_out)
    else:
        _emit_md(rows_tracks, tracks_fields, tr_out, title='Report: Grouped by Tracks')

    return 0


if __name__ == '__main__':
    sys.exit(main())


