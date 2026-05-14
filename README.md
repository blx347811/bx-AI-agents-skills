# bx-AI-agents-skills

Personal Claude Code plugin collection for Azure DevOps, Microsoft Copilot Studio authoring, and product management workflows.

## Overview

This repo is a [Claude Code plugin marketplace](https://docs.claude.com/en/claude-code/plugins) containing three plugins. Each plugin groups related skills (and optionally subagents) into a self-contained directory that Claude Code can install and invoke directly.

## Plugins

### `azure` — Azure DevOps CLI

Interact with Azure DevOps via the `az` CLI without leaving Claude Code.

| Skill | What it does |
|-------|-------------|
| `az-devops` | Query and browse work items (epics, features, stories, tasks, bugs), view sprint boards, drill into parent-child hierarchies, and list Git repositories. |

### `copilot-studio` — Copilot Studio Authoring

Author and maintain Microsoft Copilot Studio agents from the command line.

| Skill | What it does |
|-------|-------------|
| `new-topic` | Scaffold a new topic YAML file for a Copilot Studio agent. |
| `add-global-variable` | Add a global variable to an existing agent. |
| `add-logging` | Wire up logging nodes to a topic. |
| `edit-agent` | Make structural edits to an existing agent definition. |
| `best-practices` | Reference patterns for orchestrator variables, date context, child-agent response suppression, and topic redirects with variable passing. |

### `product-manager` — PM Lifecycle

End-to-end product management across a five-stage lifecycle, from raw stakeholder input to exec-ready strategy. Includes a `product-manager` subagent that orchestrates the full flow.

**Five stages:**

| Stage | Skill | Output |
|-------|-------|--------|
| 1 — Capture demand | `pm-capture-demand` | Structured demand note from meeting transcripts, demo notes, or stakeholder emails |
| 2 — Surface themes | `pm-surface-themes` | Clustered theme document, each theme backed by ≥2 demand sources |
| 3 — Author PRD | `pm-write-prd` | Product + technical design spec with decisions, alternatives rejected, and constraints named |
| 4 — Translate to work items | `pm-translate-to-workitems` | Epic → Feature → Story → Task drafts as local Markdown files |
| 5 — Exec narrative | `pm-exec-narrative` | One-page executive summary derived from the work item plan and PRD |

**Additional skills:**

| Skill | What it does |
|-------|-------------|
| `bx-ppt` | Generate a PowerPoint deck from a structured input using `pptxgenjs` (cross-platform). |
| `bx-ppt-COM` | Windows-specific variant that drives PowerPoint via COM automation for richer fidelity. |
| `sdd-generator` | Generate a Software Design Document from a PRD or set of work items. |

## Installation

> Requires Claude Code with plugin support enabled.

**Install all plugins at once:**

```bash
claude plugin install https://github.com/bryanxiao/bx-AI-agents-skills
```

**Or install a single plugin:**

```bash
claude plugin install https://github.com/bryanxiao/bx-AI-agents-skills/azure
claude plugin install https://github.com/bryanxiao/bx-AI-agents-skills/copilot-studio
claude plugin install https://github.com/bryanxiao/bx-AI-agents-skills/product-manager
```

After installation, skills are available as slash commands (e.g. `/az-devops`, `/pm-write-prd`) and the `product-manager` subagent is available via the agent picker.

## Repository Layout

```
bx-AI-agents-skills/
├── .claude-plugin/
│   └── marketplace.json        # Plugin marketplace manifest
├── azure/
│   ├── .claude-plugin/
│   │   └── plugin.json
│   └── skills/
│       └── az-devops/
│           └── SKILL.md
├── copilot-studio/
│   ├── .claude-plugin/
│   │   └── plugin.json
│   └── skills/
│       ├── add-global-variable/
│       ├── add-logging/
│       ├── best-practices/
│       ├── edit-agent/
│       └── new-topic/
└── product-manager/
    ├── .claude-plugin/
    │   └── plugin.json
    ├── agents/
    │   └── product-manager.md  # Subagent definition
    └── skills/
        ├── bx-ppt/
        ├── bx-ppt-COM/
        ├── pm-capture-demand/
        ├── pm-exec-narrative/
        ├── pm-surface-themes/
        ├── pm-translate-to-workitems/
        ├── pm-write-prd/
        └── sdd-generator/
```

Each skill lives in its own directory and exposes a `SKILL.md` as its entry point. Subagents are defined in `agents/*.md`.

## Adding a New Skill

1. Create a directory under the relevant plugin's `skills/` folder.
2. Add a `SKILL.md` with a YAML front-matter block (`name`, `description`, optional `argument-hint` and `allowed-tools`).
3. Add the skill name to the plugin's `plugin.json` if required by your Claude Code version.
4. Test by reloading the plugin in Claude Code and invoking the skill.

To add a new plugin, create a top-level directory with its own `.claude-plugin/plugin.json` and register it in `.claude-plugin/marketplace.json`.
