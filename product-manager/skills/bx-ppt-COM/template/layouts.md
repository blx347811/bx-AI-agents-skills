# Solomon Default Template — Layout Catalog

Generated from `template/Solomon Default Template.pptx`. Use this catalog when picking a layout in the editing workflow (see `editing.md` and `scripts/add_slide.py`). Layout names below come straight from the template's XML (`ppt/slideLayouts/*.xml`, `<p:cSld name="…">`); index 0 is the first layout the master exposes.

## Master

`slideMaster1` — Solomon house master.

- **Theme name:** `Solomon Widescreen Theme`
- **Color scheme:** `2025 Solomon Partners`
- **Major font (titles):** `Segoe UI Semibold`
- **Minor font (body):** `Segoe UI`
- **Slide size:** 13.33" × 7.50" (widescreen 16:9, EMU 12192000 × 6858000)

### Theme color slots

These are the named slots the master defines. Tints used in SKILL.md (ice blue `E3F7FC`, lavender `EDEAFB`) are not theme slots — they're applied as tint/shade modifications of these base colors at the layout/shape level.

| Slot | Hex | Role in SKILL.md palette |
|------|-----|--------------------------|
| `dk1` | `000000` | Body text fallback |
| `lt1` | `FFFFFF` | White background |
| `dk2` | `070263` | Deep navy |
| `lt2` | `4F4CB1` | Indigo accent |
| `accent1` | `178AE0` | Sky blue |
| `accent2` | `85D6F9` | Light cyan |
| `accent3` | `4F4CB1` | Indigo (duplicate of `lt2`) |
| `accent4` | `2FD1B2` | Teal accent (sharp accent — use sparingly) |
| `accent5` | `2B0454` | Deep purple (cover/divider use only) |
| `accent6` | `141B4D` | Primary navy (slide titles) |
| `hlink` | `0E04C7` | Hyperlink |
| `folHlink` | `003594` | Solomon blue (followed link) |

## Layouts

| Index | Layout name | File | Placeholders (type@idx) | House-style use case |
|-------|-------------|------|--------------------------|----------------------|
| 0 | Title Slide | `slideLayout1.xml` | body@11, body@12, body@13 | Cover slide. Large white field, navy title in caps anchored mid-left, sky-blue subtitle below, asymmetric arc/curve shapes bottom-right, logo top-left, date bottom-left. |
| 1 | Title and Content | `slideLayout2.xml` | title, body@11, body@13, body@48, sldNum@4 | Default content slide. One title + one body region. Use for One-Content (with rail) or any single-region body slide. |
| 2 | Two Content | `slideLayout3.xml` | title, body@11, body@12, body@18, body@21, body@22, body@48, sldNum@23 | Two-Content. Two equal columns; either side can hold text, chart, or visual; icons optional above each column. |
| 3 | Three Column | `slideLayout4.xml` | title, body@11, body@18, body@19, body@20, body@21, body@22, body@23, body@48, sldNum@25 | Three Column. Three equal columns; row labels on the left optional; columns hold text, lists, charts, or visuals interchangeably. |
| 4 | Four Content - Grid | `slideLayout5.xml` | title, body@11, body@12, body@18, body@19, body@20, body@21, body@22, body@24, body@48, body@49, sldNum@23 | Four-Content Grid. 2×2 tinted cards (alternating ice-blue and lavender), icon floating above each card's top edge, header centered, body left-aligned. |
| 5 | Content with Callout (Right) | `slideLayout6.xml` | title, body@11, body@13, body@20, body@48, sldNum@42 | Content with Callout (Right). Main content on the left; tinted callout block on the right for quotes, examples, or supporting detail. |
| 6 | Content with Callout (Left) | `slideLayout7.xml` | title, body@19, body@20, body@22, body@23, body@48, sldNum@4 | Content with Callout (Left). Tinted callout block on the left; main content on the right. Use for One-Content (with ice-blue left rail) variant. |
| 7 | Table of Contents - Agenda | `slideLayout8.xml` | title, ftr@10, sldNum@4 | Agenda / table of contents. Title + structured TOC content lives in shapes on the layout (not in editable placeholders), so most editing happens in the slide itself rather than via placeholders. |
| 8 | Section Divider | `slideLayout9.xml` | body@15, body@19, body@33, sldNum@4 | Section Divider. Title-only slide on tinted or navy background; vertical accent bar optional. Use between major sections. |

## Cross-reference: SKILL.md "Layout Patterns"

| SKILL.md pattern | Layout(s) to use |
|------------------|------------------|
| Title Slide | `Title Slide` (idx 0) |
| Section Divider | `Section Divider` (idx 8) |
| One-Content (with rail) | `Title and Content` (idx 1) or `Content with Callout (Left)` (idx 6) for the ice-blue left rail |
| Two-Content | `Two Content` (idx 2) |
| Three Column | `Three Column` (idx 3) |
| Four-Content Grid | `Four Content - Grid` (idx 4) |
| Content with Callout (Right or Left) | `Content with Callout (Right)` (idx 5) or `Content with Callout (Left)` (idx 6) |
| Process / Timeline | Build on `Title and Content` (idx 1); the timeline shapes are not a separate layout — add them per the visual motifs in SKILL.md |
| Chart + Commentary | Build on `Two Content` (idx 2) — chart in one column, commentary in the other |

## How to inspect this template at runtime

```bash
# Print master + layouts to stdout (defaults to bundled template)
python "<skill>/scripts/list_layouts.py"

# Or point at a user-supplied template
python "<skill>/scripts/list_layouts.py" path/to/other-template.pptx
```
