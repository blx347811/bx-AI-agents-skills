---
name: solomon-pptx
description: |
  Creates, reads, edits, and designs PowerPoint presentations (.pptx) in Solomon Partners
  house style — premium financial-services aesthetic with navy/indigo/ice palette,
  Segoe UI typography, line-art icons, and persistent confidential footer.
  Includes visual QA workflow with slide-to-image conversion.
  Use when user asks to "create a Solomon deck", "make a Solomon-style presentation",
  "build a pitch deck in our house style", or wants a new presentation that matches
  Solomon Partners branding.
---

# Solomon PPTX Skill

Create PowerPoint presentations in Solomon Partners house style. This skill carries the same generation/edit/QA workflow as the base pptx skill, but the **Design Ideas** section encodes Solomon's specific palette, typography, motifs, and layout patterns extracted from production deliverables.

## Master Template (Default Starting Point)

This skill ships with the Solomon Partners master template:

**`template/Solomon Default Template.pptx`**

**Use this template as the starting point for every new Solomon deck unless the user explicitly asks to build from scratch or supplies their own template.** It already encodes the house masters, slide layouts, theme fonts (Segoe UI / Segoe UI Semibold), color palette, logo placement, and the persistent confidential footer described below — starting from it is faster and more consistent than rebuilding those primitives with pptxgenjs.

**Concrete first step** (do this before anything else when creating a new Solomon deck):

```bash
# 1. Copy the master template from the skill folder into the user's working directory
#    under the desired output filename. Substitute the actual skill folder path for <skill>.
cp "<skill>/template/Solomon Default Template.pptx" "./<output-name>.pptx"

# 2. Inspect available layouts in the copy
python "<skill>/scripts/thumbnail.py" "./<output-name>.pptx"
```

Then proceed with the **Editing Workflow** (`editing.md`): unpack → reuse/duplicate slides → edit content → clean → pack.

**Layout catalog:** see [`template/layouts.md`](template/layouts.md) for the master + 9 layouts inside the bundled template, with placeholder roles and the house-style use case each layout matches. Run `python "<skill>/scripts/list_layouts.py"` to print the same list at runtime (works on user-supplied templates too).

Fall back to **Creating from Scratch** (`pptxgenjs.md`) only when the user explicitly says "from scratch," "no template," or similar.

## Quick Reference

| Task | Guide |
|------|-------|
| Read/analyze content | `python -m markitdown presentation.pptx` |
| **Create a Solomon deck (default)** | **Copy `template/Solomon Default Template.pptx` to the working dir → follow `editing.md`** |
| Edit an existing user-supplied deck | Read `editing.md` |
| Create from scratch (fallback) | Read `pptxgenjs.md` |
| List layouts in a template | `python "<skill>/scripts/list_layouts.py" [path.pptx]` |

---

## Reading Content

```bash
# Text extraction
python -m markitdown presentation.pptx

# Visual overview (paths relative to skill folder — see Path Convention)
python scripts/thumbnail.py presentation.pptx

# Raw XML
python scripts/office/unpack.py presentation.pptx unpacked/
```

---

## Editing Workflow

**Read `editing.md` for full details.**

1. Copy `template/Solomon Default Template.pptx` (skill-relative — see Path Convention) into the user's working directory under the desired output filename — or use the user-supplied template if one was provided.
2. Analyze the copy with `scripts/thumbnail.py`.
3. Unpack → manipulate slides → edit content → clean → pack. All scripts live under `scripts/` (skill-relative).

---

## Creating from Scratch

**Read `pptxgenjs.md` for full details.**

Use only when no template is appropriate — e.g., the user explicitly asked for a from-scratch build, or the bundled `template/Solomon Default Template.pptx` does not match the requested format. Otherwise prefer the editing workflow against the bundled template.

---

## Design Ideas — Solomon Partners House Style

This skill produces decks in Solomon Partners house style. Apply these patterns by default unless the user explicitly asks for a different look.

### House Style Overview

- **Tone:** Premium financial-services. Clean, restrained, navy-led. Generous white space.
- **60-30-10 split:** ~60% white background + ice-blue tints, ~30% navy/indigo for type and headers, ~10% sky/teal for accents.
- **One sharp accent per slide:** Use teal sparingly — only the final step of a process, the standout chart bar, or the single number you want noticed.
- **Dark/light contrast:** Light backgrounds throughout content slides. Reserve dark navy for the title slide cover shapes and section dividers.

### Color Palette

| Role | Hex | Usage |
|------|-----|-------|
| Primary navy | `141B4D` | Slide titles, key headers (most-used dark) |
| Deep navy | `070263` | Logo wordmark, dark stat labels |
| Indigo accent | `4F4CB1` | Bold inline emphasis, section subtitles, callout fills |
| Ice blue (tint) | `E3F7FC` | Left-rail callouts, card backgrounds, icon circles |
| Lavender (tint) | `EDEAFB` | Alternate card fill (paired with ice blue in 2×2 grids) |
| Sky blue | `178AE0` | Sub-accent, vertical accent bar, chart bars |
| Light cyan | `85D6F9` | Secondary chart bar, soft accent |
| Teal accent | `2FD1B2` | Single-use sharp accent (final step, hero stat) |
| Solomon blue | `003594` | Title slide cover shape |
| Neutral | `EBEBEB` / `FFFFFF` / `000000` | Dividers, body text, backgrounds |

### Typography

| Role | Font | Sizes |
|------|------|-------|
| Major (titles, headers) | **Segoe UI Semibold** | Title slide 36pt; content slide title 32pt; section header 12-14pt |
| Minor (body, captions) | **Segoe UI** | Body 10.5-11pt; callout 12pt; footer 9pt; stat number 18pt bold |

- Titles are **left-aligned, bottom-anchored**, spanning ~91% of slide width.
- Body is left-aligned. Only quadrant-card titles may center.
- Inline emphasis: **bold + indigo** (`4F4CB1`), or **bold + underline** for category names within lists.

### Visual Motifs (use repeatedly)

1. **Vertical accent bar (left of title)** — thin sky-blue (~3-4pt) bar to the LEFT of every content slide's title block. This is the house alternative to the forbidden underline-under-title.
2. **Line-art icons in tint circles** — outlined (not filled) icons inside ice-blue circles. Use for process steps, quadrant cards, section markers.
3. **Ice-blue left rail** — narrow tinted column hosting takeaway stats or an intro paragraph; main narrative breathes on the white right side.
4. **Numbered timeline with segmented under-bar** — N circles in a row, each above a thick horizontal bar segment. Segment colors progress through the palette: light cyan → sky blue → indigo → deep indigo → teal accent.
5. **Tinted quadrant cards** — alternating ice-blue and lavender fills, icon centered above each card's top edge.
6. **Underlined bold inline emphasis** — for category names within lists (e.g., "**Valuation Benchmarking Intelligence**: …").
7. **Persistent footer** — Solomon logo bottom-left, "Private and Confidential | [page #]" bottom-right, navy slide number on every content slide.

### Layout Patterns

- **Title Slide** — Large white field; navy title in caps anchored mid-left; sky-blue subtitle below; asymmetric arc/curve shapes in the bottom-right corner; logo top-left; date bottom-left.
- **Section Divider** — Title-only on tinted or navy background; vertical accent bar optional.
- **One-Content (with rail)** — Narrow ice-blue left column for headline + supporting stats or intro; wide white right column for the main narrative.
- **Two-Content** — Two equal columns; either side may host text, chart, or visual; icons optional above each.
- **Three Column** — Three equal columns; row labels on the left optional; columns hold text, lists, charts, or visual blocks interchangeably.
- **Four-Content Grid** — 2×2 tinted cards (alternating ice-blue and lavender), icon floating above each card's top edge, header centered, body left-aligned.
- **Process / Timeline** — N numbered steps across; line-art icons in tint circles above each step; thick segmented horizontal bar below in progressing palette colors.
- **Content with Callout (Right or Left)** — Main content on one side; tinted callout block(s) on the other for quotes, examples, or supporting detail.
- **Chart + Commentary** — Numbered list or bullets on one side; single chart or visual on the other; optional footnote bar at bottom.

### Charts

- Bar fill colors progress through the palette: light cyan → sky blue → indigo → deep navy. Reserve teal (`2FD1B2`) for the standout bar only.
- Pie wedges follow the same progression; keep wedge order consistent across paired pies.
- Data labels above bars in matching dark color, bold.
- Light gridlines (`EBEBEB`), no chart border, no shadow on chart titles.
- Axis text and labels: Segoe UI 9pt, dark navy.

### Spacing

- 0.5" minimum slide margins
- 0.3-0.5" between content blocks
- Title block sits ~0.55" from top, bottom-anchored on a ~0.46" tall placeholder
- Generous white space — premium feel comes from restraint, not density

### Avoid (Common Mistakes)

- **NEVER use accent lines under titles** — use the vertical accent bar to the LEFT instead. Underlines beneath titles are a hallmark of AI-generated slides.
- **Don't use filled-shape icons** — house style is outlined line-art only.
- **Don't oversaturate fills** — backgrounds stay in the ice-blue / lavender / cream tint range, never bold full-strength color.
- **Don't overuse the teal accent** — one element per slide maximum. If everything's accented, nothing is.
- **Don't center body text** — left-align paragraphs and lists; only quadrant-card titles center.
- **Don't skip the footer** — every content slide needs logo + confidential mark + page number.
- **Don't mix font families** — Segoe UI Semibold + Segoe UI is the only pairing.
- **Don't create text-only slides** — every slide needs an icon, chart, callout, or shape.
- **Don't forget text box padding** — when aligning lines or shapes with text edges, set `margin: 0` on the text box or offset the shape to account for padding.
- **Don't use low-contrast elements** — navy on ice-blue is fine; never light gray on white or dark on dark.
- **Don't repeat the same layout** — vary across the deck; the layout list above gives nine options.

---

## QA (Required)

**Assume there are problems. Your job is to find them.**

Your first render is almost never correct. Approach QA as a bug hunt, not a confirmation step. If you found zero issues on first inspection, you weren't looking hard enough.

### Content QA

```bash
python -m markitdown output.pptx
```

Check for missing content, typos, wrong order.

**When using templates, check for leftover placeholder text:**

```bash
python -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum|this.*(page|slide).*layout"
```

If grep returns results, fix them before declaring success.

### Visual QA

**USE SUBAGENTS** — even for 2-3 slides. You've been staring at the code and will see what you expect, not what's there. Subagents have fresh eyes.

Convert slides to images (see [Converting to Images](#converting-to-images)), then use this prompt:

```
Visually inspect these slides. Assume there are issues — find them.

Look for general issues:
- Overlapping elements (text through shapes, lines through words, stacked elements)
- Text overflow or cut off at edges/box boundaries
- Decorative lines positioned for single-line text but title wrapped to two lines
- Source citations or footers colliding with content above
- Elements too close (< 0.3" gaps) or cards/sections nearly touching
- Uneven gaps (large empty area in one place, cramped in another)
- Insufficient margin from slide edges (< 0.5")
- Columns or similar elements not aligned consistently
- Low-contrast text (e.g., light gray text on cream-colored background)
- Low-contrast icons (e.g., dark icons on dark backgrounds without a contrasting circle)
- Text boxes too narrow causing excessive wrapping
- Leftover placeholder content

Look for Solomon house-style violations:
- Missing vertical sky-blue accent bar to the left of the title
- Underline beneath the title (forbidden — should be the vertical bar instead)
- Filled-shape icons (should be outlined line-art only)
- Missing footer (logo bottom-left, confidential + page number bottom-right)
- Teal accent (`2FD1B2`) used on more than one element per slide
- Centered body text (only quadrant-card titles may center)
- Font other than Segoe UI / Segoe UI Semibold
- Oversaturated fills (backgrounds should stay in ice-blue / lavender tint range)

For each slide, list issues or areas of concern, even if minor.

Read and analyze these images:
1. .qa/slide-01.jpg (Expected: [brief description])
2. .qa/slide-02.jpg (Expected: [brief description])

Report ALL issues found, including minor ones.
```

### Verification Loop

1. Generate slides → Convert to images → Inspect
2. **List issues found** (if none found, look again more critically)
3. Fix issues
4. **Re-verify affected slides** — one fix often creates another problem
5. Repeat until a full pass reveals no new issues

**Do not declare success until you've completed at least one fix-and-verify cycle.**

---

## Converting to Images

Convert presentations to individual slide images for visual inspection:

```bash
# scripts/ path is skill-relative (see Path Convention)
python scripts/office/soffice.py --headless --convert-to pdf --outdir working/ output/[filename].pptx
mkdir -p .qa
pdftoppm -jpeg -r 150 working/[filename].pdf .qa/slide
```

This creates `.qa/slide-01.jpg`, `.qa/slide-02.jpg`, etc. The `.qa/` directory keeps verification images out of the user's output. The intermediate PDF stays in `working/` so it never triggers a file-changed event.

To re-render specific slides after fixes:

```bash
pdftoppm -jpeg -r 150 -f N -l N working/[filename].pdf .qa/slide-fixed
```

After QA is complete, clean up intermediate files:

```bash
rm -rf .qa working/[filename].pdf
```

---

## Dependencies

All dependencies are pre-installed in the Docker image. No installation needed.

- `markitdown[pptx]` - text extraction (pip, pre-installed)
- `Pillow` - thumbnail grids (pip, pre-installed)
- `pptxgenjs` - creating from scratch (npm, pre-installed globally)
- `react`, `react-dom`, `react-icons` - icon generation (npm, pre-installed globally)
- `cairosvg` - SVG to PNG rasterization (pip, pre-installed)
- LibreOffice (`soffice`) - PDF conversion (auto-configured for sandboxed environments via `scripts/office/soffice.py`)
- Poppler (`pdftoppm`) - PDF to images
