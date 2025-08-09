# Component-Specific Vibe-Coding: docs

## Additional Validation

- Markdown syntax: `markdownlint docs/**/*.md --disable MD013`
- Optional link validation: `python scripts/check_links.py` (on Operator request)
- YAML blocks embedded in docs: if extracted, validate with `yamllint` (as needed)

## Component-Specific Tests

- Treat validation as tests for documentation changes.
- Broken links or references do not block by default; escalate to Operator during incidents.

## Component Conventions

- Clear structure, progressive disclosure, professional tone, no emojis.
- Keep `[LINK]` placeholders until explicitly asked to update.
- Follow Conventional Commits for documentation changes.

## Notes

- Auto-install missing markdown tooling when needed; if installation is blocked/unavailable, pause and request Operator approval before proceeding.
- Do not modify or migrate `__vibew-*` files.


