# /vault:handoff — Save Session Work to Shared Team Memory

You are the AthenaRun vault agent. Your job is to record what was accomplished in this session so the rest of the team is up to date.

## Usage
```
/vault:handoff <app-name>
```

## Purpose
Every session should end with a handoff. This is what keeps the shared vault accurate and ensures the next person (or next session) picks up exactly where you left off.

## Workflow

### Step 1 — Identify current user and app
- Read `.claude/config/vault-user.json` for the current user
- The app name comes from the command argument (ask if not provided)

### Step 2 — Review this session
Reflect on what happened in this session:
- What was the main goal?
- What was actually completed?
- What was started but not finished?
- Any bugs found or fixed?
- Any decisions made (tech choices, design choices, data model changes)?
- Any blockers or open questions for the team?

Ask the user to confirm or add anything missing.

### Step 3 — Write to Supabase vault

Using the Supabase MCP (project ref: `zafbcpkfhtktohzjzkvj`), insert records:

```sql
-- Insert handoff record
INSERT INTO vault_handoffs (
  app_name, user_handle, summary, completed, in_progress, decisions, blockers, created_at
) VALUES (
  '{app_name}',
  '{user_handle}',
  '{one-paragraph summary}',
  '{JSON array of completed items}',
  '{JSON array of in-progress items}',
  '{JSON array of decisions made}',
  '{JSON array of blockers/open questions}',
  NOW()
);

-- Upsert app state
INSERT INTO vault_app_states (app_name, status, last_worked_by, last_summary, updated_at)
VALUES ('{app_name}', 'active', '{user_handle}', '{brief status}', NOW())
ON CONFLICT (app_name) DO UPDATE SET
  status = EXCLUDED.status,
  last_worked_by = EXCLUDED.last_worked_by,
  last_summary = EXCLUDED.last_summary,
  updated_at = EXCLUDED.updated_at;
```

If any new patterns or team decisions were made, also insert into `vault_decisions` or `vault_patterns`.

### Step 4 — Confirm handoff
Display a summary of what was saved:

---
## Handoff Saved
**App:** {app_name}
**By:** {user_handle}
**Time:** {timestamp}

**Completed:**
{bullet list}

**In progress:**
{bullet list}

**Decisions:**
{bullet list}

**Open items for team:**
{bullet list}
---

The team vault is now up to date. See you next session!

## Error handling
If Supabase MCP is not connected:
- Show error and instruct user to connect before ending the session
- Offer to print the handoff summary to copy manually
