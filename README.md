# AthenaRun Toolkit

Autonomous software creation toolkit for the AthenaRun team.

## Setup (~10 minutes)

### Step 1 — Identity

**Michael:**
```bash
cp .claude/config/vault-user.michael.json .claude/config/vault-user.json
```

**Patrick:**
```bash
cp .claude/config/vault-user.patrick.json .claude/config/vault-user.json
```

### Step 2 — Connect Supabase MCP

In Claude Code → Settings → MCP Servers, connect Supabase and select project **AthenaRun** (`zafbcpkfhtktohzjzkvj`).

Or add to your global Claude config manually — see `.claude/settings.json` for the config.

### Step 3 — Install Context7

```bash
claude mcp add context7
```

### Step 4 — Install plugins

```bash
claude plugins add superpowers
claude plugins add frontend-design
```

### Step 5 — First run

```bash
claude
/vault:briefing
```

If you see team context load — you're ready.

---

## Available commands

| Command | Description |
|---|---|
| `/build:new-app` | Build a complete app from a description |
| `/build:iterate` | Fix bugs, add features, tweak UI on existing apps |
| `/build:app-presentation` | Generate branded PPTX decks |
| `/vault:briefing` | Load shared team context (run first every session) |
| `/vault:handoff <app>` | Save session work to shared team memory (run last) |
| `/vault:init` | Initialize vault tables in Supabase (run once) |

## Session workflow

1. `cd` to this folder
2. `claude`
3. `/vault:briefing` — always first
4. Do your work
5. `/vault:handoff <app-name>` — always last

## Presentation extras

```bash
pip install playwright python-pptx
playwright install chromium
```

## Troubleshooting

**Vault errors** → Supabase MCP not connected (Step 2 above)
**Outdated API errors** → Context7 not installed (Step 3 above)
**Build pipeline slow** → Normal for first run, libraries are being fetched
