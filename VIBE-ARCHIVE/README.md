# VIBE-ARCHIVE

This directory retains archived `__vibec-*` workflow artifacts (PLAN, STATUS, ANALYSIS, etc.) for auditability. Deletion is deferred to the Operator, since Git history preserves prior content even after deletion.

## Archive Policy (Summary)
- Mark the artifact as archived in-place first:
  - Set `Status: ARCHIVE`
  - Update any POP/PLAN dashboards to `[ARCHIVE]`
  - Prepend a line: `> Archived on [ISO_UTC] – reason: <short reason>`
- Move the file into `VIBE-ARCHIVE/` using `git mv`.
- Update cross-links (e.g., POP dashboards) to point to the new location.
- Commit with a descriptive message, e.g., `chore(archive): move <file> to VIBE-ARCHIVE (reason)`

## Example Commands
```bash
mkdir -p VIBE-ARCHIVE
FILE="__vibec-PLAN__example.md"
UTC_NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)
sed -i "1s;^;> Archived on ${UTC_NOW} – reason: [ENTER_REASON]\\n\\n;" "$FILE"
git mv "$FILE" "VIBE-ARCHIVE/$(basename "$FILE")"
```

## Notes
- Prefer archive over delete to preserve local discoverability.
- Operator may later remove files from `VIBE-ARCHIVE/`; history remains in Git.


