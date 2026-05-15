# Project Claude Code setup

Custom planning system with strict role separation.

## Agents

- **planner** (`.claude/agents/planner.md`) — Opus. Read-only. Produces plans grounded in CLAUDE.md and current code state. Flags context drift; does not fix it.
- **explore-scoped** (`.claude/agents/explore-scoped.md`) — Haiku. Read-only. Narrow file-bounded research, used by planner and update-context.
- **update-context** (`.claude/agents/update-context.md`) — Sonnet. **The sole writer of CLAUDE.md.** Reviews the audit from the planner and applies updates with user approval.

## Commands

- `/plan <task>` — invoke the planner

## Workflow

1. Start a session. CLAUDE.md loads automatically into the main agent's context.
2. For non-trivial tasks: `/plan <description>` → planner returns a vetted plan with citations.
3. If the plan ends with "Context Drift Detected," decide: address drift first (`/update-context`), or proceed and update later.
4. To maintain CLAUDE.md on a cadence: `/update-context` for full audit, or `/update-context module map` for a scoped refresh.

## Design principles

- **Single writer.** Only update-context has Edit access to CLAUDE.md. Capability boundary matches trust boundary.
- **Template lives with the writer.** The CLAUDE.md template is baked into update-context's prompt. No drift between template and reality.
- **Citation discipline.** Every claim a planner makes about current behavior cites a `path:line`. If it can't be cited, the agent doesn't know it.
- **Git-based recency.** No daemon, no hooks. Git log is ground truth for recent activity.
- **User orchestrates.** Planner observes, update-context writes, you decide when to invoke each. No auto-updates.

## Files

```
.claude/
├── README.md                       (this file)
├── agents/
│   ├── planner.md
│   ├── explore-scoped.md
│   └── update-context.md
└── commands/
    └── plan.md

CLAUDE.md                           (maintained by update-context agent)
```