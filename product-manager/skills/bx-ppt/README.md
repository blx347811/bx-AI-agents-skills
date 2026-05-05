# solomon-pptx

A Solomon Partners–branded extension of the base `pptx` skill. Same generation / edit / QA scripts; layered on top is everything needed to produce decks in Solomon house style, including a bundled master template.

## What this skill adds over the base `pptx` skill

| Area | Base `pptx` skill | `solomon-pptx` |
|------|-------------------|----------------|
| Workflow scripts | `unpack.py`, `pack.py`, `add_slide.py`, `clean.py`, `thumbnail.py`, `soffice.py`, `validate.py` | **Same** — reused unchanged |
| Master template | None — every deck starts from scratch | **Bundled** at `template/Solomon Default Template.pptx` (1 master, 9 layouts, `Solomon Widescreen Theme`, `2025 Solomon Partners` color scheme) |
| House style guidance | None | **`SKILL.md` "Design Ideas" section** — palette, typography, motifs, layout patterns, do/don't list |
| Layout discovery | Read XML by hand | **`template/layouts.md`** — catalog of all layouts with placeholder roles + house-style use case |
| Runtime layout listing | Not available | **`scripts/list_layouts.py`** — prints master + layouts for any `.pptx`, defaults to bundled template |
| QA prompt | Generic | Solomon-specific checks (vertical accent bar, no title underline, line-art icons, footer presence, teal-accent-once rule) |
| From-scratch fallback | Default path | Discouraged — `pptxgenjs.md` retained but reachable only when user explicitly opts out of the template |

## Files unique to `solomon-pptx`

```
solomon-pptx/
├── README.md                              ← this file
├── SKILL.md                               ← Design Ideas + workflow (Solomon-specific sections only)
├── template/
│   ├── Solomon Default Template.pptx      ← master template (bundled)
│   └── layouts.md                         ← layout catalog
└── scripts/
    └── list_layouts.py                    ← runtime layout introspection
```

Everything else under `scripts/` (including `scripts/office/`) is inherited from the base `pptx` skill, untouched.

## Recent changes

- Added `template/layouts.md` cataloging the 1 master + 9 layouts, each cross-referenced to a SKILL.md "Layout Pattern".
- Added `scripts/list_layouts.py` (stdlib only — no `python-pptx` dependency) for runtime introspection of any `.pptx` template.
- Updated `SKILL.md` with a pointer to the catalog and a Quick Reference row for the new script.

No edits to the base `pptx` workflow scripts (`unpack.py`, `pack.py`, `add_slide.py`, `clean.py`, `thumbnail.py`, `soffice.py`, `validate.py`).
