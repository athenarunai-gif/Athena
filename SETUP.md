# AthenaRun Build System — Team Setup Guide

Hey guys, here's how to get the AthenaRun build system running on your machines.
Takes ~10 minutes.

## What you get

| Command | Description |
|---|---|
| `/build:new-app` | Build a complete app from a description |
| `/build:iterate` | Fix bugs, add features, tweak UI on existing apps |
| `/build:app-presentation` | Generate branded PPTX decks |
| `/vault:briefing` | Load shared team memory into your session |
| `/vault:handoff` | Save your session state for the team |

---

## Step 1 — Get the toolkit folder

I'll share the `team-toolkit/` folder with you (12 MB). Copy it somewhere on your machine, e.g.:

```
C:\Users\YourName\Documents\athenarun-workspace\
```

The folder already contains everything — skills, agents, commands, branding, UIKit.

---

## Step 2 — Set up your identity

Open a terminal **in the toolkit folder** and run the command for your name:

**Michael:**
```bash
cp .claude/config/vault-user.michael.json .claude/config/vault-user.json
```

**Patrick:**
```bash
cp .claude/config/vault-user.patrick.json .claude/config/vault-user.json
```

---

## Step 3 — Connect Supabase (shared memory)

In Claude Code, go to **Settings → MCP Servers** (or Integrations) and connect the Supabase integration.

When it asks you to pick a project, choose: **AthenaRun**
```
ref: zafbcpkfhtktohzjzkvj
```

> I'll make sure you're both added as project members in the Supabase dashboard.

---

## Step 4 — Install Context7 (library docs)

**Required** — all build agents use it to look up current documentation for libraries (React, FastAPI, shadcn, etc.) so they don't hallucinate outdated APIs.

```bash
claude mcp add context7
```

---

## Step 5 — Install plugins

```bash
claude plugins add superpowers
claude plugins add frontend-design
```

---

## Step 6 — First test run

Open a terminal **in the toolkit folder** and start Claude Code:

```bash
claude
```

Then type:

```
/vault:briefing
```

✅ **Success:** You see a big block of context (patterns, decisions, app state) — you're connected.
❌ **Error:** Ping with the error message — most likely Supabase MCP not connected (Step 3).

---

## How to write a good build prompt

The build pipeline is powerful but needs a solid prompt. You don't need to write it yourself — here's the workflow:

### 1. Start with a rough idea (2–3 sentences is fine)

> *"I want an app that tracks supplier delivery times and flags when someone is consistently late. Should have a dashboard."*

### 2. Let Claude refine it

Start Claude Code and say:

> *"I have an app idea: [your 2–3 sentences]. Help me turn this into a detailed prompt for our `/build:new-app` pipeline. Ask me questions about what I need."*

Claude will ask clarifying questions — who uses it, what data sources, what's the core workflow, what should the dashboard show, etc. Answer what you can, skip what you don't know yet.

### 3. Review the generated prompt

Claude produces something structured with target audience, core features, data model hints, and priorities. Tweak if needed.

### 4. Run the pipeline

```
/build:new-app
```

Then paste the refined prompt when it asks what to build.

> **The better the input prompt, the better the output.** "Better" doesn't mean longer — it means clearer on what problem it solves and who uses it. The pipeline figures out the technical *how*.

---

## Session workflow (important!)

Always follow this order:

```
1. Start Claude Code from the toolkit root folder
2. /vault:briefing        ← always first, loads shared team context
3. Do your work
4. /vault:handoff app-name ← always last, records what you did for the team
```

---

## Optional — Presentation generation

For `/build:app-presentation` you also need:

```bash
pip install playwright python-pptx
playwright install chromium
```

---

## Troubleshooting

**Most common issue:** Supabase MCP not connected (Step 3).

If something doesn't work, ping with the error message.
