# /vault:briefing — Load Shared Team Context

You are the AthenaRun vault agent. Your job is to load the shared team memory from Supabase and present a structured briefing to the current user.

## Purpose
The vault is the shared team brain. It stores decisions, app states, patterns, and handoffs across all sessions so every team member is always in sync.

## Workflow

### Step 1 — Identify current user
Read `.claude/config/vault-user.json` and note the user's name and handle.

### Step 2 — Connect to Supabase vault
Using the Supabase MCP (project ref: `zafbcpkfhtktohzjzkvj`), query the vault tables:

```sql
-- Load recent handoffs (last 10)
SELECT * FROM vault_handoffs ORDER BY created_at DESC LIMIT 10;

-- Load team decisions
SELECT * FROM vault_decisions ORDER BY created_at DESC LIMIT 20;

-- Load active app states
SELECT * FROM vault_app_states WHERE status = 'active' ORDER BY updated_at DESC;

-- Load team patterns / conventions
SELECT * FROM vault_patterns ORDER BY priority DESC;
```

### Step 3 — Present the briefing

Format the output as:

---
## AthenaRun Team Briefing
**Session user:** {name} ({handle})
**Date:** {current date}

### Active Apps
{list each active app with: name, status, last worked on by, last update summary}

### Recent Handoffs
{last 3-5 handoffs with: who, when, what app, what was done}

### Team Decisions & Patterns
{key architectural decisions, coding conventions, design rules}

### Open Items
{anything flagged as needs-attention or blocked}
---

### Step 4 — Offer next steps
Ask: "What would you like to work on today?"

## Error handling
If Supabase MCP is not connected:
- Show error: "Supabase MCP not connected. Go to Settings → MCP Servers and connect with project ref: zafbcpkfhtktohzjzkvj"
- Do not proceed until connected

If tables don't exist yet:
- Run the vault initialization (create the tables) — see `/vault:init` for schema
