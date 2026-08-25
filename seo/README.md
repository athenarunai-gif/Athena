# seo/

Workspace for the weekly AI-search routine. The routine itself lives in
`.claude/skills/weekly-seo/SKILL.md` and runs every Monday.

| Path | What it holds |
| --- | --- |
| `keywords.csv` | Every keyword considered, with `status`: `candidate` → `picked` → `keep` \| `drop` |
| `tracking.csv` | One row per keyword per week: did an AI answer cite us, or cite whom instead |
| `runs/<date>/` | That week's log, plus the YouTube script and chapter list |
| `outbox/` | Drafted emails and community answers — **a human sends these, never the agent** |

Published pages go to `content/` (English) and `content/de/` (German), built from
`.claude/skills/weekly-seo/references/page-template.html`.

## Running it by hand

`/weekly-seo` in Claude Code, or "run the weekly SEO routine". The scheduled Monday
run does the same thing on its own and reports back the human to-do list.

## What the agent will not do

It does not publish, email, post, or upload. Recording the video, sending the
outreach, posting the community answers, and reading Search Console are human steps —
each run's `log.md` ends with exactly that list.
