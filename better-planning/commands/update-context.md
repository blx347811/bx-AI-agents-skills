---
description: Audit CLAUDE.md for drift and dispatch the update-context agent to apply fixes
argument-hint: [optional drift report or area to audit]
allowed-tools: Read, Glob, Grep, Task, Bash(git log:*)
---

You are running an ad-hoc CLAUDE.md refresh. Your job is to produce a focused drift report and hand it to the `update-context` agent, which applies the edits.

The user-supplied argument is:

$ARGUMENTS

## Workflow

### 1. Decide your input mode

- If `$ARGUMENTS` already contains a drift report (e.g., output from `/planner`), use it directly. Skip to step 3.
- If `$ARGUMENTS` is empty or names a scope ("audit the module map", "review recently-active"), run the mini-audit in step 2.

### 2. Mini-audit

Produce a short drift report. This is intentionally narrow — not a full planner workflow.

- Read `CLAUDE.md`. If it does not exist, tell the user and stop.
- Run `git log --name-only --pretty=format: --since="2 weeks ago" | sort | uniq -c | sort -rn | head -30` to surface recently active files.
- Compare the observed top files against CLAUDE.md's `## Module map` and `## Recently active modules` sections. Flag entries that look stale, missing, or contradicted.
- If the user named a scope, restrict the comparison to that scope.

Do **not** dispatch `explore-scoped` here. The agent does its own narrow verification.

The drift report should be a plain bullet list:

```
- Module map: `foo/` missing — 12 commits in last 2 weeks
- Recently active: `legacy/` listed but no commits in 90 days
- Stack: line says "Pydantic v1" but pyproject.toml may have moved to v2 (verify)
```

### 3. Dispatch the agent

Call the `update-context` agent via the Task tool. Pass the drift report as the prompt, prefaced with one line of context (e.g., "Drift report from /update-context ad-hoc audit:").

### 4. Relay the result

When the agent returns, surface its full output to the user verbatim — especially the "Flagged for human review" section. Those items are not auto-applied; the user decides whether to incorporate them by editing CLAUDE.md manually or running a follow-up.

If the agent returns `Status: unable to apply`, report the reason to the user and stop.

## Constraints

- **Read-only on everything except via the agent.** You do not edit CLAUDE.md directly — only the `update-context` agent has Edit access.
- **Keep the audit narrow.** This command is not a planner. If the user wants a full audit-and-plan loop, point them to `/planner` instead.
- **No silent edits.** Always relay what the agent applied and what it flagged.
