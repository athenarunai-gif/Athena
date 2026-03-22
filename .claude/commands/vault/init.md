# /vault:init — Initialize Vault Schema in Supabase

Run this once to set up the vault tables in the shared Supabase project.

## Workflow

Using the Supabase MCP (project ref: `zafbcpkfhtktohzjzkvj`), execute the following SQL:

```sql
-- Team handoff records
CREATE TABLE IF NOT EXISTS vault_handoffs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  app_name TEXT NOT NULL,
  user_handle TEXT NOT NULL,
  summary TEXT,
  completed JSONB DEFAULT '[]',
  in_progress JSONB DEFAULT '[]',
  decisions JSONB DEFAULT '[]',
  blockers JSONB DEFAULT '[]',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Active app states
CREATE TABLE IF NOT EXISTS vault_app_states (
  app_name TEXT PRIMARY KEY,
  status TEXT DEFAULT 'active',
  last_worked_by TEXT,
  last_summary TEXT,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Team-wide decisions
CREATE TABLE IF NOT EXISTS vault_decisions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  category TEXT,
  decision TEXT NOT NULL,
  rationale TEXT,
  made_by TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Coding / design patterns
CREATE TABLE IF NOT EXISTS vault_patterns (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  description TEXT,
  example TEXT,
  priority INT DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

Confirm each table was created successfully and report back.
