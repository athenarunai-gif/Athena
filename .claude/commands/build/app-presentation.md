# /build:app-presentation — Generate Branded PPTX Decks

You are the AthenaRun presentation agent. Generate a polished, branded PowerPoint deck for an app built with the AthenaRun toolkit.

## Requirements
- Python with `python-pptx` installed
- Playwright with Chromium: `playwright install chromium`
- Run: `pip install playwright python-pptx` if not already done

## Pre-flight

1. Read `.claude/config/vault-user.json` to identify the presenter.
2. Ask which app this presentation is for.
3. Load any relevant vault context about the app.

## Workflow

### Step 1 — Gather content
Ask the user:
- What is the presentation for? (client pitch / internal review / demo)
- Who is the audience?
- How many slides? (default: 8-12)
- Any specific sections to include or exclude?

### Step 2 — Plan slide structure
Default deck structure:
1. Title slide (app name, tagline, presenter)
2. Problem statement
3. Solution overview
4. Key features (1 slide per major feature, max 3)
5. Live demo / screenshot slide
6. Technical architecture (optional)
7. Next steps / roadmap
8. Q&A / contact

### Step 3 — Generate the deck

Write a Python script using `python-pptx` that:
- Uses AthenaRun brand colors: background `#1a1a2e`, accent `#e94560`, text white/light gray
- Sets slide dimensions to 16:9 (33.87cm × 19.05cm)
- Applies consistent typography (Inter font family, fallback Calibri)
- Generates each slide with proper layouts
- Saves as `<app-name>-presentation.pptx`

For screenshot slides, use Playwright to capture the running app at `localhost:3000` (or ask for the URL).

### Step 4 — Execute and deliver
Run the generated Python script and confirm the file was created.
Tell the user the output file path.

## Brand guidelines
- Primary background: `#1a1a2e`
- Accent / highlight: `#e94560`
- Secondary accent: `#16213e`
- Body text: `#e0e0e0`
- Heading text: `#ffffff`
- Font: Inter (or Calibri as fallback)
- Minimal slide layouts — no clip art, no gradients except subtle dark ones
- Icons via text (Unicode) or omit
