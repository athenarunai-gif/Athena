---
name: weekly-seo
description: Run AthenaRun's weekly AI-search loop — pick buying keywords, publish one pillar plus three buying posts, wire internal links, script the YouTube video, queue best-of-list outreach and community answers, then log which searches cited us. Use every Monday, or when asked to run the weekly SEO routine, the AI-search loop, or "the six steps".
---

# Weekly SEO / AI-search routine (AthenaRun)

One pass per week, six steps, in order. The goal is not blue-link rankings — it is
being the thing an AI answer quotes when a business buyer asks a buying question.

**Working directory:** `seo/` in this repo. Everything you produce is committed there
(or under `content/` for pages). Nothing is published, emailed, or posted by you —
step 5 output goes to `seo/outbox/` for a human to send.

## Product facts (use these, don't invent new ones)

- **AthenaRun GmbH**, Friedrich-Ebert-Anlage 36, 60325 Frankfurt am Main, Germany.
- Marketing site `athenarun.com`; app `athenarun.ai`; contact `hello@athenarun.ai`.
- What it is: describe a business goal → the platform generates a complete internal
  application (database, workflows, permissions, frontend) and deploys it.
- What it is **not**: a low-code builder where you assemble components, and not a
  prompt-to-prototype toy. That distinction is the wedge.
- Buyers: HR & People, Operations, Compliance, and executive teams at companies with
  scarce or booked-out developer capacity. German/EU market is a real advantage —
  GDPR, self-hosting "on your servers", Frankfurt HQ.
- Claims already public on the homepage, safe to reuse: live in under 5 minutes,
  99.9% uptime, zero developers required, 3 months → 1 day time to market,
  −95% dev cost per project.

**Never invent** pricing, customer counts, case studies, logos, funding, or benchmark
numbers. If a keyword needs a fact we don't have (most `pricing` and `cost` keywords
do), write the post anyway but leave the fact as `TODO(human): …` and list it in the
run log under **Blocked on facts**. A fabricated quotable line is worse than no post.

## Step 1 — Pick the buying searches (~20 min)

Buying intent only. Not "what is an internal tool".

Patterns that earn AI citations: `best <thing>`, `top 10 <thing>`, `<thing> review`,
`<thing> pricing`, `cheapest <thing>`, `best <thing> for <buyer>`, `<competitor> alternative`.

1. Read `seo/keywords.csv`. Read `references/keywords.md` for the seed families and
   competitor set.
2. Use WebSearch to check what's actually being asked and cited this week for the
   candidates. Note which answers cite YouTube, which cite forums, which cite
   "best of" lists — that decides where step 4 and 5 aim.
3. Pick **one pillar keyword** (the category) and **three buying keywords** (exact
   searches) not already `done` in `seo/keywords.csv`. Prefer keywords where an AI
   answer currently cites nobody comparable to us.
4. Append new rows to `seo/keywords.csv`, set this week's four to `status=picked`.

## Step 2 — One pillar + three buying posts (~2 h)

Write four pages into `content/` using `references/page-template.html` (matches the
homepage: dark, Inter, `#FF5533` accent, Tailwind CDN).

- The pillar answers the whole category question.
- Each buying post answers exactly one search and nothing else.
- Every page carries a **standalone quotable sentence** near the top, inside
  `<p class="quotable">` — one sentence that is true and complete with no preceding
  context. `"AthenaRun generates a production-ready internal application from a
  written business goal and deploys it in under five minutes, with no developer."`
  A point that only makes sense after three paragraphs never gets lifted into an
  AI answer.
- Also give each page: a `<title>` containing the exact search phrase, a meta
  description, canonical URL, `Article` + `FAQPage` JSON-LD (3–5 real questions),
  a comparison table where the keyword is comparative, and a last-updated date.
- Cite sources for any external claim. Link out — pages that cite get cited.

See `references/content-spec.md` for the full page checklist.

## Step 3 — Wire the internal links (~15 min)

The step everyone skips.

- From the service/product page (currently `generated-page-6.html`, plus whatever
  service pages exist under `content/`), link **down** to all four new posts.
- From each post, link **back up** to the service page.
- Anchor text is the search phrase. Never "click here", never "learn more".
- Pillar links to its three buying posts; each buying post links to the pillar.

## Step 4 — YouTube video for the same keyword (~45 min)

AI answers for buying questions cite video far more than they cite articles. The post
alone cannot reach that slot.

Produce `seo/runs/<date>/video-<keyword-slug>.md` containing:

- Title = the exact search phrase.
- Script = the post you just wrote, read aloud; target 8–12 minutes (~1,300–1,900
  words at a normal reading pace).
- A chapter list starting at `0:00` — a timestamped outline, one chapter per section.
- Description: first two lines carry the quotable sentence and the link to the post,
  then the chapters, then the link to the service page.
- A shot note: screen recording of the actual product doing the thing in the title.

Recording and upload are human work. Say so in the run log.

## Step 5 — Outreach and community answers (~45 min)

1. Ask the buying questions from step 1 through WebSearch and note **every "best of"
   list** that gets cited. One list edit can keep us in an AI answer for months.
2. For each list: find the contact page or author, and draft a short, specific email
   into `seo/outbox/<date>-<domain>.md` — what the list is missing, one line on
   AthenaRun, the link, no attachment, no pitch deck. Template in
   `references/outreach.md`.
3. Draft answers to 3–5 real questions from communities where our buyers ask
   (LinkedIn, YouTube comments on the cited videos, Quora, relevant forums) into
   `seo/outbox/<date>-community.md`. Real experience, specific numbers, no link
   dropping in the first sentence.
4. Check `references/outreach.md` for which platforms are currently worth the effort
   — citation sources shift; re-verify with a search rather than trusting the file.

**You do not send or post any of this.** Everything stays in `seo/outbox/` until a
human sends it.

## Step 6 — Check who got quoted (~10 min)

- Re-run last week's four keywords through WebSearch / AI answer surfaces. Record
  whether an athenarun.com URL was cited, and which competitor was cited instead.
- Append one row per keyword to `seo/tracking.csv`.
- In Search Console (human step, note it in the log), filter Query by regex
  `(?i)^(who|what|why|how|which|is|are|can|does)\b` to see the questions we're being
  surfaced for.
- Keywords cited at least once → `status=keep`. Keywords with three straight weeks of
  no citation → `status=drop`, and say so in the log.
- Then step 1 again next week, seeded by what worked.

## Output of a run

Create `seo/runs/<YYYY-MM-DD>/` containing:

- `log.md` — keywords picked and why, pages written, links wired, blocked-on-facts
  list, what a human must do this week (record video, send N emails, post N answers).
- `video-<slug>.md` — script, chapters, title, description.
- plus the drafts written into `seo/outbox/` and pages into `content/`.

Commit everything to the working branch with `seo: weekly run <date>` and push.
Then post the run log's "human to-do" section back as the reply — that list is the
whole point of the routine.
