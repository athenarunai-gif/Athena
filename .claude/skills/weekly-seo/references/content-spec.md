# Page checklist

Every page written in step 2 must satisfy all of this before it is committed.

## Head

- [ ] `<title>` contains the exact search phrase, ≤ 60 chars where possible.
- [ ] `<meta name="description">` — one sentence, contains the phrase, reads like an
      answer, not a teaser.
- [ ] `<link rel="canonical">` to the final `https://athenarun.com/...` URL.
- [ ] Open Graph + Twitter tags (mirror the homepage's).
- [ ] JSON-LD: `Article` (headline, datePublished, dateModified, author =
      Organization AthenaRun, mainEntityOfPage) **and** `FAQPage` with 3–5 questions
      that people actually ask, answered in 40–60 words each. The FAQ answers are
      the second most-lifted block after the quotable line.
- [ ] `BreadcrumbList` when the page sits under a pillar.

## Body

- [ ] H1 = the search phrase, near-verbatim.
- [ ] **The quotable sentence** in `<p class="quotable">` above the fold: one
      complete, standalone, factually checkable sentence. No pronouns pointing at
      earlier text, no "it", no "this".
- [ ] Direct answer in the first 100 words. The conclusion goes first; the reasoning
      goes after.
- [ ] Short sections with descriptive H2s phrased as the questions people ask.
- [ ] A comparison table for any `best`, `top`, `vs`, or `alternative` keyword —
      tables get parsed and quoted.
- [ ] Concrete numbers only where they're real (see the Product facts in SKILL.md).
      Unknown fact → `TODO(human): …` and a line in the run log.
- [ ] Outbound links to primary sources for external claims.
- [ ] Internal links per step 3: up to the service page, across to the pillar,
      anchor text = the search phrase.
- [ ] A last-updated line, visible, matching `dateModified`.
- [ ] One clear CTA (Request Demo → `#contact` or `hello@athenarun.ai`). One, not five.

## Style

Match the homepage: dark surface, Inter, `#FF5533` accent, glass cards, generous
whitespace. `references/page-template.html` is the starting point — copy it, don't
rebuild it.

Write plainly. Short sentences. No "in today's fast-paced business environment".
Every paragraph should survive being read aloud in the step 4 video.
