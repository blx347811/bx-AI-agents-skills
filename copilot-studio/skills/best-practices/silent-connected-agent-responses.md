# Silent Connected Agent Responses

Use this pattern when the main agent must own all user-facing messaging while a connected agent performs work silently and returns structured data. The main agent reads the connected agent's output from global variables and crafts the response itself.

## Connected Agent vs Child Agent

This skill applies specifically to **connected agents** — independent, reusable agents that can run standalone and serve multiple main agents. **Child agents** are fully owned by a single main agent and modularize logic within it. The distinction matters because their I/O wiring differs: child agent inputs/outputs sit at the root of the TaskDialog YAML, while connected agent inputs/outputs go inside `action`. See [prevent-child-agent-responses.md](prevent-child-agent-responses.md) for the child-agent equivalent.

## The Two Requirements

Silent operation requires **both** of the following. Either one alone is insufficient.

1. **Behavioral suppression** — instruction block in the connected agent's system instructions that forbids direct user messaging
2. **I/O plumbing** — global variables wired with the correct external-source toggles and dual assignment

## Behavioral Suppression

Add the following to the connected agent's system instructions. Without this, the agent's orchestrator may call `SendMessageTool` and write directly to the conversation.

```
CRITICAL - DO NOT MESSAGE USERS
- DO NOT respond directly to the user
- DO NOT call SendMessageTool or send any messages
- ONLY populate the output variables with your response
- Let the parent orchestrator deliver the response to the user
```

## I/O Plumbing for Connected Agents

### Variable configuration

For each value the main agent needs to receive:

- **Inputs** — mark the variable as global and enable **"External source can set the value"**
- **Outputs** — enable **"External source can receive the value"**

If the toggle is off, the variable looks correct in YAML but isn't exposed to the calling agent. State won't propagate.

### YAML placement

For connected agents, `inputType` and `outputType` go **inside `action`**, not at the root of the TaskDialog. This is different from child agents. Placing them at root causes a validation error or silent invocation failure.

```yaml
# Connected agent — correct placement
kind: AdaptiveDialog
beginDialog:
  kind: OnRecognizedIntent
  id: main
  intent: {}
  actions:
    - kind: SetVariable
      id: setResult
      variable: Global.AgentResult
      value: =Topic.AgentResult
    - kind: SetVariable
      id: setResultTopic
      variable: Topic.AgentResult
      value: =Topic.AgentResult

inputType:
  properties:
    userQuery:
      displayName: userQuery
      type: String

outputType:
  properties:
    AgentResult:
      displayName: AgentResult
      type: String
```

### Dual assignment — critical

The connected agent's standalone topic must assign its output to **both** the global variable and the topic variable:

- `Global.AgentResult` — this is what the main agent receives after invocation
- `Topic.AgentResult` — this makes the tool output visible in the test trace and to the action runner

Missing either assignment causes a silent partial failure: the value lands in one place but not the other.

## Implementation Steps

1. **Define global variables** on the connected agent for each input and output the main agent will exchange
2. **Enable toggles** — "External source can set the value" on inputs, "External source can receive the value" on outputs
3. **Place `inputType` / `outputType` inside `action`** in the connected agent's YAML, not at root
4. **Add dual `SetVariable` actions** in the connected agent's standalone topic — assign each output to both `Global.X` and `Topic.X`
5. **Add the no-messaging instruction block** to the connected agent's system instructions
6. **In the main agent**, read `Global.AgentResult` (or your named variable) after invoking the connected agent and use it to craft the user-facing message

## Common Failure Modes

| Symptom | Root cause |
|---|---|
| Main agent doesn't receive the output value | Missing `Global.X` assignment in the standalone topic, or "External source can receive the value" toggle is off |
| Tool output not visible in test trace | Missing `Topic.X` assignment — only `Global.X` was set |
| Connected agent messages the user directly | Missing behavioral instruction block |
| YAML validation error or agent can't be invoked | `inputType` / `outputType` placed at root instead of inside `action` |

## When to Use This Pattern

- The main agent must own tone, format and brand voice across all user-facing messages
- Multiple connected agents contribute partial results that the main agent combines before responding
- The main agent applies business logic, filtering or enrichment to the connected agent's output
- You want a reusable connected agent that doesn't leak messages when hosted by different main agents
