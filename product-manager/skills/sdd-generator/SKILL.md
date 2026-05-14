---
name: sdd-generator
description: >
  Fills out a standard Solution Design Document (SDD) template for a Copilot, AI agent, or automation.
  Use this skill whenever the user mentions SDD, Solution Design Document, wants to document a Copilot or AI agent,
  or provides a description of an agent and asks to create documentation for it.
  The skill accepts any form of agent context (free-text description, meeting notes, uploaded docs)
  and produces a fully populated .docx file using the bundled SDD template.
---

# SDD Generator

Populates a standard SDD template (.docx) for a Copilot, AI agent, or automation.

## Workflow

### Step 1 - Gather context

Read everything the user has provided. You're looking for:
- **Agent name and purpose** - what it does and why
- **Tech stack** - platforms, APIs, data sources (Copilot Studio, Power Automate, Azure OpenAI, SharePoint, Bing, Dataverse, etc.)
- **Process flow** - trigger -> steps -> output
- **Key contacts** - Process SME, Process Owner (use [TBD] for anything not mentioned)
- **Restrictions** - data, user access, compliance constraints
- **Fallback behaviors** - what happens per failure scenario

Make reasonable inferences from the agent description for anything not explicitly stated. Use [TBD] for genuinely unknown values. Never leave a field empty - either populate it or use [TBD].

### Step 2 - Generate working/sdd_content.json

Write `working/sdd_content.json` using this schema:

```json
{
  "agent_name": "Human-readable name",
  "version": "1.0",
  "date": "YYYY-MM-DD",
  "author": "[TBD]",
  "purpose": "2-4 sentence paragraph describing what the agent does, why it exists, and what problem it solves.",
  "objectives": {
    "problem": "The specific inefficiency or gap this agent addresses.",
    "objective": "What the agent is designed to achieve.",
    "value": "Quantified or described business benefit.",
    "expected_outcome": "Measurable result once deployed."
  },
  "key_contacts": [
    {"role": "Process SME", "name": "Full Name", "email": "name@example.com"},
    {"role": "Process Owner", "name": "Full Name", "email": "name@example.com"},
    {"role": "Technical Lead", "name": "[TBD]", "email": "[TBD]"},
    {"role": "Business Sponsor", "name": "[TBD]", "email": "[TBD]"}
  ],
  "process_as_is": "Current manual or legacy process this agent replaces or augments.",
  "high_level_solution": "Overall solution architecture and how the agent works at a high level.",
  "applications": [
    {"name": "Platform name", "purpose": "Role in the agent", "owner": "Team or vendor", "access_method": "API / native connector / SDK"}
  ],
  "process_flow": [
    {"step": "1", "action": "Trigger event", "actor": "System or User", "output": "What is produced"}
  ],
  "process_steps_detail": "Narrative description expanding on the process flow table.",
  "restrictions": [
    {"restriction": "Constraint description", "rationale": "Why this restriction exists"}
  ],
  "prompt_logic": "Prompting strategy: system prompt purpose, context injection, RAG or reasoning patterns.",
  "prompts": [
    {"name": "Prompt name", "purpose": "What it does", "link": "[TBD]"}
  ],
  "fallback_actions": {
    "no_data_found": "Action when no relevant data is returned",
    "api_timeout": "Action when an external API times out",
    "low_confidence": "Action when model confidence is below threshold",
    "user_out_of_scope": "Action when user asks something outside agent scope",
    "auth_failure": "Action when authentication fails",
    "duplicate_detected": "Action when a duplicate record or request is detected",
    "data_quality_issue": "Action when input data is malformed or incomplete",
    "escalation_needed": "Action when the issue requires human escalation",
    "scheduled_job_failure": "Action when a scheduled trigger or batch job fails"
  },
  "test_cases": [
    {"id": "TC-01", "scenario": "Happy path", "expected": "Expected result"},
    {"id": "TC-02", "scenario": "Edge case", "expected": "Expected result"},
    {"id": "TC-03", "scenario": "Failure scenario", "expected": "Expected result"},
    {"id": "TC-04", "scenario": "Auth/permission test", "expected": "Expected result"},
    {"id": "TC-05", "scenario": "Data quality test", "expected": "Expected result"}
  ],
  "challenges": "Known risks, open questions, or implementation challenges.",
  "deployment_contacts": "Names and roles responsible for deployment sign-off.",
  "deployment_strategy": "Phased rollout plan, pilot group, environment promotion path.",
  "infrastructure": "Hosting, licensing, compute requirements, environment dependencies.",
  "training": "Training and change management plan for end users and support staff.",
  "feedback_loop": "How feedback is collected post-deployment and how the agent will be improved."
}
```

### Step 3 - Populate the template

Use the bundled helper script to create the final document:

```bash
python product-manager/skills/sdd-generator/scripts/populate_sdd.py working/sdd_content.json product-manager/skills/sdd-generator/assets/SDD_template.docx working/<agent-name>-SDD.docx
```

Create `working/` if it does not already exist. The output filename should be descriptive and end with `-SDD.docx`.
