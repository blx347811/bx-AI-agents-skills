# better-planning

Custom planning system with strict role separation.

## Agents

- **explore-scoped** (`agents/explore-scoped.md`) — Haiku. Read-only. Narrow file-bounded research, spawned by the planner command and update-context.

## Skills

- `/update-context` (`skills/update-context/SKILL.md`) — **The sole writer of CLAUDE.md.** Reviews drift flagged by the planner and applies updates with user approval.

## Commands

- `/planner <task>` — run the planner workflow in the main orchestrator, which produces a vetted plan and can spawn explore-scoped subagents as needed.

## Workflow

1. Start a session. CLAUDE.md loads automatically into the main agent's context.
2. For non-trivial tasks: `/planner <description>` → orchestrator runs the planning workflow and returns a vetted plan with citations.
3. If the plan ends with "Context Drift Detected," decide: run `/update-context` to address drift first, or proceed and update later.
4. To maintain CLAUDE.md on a cadence: run `/update-context` for a full audit, or scope it to a specific module.

## Design principles

- **Planner runs in the orchestrator.** The planning logic lives in the command, not a subagent, so it can spawn explore-scoped subagents via Task.
- **Single writer.** Only `/update-context` has Edit access to CLAUDE.md. Capability boundary matches trust boundary.
- **Template lives with the writer.** The CLAUDE.md template is baked into update-context's prompt. No drift between template and reality.
- **Citation discipline.** Every claim the planner makes about current behavior cites a `path:line`. If it can't be cited, the agent doesn't know it.
- **Git-based recency.** No daemon, no hooks. Git log is ground truth for recent activity.
- **User orchestrates.** Planner observes, update-context writes, you decide when to invoke each. No auto-updates.

## Files

```
├── README.md                       (this file)
├── agents/
│   └── explore-scoped.md
├── commands/
│   └── planner.md
└── skills/
    └── update-context/
        └── SKILL.md

CLAUDE.md                           (maintained by /update-context skill)
```
