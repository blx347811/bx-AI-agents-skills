---
name: pm-translate-to-workitems
description: >
  Decomposes a stage-3 PRD into an Epic → Feature → Story → Task hierarchy of work item drafts. Use whenever the user says "translate to work items", "break this down", "create the work items", "decompose into tasks", "what are the work items for this PRD", or is ready to turn a PRD into deliverable units. Produces local .md files with placeholder IDs — no external system calls, no ADO reads or writes. Writes to the 4_Delivery_WorkItems/ folder.
---

# pm-translate-to-workitems

Decomposes PRD decisions into a local work item hierarchy. Placeholder IDs throughout — the user assigns real IDs when posting to their delivery system.

## Workflow

### Step 1 — Read the PRD

Locate and read the most recent `.md` file in `3_PRD_Decisions/`. If none exists, stop and route the user to `/pm-write-prd` first.

### Step 2 — Detect existing format

Check `4_Delivery_WorkItems/` for existing `.md` work item files. If files are present, open one and note:
- Header table fields and their order
- ID format
- Hierarchy notation in `## Hierarchy`
- Filename convention

If the folder is empty, use the default format in `## Output format` below.

### Step 3 — Build the hierarchy

Decompose PRD decisions into a work item tree:

| Type | Scope | Typical count |
|---|---|---|
| **Epic** | Large capability area | 1–3 per PRD |
| **Feature** | Deliverable chunk within an Epic | 2–5 per Epic |
| **User Story** | User-facing behavior within a Feature | 2–4 per Feature |
| **Task** | Concrete implementation step within a Story | Optional; include when clear from PRD |

Every work item must:
- Reference its parent by ID
- Trace back to the PRD decision or section that generated it (include the reference in the Description)

User stories follow the pattern: `As a {role}, I want {action} so that {outcome}.`

### Step 4 — Assign placeholder IDs

Use the form: `TBD-Epic-1`, `TBD-Feature-1.1`, `TBD-Story-1.1.1`, `TBD-Task-1.1.1.1`.

The user replaces these with real IDs when posting to their delivery system. Do not call any external system to check for collisions.

### Step 5 — Preview the hierarchy

Before writing any files, show the user:
1. The full hierarchy tree (indented bullet list with IDs and titles)
2. The list of filenames to be created

Wait for confirmation or corrections.

### Step 6 — Write all files

Write one `.md` per work item, plus an `_index.md`. Report the filenames and count on completion.

---

## Output format

### Work item file: `{ID}_{Type}_{Slug}.md`

```markdown
# [{ID}] {Type} — {Title}

| Field | Value |
|---|---|
| **State** | Draft |
| **Assigned To** | [TBD] |
| **Iteration** | [TBD] |
| **Area** | [TBD] |
| **Created** | {YYYY-MM-DD} |
| **Last Changed** | {YYYY-MM-DD} |
| **ADO Link** | [TBD] |

## Hierarchy

**Parent:** [{Parent ID} — {Parent Title}]({parent-filename}.md)

**Children:**
- [{Child ID} — {Child Title}]({child-filename}.md)

## Description

{For Epics/Features: capability description. For User Stories: "As a {role}, I want {action} so that {outcome}." For Tasks: specific implementation step.}

**PRD reference:** {Section name or decision title from 3_PRD_Decisions/}
```

### Index file: `_index.md`

```markdown
# Work Item Index — {Product}

_Generated from [`3_PRD_Decisions/{prd-filename}`]({relative path}) on {YYYY-MM-DD}._

## Hierarchy

- {TBD-Epic-1} — {Epic title}
  - {TBD-Feature-1.1} — {Feature title}
    - {TBD-Story-1.1.1} — {Story title}

## All items

| ID | Type | Title | State | Parent |
|---|---|---|---|---|
| TBD-Epic-1 | Epic | {Title} | Draft | — |
| TBD-Feature-1.1 | Feature | {Title} | Draft | TBD-Epic-1 |
| TBD-Story-1.1.1 | User Story | {Title} | Draft | TBD-Feature-1.1 |
```
