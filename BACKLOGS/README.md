# BACKLOGS/

This directory contains backlog index files and the collection of backlog items.

- Backlog index files: Markdown files in this directory. The default index is `BACKLOG_MAIN.md` (you may create additional indexes alongside it, e.g., `TEAM_ALPHA.md`, `ROADMAP_2025Q4.md`).
- Backlog items: Stored under `ITEMS/` as individual Markdown files.

## Conventions
- Links in backlog indexes should be relative to the index file (e.g., `ITEMS/BLIT_SYS123_2025-08-09T23-59-59Z.md`).
- Item filenames should be concise and unique: `BLIT_[systemID]_[timestamp].md` (ISO 8601 UTC with trailing Z; colon-safe in filenames: `YYYY-MM-DDTHH-MM-SSZ`).
- `[systemID]` allowed characters: strictly alphanumeric and underscore (regex: `^[A-Za-z0-9_]+$`).
- The default backlog index filename may be `BACKLOG_MAIN.md` (default). If preferred, you can rename to `BACKLOG_DEFAULT.md` and update references accordingly.

## Examples
- `BACKLOG_MAIN.md` → default backlog index
- `ITEMS/BLIT_SYSABC_2025-08-09T23-59-59Z.md` → a backlog item
