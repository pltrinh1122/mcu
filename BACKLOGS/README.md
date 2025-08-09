# BACKLOGS/

This directory contains backlog index files and the collection of backlog items.

- Backlog index files: Markdown files in this directory. The default index is `BACKLOG_MAIN.md` (you may create additional indexes alongside it, e.g., `TEAM_ALPHA.md`, `ROADMAP_2025Q4.md`).
- Backlog items: Stored under `ITEMS/` as individual Markdown files.

## Conventions
- Links in backlog indexes should be relative to the index file (e.g., `ITEMS/BLIT_SYS123_2025-08-09T23-59-59Z.md`).
- Item filenames should be concise and unique: `BLIT_[systemID]_[timestamp].md` (ISO 8601 UTC with trailing Z; colon-safe in filenames: `YYYY-MM-DDTHH-MM-SSZ`).
- `[systemID]` allowed characters: strictly alphanumeric and underscore (regex: `^[A-Za-z0-9_]+$`).
- The default backlog index filename may be `BACKLOG_MAIN.md` (default). If preferred, you can rename to `BACKLOG_DEFAULT.md` and update references accordingly.

## Intake and Discovery Policy
- Intake: Always create a minimal raw item quickly (Summary, Source Reference to the note, filename per convention). Set `source_track: Captured`.
- Discovery triage: Right-size scope. If splitting/merging/bundling:
  - Create successor item(s) in `ITEMS/`, each with Derived-from link(s) to the original.
  - Update the original item with Disposition and Superseded-by link(s).
  - In the backlog index, annotate the original entry with "(superseded by: ...)" and add relative links to successor item(s).
  - Do not delete originals; they remain evidence.

## Examples
- `BACKLOG_MAIN.md` → default backlog index
- `ITEMS/BLIT_SYSABC_2025-08-09T23-59-59Z.md` → a backlog item
