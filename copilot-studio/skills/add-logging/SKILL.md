---
user-invocable: false
description: Add a Logging Topic to a Copilot Studio agent that fires a custom telemetry event once per conversation on the first user message. Use when the user wants to capture session-start telemetry (e.g., signed-in email, tenant, locale) via Application Insights without prompting the user.
argument-hint: <event name and property to log>
allowed-tools: Read, Write, Glob, Grep
context: fork
agent: copilot-studio-author
---

# Add Logging Topic

Create a silent "session-start" telemetry topic that logs one or more `LogCustomTelemetryEvent` actions exactly once per conversation, gated by a `Global.HasLoggedStart` idempotency flag.

## When to Use

- The user wants to record that a conversation started (and by whom) without adding any user-visible message.
- The user wants to emit telemetry for dashboards / Application Insights queries keyed on signed-in identity, tenant, channel, locale, or any Power Fx–derivable value.
- The user wants telemetry fired at most once per conversation, not on every turn.

If the user wants telemetry on a *specific* event (e.g., after a successful search), this skill is not the right fit — add a `LogCustomTelemetryEvent` action inline in the relevant topic instead.

## Instructions

1. **Auto-discover the agent directory**:
   ```
   Glob: **/agent.mcs.yml
   ```
   Use the top-level agent. NEVER hardcode an agent name.

2. **Read `settings.mcs.yml`** to get the `schemaName` prefix (needed for the idempotency global variable):
   ```
   Read: <agent-dir>/settings.mcs.yml
   ```
   Extract the root-level `schemaName` (e.g., `cree7_techEmailGeneratorBx`).

3. **Gather inputs from the user** (ask follow-ups if any are missing):
   - **Event name(s)** — one or more PascalCase identifiers (e.g., `UserEmail`, `SessionStart`, `TenantId`). These appear as `customEvents` in Application Insights.
   - **Property value(s)** — the Power Fx expression evaluated when the event fires. Common choices:
     - `=System.User.Email` — signed-in user's email (requires `authenticationMode: Integrated` or `ManualAuthentication`).
     - `=System.User.DisplayName` — signed-in display name.
     - `=System.User.Id` — AAD object id.
     - `=System.Conversation.Id` — conversation id, for correlating turns across events.
     - `=System.Activity.ChannelId` — Teams vs. M365 Copilot vs. web.
     - Any literal or composed expression, e.g., `="agent-v2"`.
   - **Idempotency flag name** — default `HasLoggedStart`. Only change if one already exists with a different name.

4. **Ensure the idempotency global variable exists** at `<agent-dir>/variables/HasLoggedStart.mcs.yml`. If it doesn't, create it:

   ```yaml
   # Name: Has Logged Start
   # Idempotency flag for the Logging Topic; set to true after the first-message telemetry fires so it won't fire again this conversation.
   name: HasLoggedStart
   aIVisibility: HideFromAIContext
   scope: Conversation
   description: True after the Logging Topic has fired once this conversation. Prevents duplicate session-start telemetry.
   schemaName: <prefix>.globalvariable.HasLoggedStart
   kind: GlobalVariableComponent
   defaultValue: DEFAULT
   ```

   - `aIVisibility: HideFromAIContext` — the orchestrator has no reason to reason about this flag.
   - `scope: Conversation` — matches the fire-once-per-conversation semantic.
   - Replace `<prefix>` with the `schemaName` read from `settings.mcs.yml`.

5. **Create the topic file** at `<agent-dir>/topics/LoggingTopic.mcs.yml`:

   ```yaml
   mcs.metadata:
     componentName: Logging Topic
   kind: AdaptiveDialog
   beginDialog:
     kind: OnActivity
     id: main
     condition: =IsBlank(Global.HasLoggedStart) || Global.HasLoggedStart = false
     type: Message
     actions:
       - kind: LogCustomTelemetryEvent
         id: logEvent_<rand>
         eventName: <EventName>
         properties: =<PowerFxExpression>

       # ...repeat LogCustomTelemetryEvent for each additional event...

       - kind: SetVariable
         id: setFlag_<rand>
         variable: Global.HasLoggedStart
         value: true

   inputType: {}
   outputType: {}
   ```

   - `type: Message` — fires on user messages only; not on `ConversationUpdate`, typing indicators, etc. This is deliberate: `ConversationUpdate` can fire with no signed-in identity populated yet, which would log blanks.
   - `condition` — the guard that makes this fire-once. Uses `IsBlank(...) || ... = false` so it works both on a fresh conversation (flag undefined) and on explicitly-reset conversations (flag set back to false).
   - `SetVariable` on `Global.HasLoggedStart` **must be the last action** — if an earlier action errors out, the flag stays false and the next message will retry. Put it last only if you want at-most-once; put it first if you want at-least-once-ish (the logger fires once even if a later action fails).
   - Use fresh random 6-char IDs per action (e.g., `mY6zsD`, `QJiFjh`). Don't reuse IDs across actions.

6. **Verify after writing**:
   - Open `<agent-dir>/variables/HasLoggedStart.mcs.yml` and confirm `schemaName` matches `<settings-schemaName>.globalvariable.HasLoggedStart`.
   - Open the new topic and confirm the `Global.HasLoggedStart` reference matches the variable name exactly (case-sensitive).

## Multiple Events in One Topic

Prefer one `LogCustomTelemetryEvent` per distinct event name rather than stuffing everything into one event's `properties`. Application Insights `customEvents` is keyed on `name`, so separate events = separate rows and cleaner Kusto queries. Example:

```yaml
- kind: LogCustomTelemetryEvent
  id: logEmail_aB3xYz
  eventName: UserEmail
  properties: =System.User.Email

- kind: LogCustomTelemetryEvent
  id: logChannel_qR7mLw
  eventName: SessionChannel
  properties: =System.Activity.ChannelId
```

## Authentication Caveat

`System.User.Email` / `System.User.Id` are only populated when `authenticationMode` in `settings.mcs.yml` is `Integrated` or `ManualAuthentication`. If the agent is unauthenticated, the telemetry will log empty strings. Check `settings.mcs.yml` before promising the user that email logging will work, and warn them if the agent is configured for anonymous access.

## Related Skills

- `/copilot-studio:add-global-variable` — use this pattern if the user wants the idempotency flag (or any other variable) configured with full options (e.g., a non-default initial value, `UseInAIContext`).
- `/copilot-studio:best-practices` → `orchestrator-variables.md` — background on when to use `UseInAIContext` vs. `HideFromAIContext`.
