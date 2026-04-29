---
name: az-devops
description: >
  Use this skill whenever the user wants to interact with Azure DevOps (ADO) — listing projects,
  querying or browsing work items (epics, features, user stories, tasks, bugs), viewing work item
  details or drilling into parent-child hierarchies, or listing Git repositories. Trigger on any
  mention of Azure DevOps, ADO, work items, sprints, epics, stories, boards, repos, pipelines,
  iterations, or queries. Even vague requests like "what's in my sprint?" or "show me that ticket"
  or "list our repos" should use this skill.
---

# Azure DevOps CLI Skill

Use the `az devops` / `az boards` / `az repos` CLI to interact with Azure DevOps.

**Defaults already configured — no need to pass `--org` or `--project` for the Technology project:**
- Organization: `https://dev.azure.com/SolomonPartners`
- Project: `Technology`

Only pass `--project "OtherProject"` when the user targets a different project.

---

## Listing Projects

```bash
az devops project list --output table
```

---

## Querying Work Items

Use WIQL (Work Item Query Language) via `az boards query`. Always prefer `--output table` for
quick scans; switch to `--output json` when the user needs to process or filter results further.

> **Windows note:** On Windows, run `az` commands via the **PowerShell tool** (not Bash). Git
> Bash mishandles `az.cmd` argument passing, causing WIQL strings to be split incorrectly.

```powershell
az boards query --wiql "SELECT [System.Id], [System.Title], [System.WorkItemType], [System.State], [System.AssignedTo] FROM WorkItems WHERE <conditions> ORDER BY [System.ChangedDate] DESC" --output table
```

### Common WIQL patterns

**My active items in the current sprint:**
```bash
az boards query --wiql "SELECT [System.Id], [System.Title], [System.WorkItemType], [System.State] FROM WorkItems WHERE [System.TeamProject] = 'Technology' AND [System.AssignedTo] = @Me AND [System.IterationPath] = @CurrentIteration AND [System.State] NOT IN ('Closed', 'Removed') ORDER BY [System.ChangedDate] DESC" --output table
```

**All active items in a sprint (by path pattern):**
```bash
az boards query --wiql "SELECT [System.Id], [System.Title], [System.WorkItemType], [System.State], [System.AssignedTo] FROM WorkItems WHERE [System.TeamProject] = 'Technology' AND [System.IterationPath] UNDER 'Technology\\<SprintName>' AND [System.State] NOT IN ('Closed', 'Removed') ORDER BY [System.WorkItemType], [System.Id]" --output table
```

**By work item type:**
```bash
az boards query --wiql "SELECT [System.Id], [System.Title], [System.State], [System.AssignedTo] FROM WorkItems WHERE [System.TeamProject] = 'Technology' AND [System.WorkItemType] = 'User Story' AND [System.State] NOT IN ('Closed', 'Removed') ORDER BY [System.Id] DESC" --output table
```

**By assignee:**
```bash
az boards query --wiql "SELECT [System.Id], [System.Title], [System.WorkItemType], [System.State] FROM WorkItems WHERE [System.TeamProject] = 'Technology' AND [System.AssignedTo] = 'Full Name <email>' AND [System.State] NOT IN ('Closed', 'Removed') ORDER BY [System.ChangedDate] DESC" --output table
```

### Key WIQL fields
| Field | Description |
|---|---|
| `[System.Id]` | Work item ID |
| `[System.Title]` | Title |
| `[System.WorkItemType]` | Epic, Feature, User Story, Task, Bug |
| `[System.State]` | New, Active, Resolved, Closed, Removed |
| `[System.AssignedTo]` | Assigned person (use `@Me` for current user) |
| `[System.IterationPath]` | Sprint/iteration (use `@CurrentIteration` for current sprint) |
| `[System.AreaPath]` | Area path |
| `[System.ChangedDate]` | Last modified |
| `[System.Tags]` | Tags |

### Work item hierarchy
Epic → Feature → User Story → Task / Bug

---

## Work Item Details

```bash
# Full details — fields, relations, links
az boards work-item show --id <ID> --expand all --output json
```

For a readable summary, extract the most useful fields:
```bash
az boards work-item show --id <ID> --expand all --output json | python -c "
import json, sys
wi = json.load(sys.stdin)
f = wi['fields']
print(f'ID:          {wi[\"id\"]}')
print(f'Type:        {f.get(\"System.WorkItemType\", \"\")}')
print(f'Title:       {f.get(\"System.Title\", \"\")}')
print(f'State:       {f.get(\"System.State\", \"\")}')
assigned = f.get('System.AssignedTo', {})
print(f'Assigned To: {assigned.get(\"displayName\", \"\") if isinstance(assigned, dict) else assigned}')
print(f'Iteration:   {f.get(\"System.IterationPath\", \"\")}')
print(f'Area:        {f.get(\"System.AreaPath\", \"\")}')
print(f'Description: {f.get(\"System.Description\", \"\")[:500] if f.get(\"System.Description\") else \"\"}')
"
```

---

## Work Item Children

Children are linked via `System.LinkTypes.Hierarchy-Forward` relations.

**Step 1** — get the parent's relations:
```bash
az boards work-item relation show --id <PARENT_ID> --output json
```

**Step 2** — extract child IDs and fetch each child. Use this Python one-liner to do both in one shot:
```bash
az boards work-item relation show --id <PARENT_ID> --output json | python -c "
import json, sys, subprocess

data = json.load(sys.stdin)
child_urls = [r['url'] for r in data.get('relations', []) if r.get('rel') == 'System.LinkTypes.Hierarchy-Forward']
child_ids = [url.split('/')[-1] for url in child_urls]

if not child_ids:
    print('No children found.')
    sys.exit(0)

print(f'Found {len(child_ids)} child(ren): {child_ids}\n')
for cid in child_ids:
    result = subprocess.run(['az', 'boards', 'work-item', 'show', '--id', cid, '--expand', 'fields', '--output', 'json'], capture_output=True, text=True)
    wi = json.loads(result.stdout)
    f = wi['fields']
    assigned = f.get('System.AssignedTo', {})
    name = assigned.get('displayName', '') if isinstance(assigned, dict) else assigned
    print(f'  [{wi[\"id\"]}] {f.get(\"System.WorkItemType\",\"\")} | {f.get(\"System.State\",\"\")} | {name} | {f.get(\"System.Title\",\"\")}')
"
```

To go deeper (grandchildren), run the same pattern recursively on each child ID.

---

## Listing Git Repositories

```bash
# Repos in the Technology project (default)
az repos list --output table

# Repos in a different project
az repos list --project "OtherProject" --output table

# With clone URLs
az repos list --output json | python -c "
import json, sys
repos = json.load(sys.stdin)
for r in repos:
    print(f'{r[\"name\"]:<40} {r.get(\"remoteUrl\", \"\")}')
"
```

---

## Tips

- **Windows:** Always use the PowerShell tool (not Bash) for `az` commands. Git Bash mishandles `az.cmd` argument passing.
- Use `--output table` for human-readable listings, `--output json` when piping to Python for filtering or formatting.
- If the user asks about a specific work item number, use `az boards work-item show --id <N>`.
- If the user asks who owns something or what's in a sprint, write a WIQL query — it's the most flexible approach.
- For multi-level drilldowns (e.g., "show me Epic X and all its stories and tasks"), get the epic's children first, then get each child's children.
- State values vary slightly by work item type; when filtering by state, prefer `NOT IN ('Closed', 'Removed')` over listing specific active states.
- Python is available for post-processing JSON output — pipe `az ... --output json` into `python -c "..."` for clean formatted summaries.
