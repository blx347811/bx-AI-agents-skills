---
user-invocable: false
name: best-practices
description: "Best practices for Copilot Studio agents. Covers the shared OnActivity initialization pattern, dynamic topic redirects with Switch expressions, preventing child agents from responding directly to users, and silently managing connected agent I/O. USE FOR: OnActivity provisioning, conversation-init, personalized knowledge, dynamic redirect, Switch, BeginDialog, if/then/else replacement, child agent responses, completion setting, SendMessageTool, output variables, connected agents, connected agent inputs, connected agent outputs, global variables, External source can set the value, External source can receive the value, silent connected agent, dual assignment."
context: fork
agent: copilot-studio-author
---

# Copilot Studio Best Practices

**Only read the file relevant to the current task** — do NOT read all files.

## Dynamic Topic Redirect with Variable → [Topic-redirect-withvariable.md](Topic-redirect-withvariable.md)

Uses a `Switch()` Power Fx expression inside a `BeginDialog` node to dynamically redirect to different topics based on a variable value. Replaces complex if/then/else condition chains with a single, maintainable YAML pattern.

**Read this best-practice when:**
- The user needs to route to one of several topics based on a variable
- The user wants to replace nested ConditionGroup nodes with a cleaner approach
- The user asks about dynamic topic redirects or Switch expressions in BeginDialog

## Prevent Child Agent Responses → [prevent-child-agent-responses.md](prevent-child-agent-responses.md)

Prevents child agents from sending messages directly to the user. Clarifies the common misconception about the completion setting and provides the instruction block to force child agents to use output variables instead of `SendMessageTool`.

**Read this best-practice when:**
- The user wants a child agent to return data without messaging the user
- The user is confused about the completion setting on a child agent
- The parent agent needs to control all user-facing responses

## Silent Connected Agent Responses → [silent-connected-agent-responses.md](silent-connected-agent-responses.md)

Wires a connected agent to return data silently to the main agent via global variables, while the main agent owns all user-facing messaging. Covers the connected-agent-specific I/O plumbing (action-level `inputType`/`outputType`, external-source toggles, dual `Global`/`Topic` assignment) paired with the behavioral instruction block that prevents direct user messages.

**Read this best-practice when:**
- The user is building or invoking a connected agent and the main agent must own all messaging
- A connected agent's output is reaching the user when it shouldn't
- The main agent isn't receiving values back from a connected agent
- The user needs to understand how connected-agent I/O wiring differs from child-agent I/O wiring
- The agent you're invoking has its own agent.mcs.yml, settings.mcs.yml, and isAgentConnectable: true — i.e. it is a standalone publishable agent, not a topic-level module
- You need to create global variables for connected-agent I/O (see variable format note below)

**Before creating global variables:** read an existing variable file in the project first — do not guess property names from the UI labels. The correct YAML keys are `isExternalInitializationAllowed: true` (input — "External source can set the value") and `isOutputToExternalCallers: true` (output — "External source can receive the value"). Variables also require `name:`, `schemaName:` (`<agentSchemaName>.globalvariable.<VariableName>`), and `kind: GlobalVariableComponent` fields. The UI label text does not map 1:1 to YAML keys.

## Date Context → [date-context.md](date-context.md)

Provides the current date to the orchestrator through agent instructions using Power FX (`{Text(Today(),DateTimeFormat.LongDate)}`). Enables accurate responses to date-related questions by giving the orchestrator explicit awareness of "today" for interpreting relative timeframes.

**Read this best-practice when:**
- Users ask date-relative questions ("What's next week?", "upcoming events", "recent announcements")
- The agent needs to filter time-sensitive knowledge sources
- Date interpretation is causing confusion or hallucinations
- The agent handles schedules, calendars, deadlines, or time-sensitive content