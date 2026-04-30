---
name: pm-exec-narrative
description: >
  Produces an executive-facing strategy narrative from stage-3 PRD decisions and stage-4 work items. Use whenever the user says "exec brief", "strategy narrative", "prioritization doc", "make this executive", "one-pager for leadership", "what do I tell the partners", "what's the strategy", or needs a one-page summary to share with leadership or stakeholders. Can render in Working, Team, or Executive register. Optionally produces a PowerPoint deck. Writes to the 5_Prioritization_Strategy/ folder.
---

# pm-exec-narrative

Produces an exec-facing one-pager that traces from decisions to sequenced delivery. Decision-first. Source-anchored.

## Workflow

### Step 1 — Confirm upstream artifacts

Read:
- Most recent file in `3_PRD_Decisions/` → decisions, constraints, success signals
- `4_Delivery_WorkItems/_index.md` → work item scope and phasing

If either is missing, flag the gap and ask whether to proceed with available material or pause.

### Step 2 — Identify the register

Ask the user which register if not explicitly stated:
- **Working:** full structure, all evidence links, open questions visible
- **Team:** scoped to what the direct team owns; one delivery step per dependency owner
- **Executive:** one page, decision-first, no internal jargon, no `[TBD]` items visible (replace with "[under investigation]")

Default to Working if not specified.

### Step 3 — Draft the narrative

For Working register — write all sections:
- **Situation:** What is the problem and why does it matter now? (2–3 sentences)
- **Decision needed:** What does the reader need to decide or approve? (one sentence)
- **Options considered:** 2–3 options with tradeoffs (bullet format)
- **Recommendation:** One sentence recommendation, then 2–3 sentences of rationale citing PRD decisions
- **Sequencing:** Ordered phases or milestones. In Working register, link to work item IDs for traceability.
- **Open questions:** Unresolved items that affect the recommendation

For Executive register — strip to the essential:
- Remove work item ID references
- Remove all `[TBD]`/open-question sections
- Replace technical terms with plain language
- Target: one page readable in under 60 seconds

### Step 4 — Review with user

Show the draft. Ask whether tone, scope, and detail level match the intended audience. Adjust the register or content on feedback.

### Step 5 — Write the file

Write to `5_Prioritization_Strategy/`. Filename: `{Product} - Strategy Brief - {YYYY-MM-DD}.md`.

For Executive register: offer to produce a `pptx` deck via the `pptx` skill. Ask before invoking — this is the user's call.

---

## Output format

### Working register

```markdown
# Strategy Brief — {Product} — {YYYY-MM-DD}

_Sources: [`3_PRD_Decisions/{prd-filename}`]({path}), [`4_Delivery_WorkItems/_index.md`]({path})_

---

## Situation

{What is the problem and why does it matter now? 2–3 sentences.}

## Decision needed

{What the reader needs to decide or approve. One clear sentence.}

## Options considered

1. **{Option A}** — {1-sentence tradeoff summary}
2. **{Option B}** — {1-sentence tradeoff summary}
3. **{Option C / Status quo}** — {1-sentence tradeoff summary}

## Recommendation

**{Recommended option}.** {2–3 sentence rationale citing the PRD decisions that support it.}

## Sequencing

- **Phase 1 — {Name}:** {What gets built and why first. Work items: TBD-Epic-1}
- **Phase 2 — {Name}:** {What gets built next. Work items: TBD-Epic-2}

## Open questions

- [TBD] {Question that must be resolved before this can proceed}
```

### Executive register

```markdown
# {Product} — Strategy Brief

## Situation
{2 sentences. No internal jargon. No work item IDs. Decision-first framing.}

## What we need
{One clear ask — a decision, approval, or resource commitment.}

## Options
1. **{Option A}** — {tradeoff, one line}
2. **{Option B}** — {tradeoff, one line}

## Recommendation
{Option name} — {1–2 sentence rationale. No jargon.}

## Delivery plan
- **{Phase 1}:** {Plain-English milestone. When.}
- **{Phase 2}:** {Plain-English milestone. When.}
```
