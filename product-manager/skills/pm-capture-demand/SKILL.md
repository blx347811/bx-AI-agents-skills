---
name: pm-capture-demand
description: >
  Captures raw stakeholder input — meeting transcripts, demo notes, emails, architecture reviews — and produces a structured stage-1 demand note. Use whenever the user shares unstructured meeting notes, says "capture this feedback", "log what we discussed", "write up the demo notes", "document this stakeholder call", or provides a chunk of raw stakeholder input that needs to be turned into a referenceable artifact. Writes to the 1_UserDemand_TechnicalReviews/ folder of the active product. Also use proactively when the user pastes a block of unstructured notes alongside a product name.
---

# pm-capture-demand

Turns raw stakeholder input into a structured demand note that downstream PM stages can cite as evidence.

## Workflow

### Step 1 — Identify the input and product

Confirm:
- **Input:** transcript, email, freeform notes, or a mix — read from file or use pasted content as-is
- **Product:** which product/project this demand belongs to
- **Date:** from the content or ask the user (used in filename and header)
- **Meeting type:** Demo, Architecture Review, Stakeholder Sync, or other (used in filename)

### Step 2 — Locate the stage-1 folder

Look for a folder matching `1_UserDemand_TechnicalReviews/` (or similar) inside the product directory. If it does not exist, ask the user to confirm the path before writing.

### Step 3 — Match existing format

Scan the stage-1 folder for prior `.md` files. If they exist, open one and note its structure: section names, heading level, date format. The new artifact must match exactly. If the folder is empty, use the default format below.

### Step 4 — Extract content

Extract the following. If a section has no clear content in the input, write `[TBD]` — do not invent.

- **Quick Recap:** 2–4 sentence paragraph summarizing what was demonstrated, decided, or discussed. Past tense. No bullets.
- **Next Steps:** bulleted list of action items grouped by owner (`**Owner:**` prefix). One bullet per action. Include open items and follow-ups.
- **Summary sections:** 2–5 topical subsections covering the main threads of conversation. Each has a short `###` heading and 1–3 paragraph body. Do not duplicate the Quick Recap.
- **Flags for review:** Terms, claims, or statements in the input that are ambiguous, internally inconsistent, or use jargon that should be confirmed (e.g., product names, version numbers, attributed quotes). Format as a `>` blockquote callout with ⚠️ bullets. Omit this section entirely if there is nothing to flag.

### Step 5 — Draft the artifact

Show the full draft to the user, including the proposed filename (`{Product} - {Meeting Type} - {M.D}.md`), before writing. Wait for confirmation.

### Step 6 — Write the file

Write the `.md` file to the stage-1 folder. Report the full path on completion.

---

## Output format

```markdown
# Meeting Notes — {Product} — {Meeting Type} — {M.D}

## Quick Recap

{2–4 sentence paragraph. Past tense. No bullets.}

---

## Next Steps

- **{Owner}:** {Action}
- **{Owner}:** {Action}

---

## Summary

### {Topic 1}

{paragraph}

### {Topic 2}

{paragraph}

---

> **Flags for review:**
> - ⚠️ "{term or claim}" — {why this needs confirmation}
```
