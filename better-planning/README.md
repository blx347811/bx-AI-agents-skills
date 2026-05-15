# better-planning

Custom planning system with strict role separation.

## Agents

- **explore-scoped** (`agents/explore-scoped.md`) — Haiku. Read-only. Narrow file-bounded research, dispatched by the planner command and by update-context.
- **update-context** (`agents/update-context.md`) — Sonnet. **The sole writer of CLAUDE.md.** Receives a drift report from its parent and applies surgical edits directly. Dispatched by `/planner` and by `/update-context`.

## Commands

- `/planner <task>` — run the planner workflow in the main orchestrator (Opus). Produces a vetted plan, can dispatch explore-scoped for research, and can dispatch update-context when drift is detected.
- `/update-context [drift report or scope]` — ad-hoc CLAUDE.md refresh. Runs a focused mini-audit (or accepts a drift report) and dispatches the update-context agent.

## Workflow

1. Start a session. CLAUDE.md loads automatically into the main agent's context.
2. For non-trivial tasks: `/planner <description>` → orchestrator runs the planning workflow and returns a vetted plan with citations.
3. If the plan ends with "Context Drift Detected," decide: dispatch the update-context agent now (planner will offer), or proceed and refresh later.
4. To maintain CLAUDE.md on a cadence: run `/update-context` for a focused audit, or scope it to a specific area.

## Design principles

- **Planner runs in the orchestrator.** The planning logic lives in the command (Opus), not a subagent, so it can spawn explore-scoped and update-context via Task.
- **Single writer.** Only the `update-context` agent has Edit access to CLAUDE.md. Capability boundary matches trust boundary.
- **Writer isolation.** CLAUDE.md edits run in a Sonnet sub-agent so the planner's Opus context stays clean and the writer's tool surface stays narrow.
- **Template lives with the writer.** The CLAUDE.md template is baked into update-context's prompt. No drift between template and reality.
- **Citation discipline.** Every claim the planner makes about current behavior cites a `path:line`. If it can't be cited, the agent doesn't know it.
- **Git-based recency.** No daemon, no hooks. Git log is ground truth for recent activity.
- **User orchestrates.** Planner observes, update-context writes, you decide when to invoke each. No auto-updates.

## Files

```
├── README.md                       (this file)
├── agents/
│   ├── explore-scoped.md
│   └── update-context.md
└── commands/
    ├── planner.md
    └── update-context.md

CLAUDE.md                           (maintained by the update-context agent)
```
