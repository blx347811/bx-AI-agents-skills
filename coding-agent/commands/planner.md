---
description: Invoke the project planner for a non-trivial task
argument-hint: [task description]
allowed-tools: Task
---

Use the planner subagent to produce an implementation plan for the following task:

$ARGUMENTS

After the planner returns its plan, summarize the key decisions. If the plan ends with "Context Drift Detected," ask me whether to:
1. Invoke update-context to address the drift first, then re-plan
2. Proceed with the current plan and update docs later
3. Refine the plan further