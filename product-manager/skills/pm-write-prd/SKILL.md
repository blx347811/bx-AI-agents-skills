---
name: pm-write-prd
description: >
  Turns stage-2 themes and user-supplied technical constraints into a combined Product Requirements Document (PRD) that includes the technical design spec. Use whenever the user says "write a PRD", "document the decisions", "write up the requirements", "create the product spec", "formalize this into a PRD", or is ready to move from themes to formal requirements. The PRD includes both product requirements (problem statement, decisions with alternatives rejected, constraints, success signals) and the technical design spec (architecture, components, data flow, integration points, dependencies) in one document. Writes to the 3_PRD_Decisions/ folder.
---

# pm-write-prd

Produces the stage-3 combined PRD + technical design spec. Every decision traces to a theme; every theme is cited by name. The product reasoning and technical design live in a single document.

## Workflow

### Step 1 — Confirm upstream exists

Check for a `2_Themes_Evidence/` document for this product. If none exists, stop and route the user to `/pm-surface-themes` first. If a themes doc exists but is sparse, proceed with `[TBD]` placeholders and flag the gaps clearly.

### Step 2 — Gather technical constraints

Ask the user for:
- Target system or platform (if known)
- Known technical constraints (security model, performance requirements, existing integrations, data sources)
- Stakeholders who will review the PRD

Document all responses. Anything unknown becomes `[TBD]` in the technical design spec.

### Step 3 — Draft the product requirements section

Write the following. Cite themes by name throughout.

- **Problem statement:** What user need or business gap does this address? Cite the driving themes.
- **Audience:** Who uses this? Distinguish primary (direct users) from secondary (beneficiaries or affected parties).
- **Decisions:** Each major product decision, with: the decision taken, alternatives explicitly rejected, and the rationale. One subsection per decision. Tag each decision with the theme it resolves. Decisions with alternatives rejected are the highest-value content — take time to get them right.
- **Constraints:** Known limits (business, regulatory, operational). Mark unknown constraints `[TBD]`.
- **Success signals:** Observable outcomes that indicate this worked. Behavioral, not just metrics.

### Step 4 — Draft the technical design spec

Write the following, or `[TBD]` for anything not yet known:

- **System architecture:** Text-based description or block diagram of the system. Name the major components and show how they connect.
- **Components:** A table listing each component/service with a one-line purpose.
- **Data flow:** How data moves through the system, step by step. Name which component handles each step.
- **Integration points:** External systems, APIs, and data sources the system touches. For each: name, interaction direction (in/out/both), and a one-sentence description.
- **Dependencies:** What this system relies on (upstream), and what relies on this system (downstream).
- **Open technical questions:** Questions that must be answered before implementation can begin.

### Step 5 — Review with user

Present the full draft. Ask the user to:
- Confirm or revise decisions — especially the "alternatives rejected" entries
- Fill in any `[TBD]` items they already know
- Add missing technical constraints or integration points

### Step 6 — Write the file

Write to `3_PRD_Decisions/`. Filename: `{Product} - PRD - {YYYY-MM-DD}.md`. Report the full path on completion.

---

## Output format

````markdown
# PRD — {Product} — {YYYY-MM-DD}

_Themes sourced from: [`2_Themes_Evidence/{themes-filename}`]({relative path})_

---

## Problem statement

{What user need or business gap this addresses. Cite the themes driving it by name.}

## Audience

**Primary:** {Who directly uses this}
**Secondary:** {Who benefits or is affected}

---

## Decisions

### Decision 1: {Short title}

| | |
|---|---|
| **Decision** | {What was decided} |
| **Alternatives rejected** | {What else was considered and why it was ruled out} |
| **Rationale** | {Why this decision was made — cite the theme} |
| **Theme** | {Theme name from stage-2} |

### Decision 2: {Short title}

...

---

## Constraints

- {Constraint}
- [TBD] {Constraint requiring investigation}

## Success signals

- {Observable outcome that indicates success}
- {Another observable outcome}

---

## Technical design spec

### System architecture

{Describe the high-level system structure. Use a text block diagram or prose. Name every major component.}

```
[Component A] → [Component B] → [Component C]
                      ↑
               [External System]
```

### Components

| Component | Purpose |
|---|---|
| {Name} | {One-line description} |
| {Name} | {One-line description} |

### Data flow

1. {Step — which component, what happens, what data moves}
2. {Step}
3. {Step}

### Integration points

| System / API | Direction | Description |
|---|---|---|
| {Name} | In / Out / Both | {One sentence} |

### Dependencies

**Upstream (this system relies on):** {list}
**Downstream (relies on this system):** {list}

### Open technical questions

- [TBD] {Question that must be answered before implementation}

---

## Open questions

- [TBD] {Unresolved product-level question}
````
