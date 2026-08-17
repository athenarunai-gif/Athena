"""Rebuild slides 1-7 of the AthenaRun pitch deck.

Slides 8-12 are left untouched. Everything here reuses the existing corporate
identity (see ci.py): same typefaces, same type sizes, same palette, same
hairline/node/gate motifs. What changes is layout, information architecture and
the quality of the visualisation.
"""
import os
import shutil
import zipfile

from ci import *  # noqa: F401,F403
import ci

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "Pitch_Deck_AthenaRun_v3.pptx")
UNPACKED = os.path.join(HERE, "build_unpacked")
OUT = os.path.join(HERE, os.pardir, "Pitch_Deck_AthenaRun_v4.pptx")

RAIL_Y = 2.86          # shared chain-rail centre line for slides 3 and 4
NODE_TOP = RAIL_Y - NODE_D / 2
NUM_Y = RAIL_Y - 0.105
NAME_Y = 3.24
SUB_Y = 3.49
LEGEND_Y = 3.92
BAND_Y, BAND_H = 4.36, 0.34
OUT_CARD_Y, OUT_CARD_H = 5.50, 0.86

# The two chain slides became one, so the deck is eleven slides. Rather than
# renumber every part, the dropped slide is simply removed from <p:sldIdLst> and
# the six rebuilt slides are written onto the parts that survive, in order.
SLIDE_PARTS = [1, 2, 3, 5, 6, 7]
DROPPED_PART = 4
ORIGINAL_PARTS = [8, 9, 10, 11, 12]


# --------------------------------------------------------------------------
# shared chain components
# --------------------------------------------------------------------------
def rail_node(cx, num):
    return [
        ellipse(cx - NODE_D / 2, NODE_TOP, NODE_D),
        text(cx - 0.28, NUM_Y, 0.56, 0.21,
             run(num, 1300, MUTED, font=MONO), align="ctr"),
    ]


def rail_stage(cx, name, sub):
    return [
        text(cx - 1.11, NAME_Y, 2.22, 0.24, run(name, T_STAGE, TEXT), align="ctr"),
        text(cx - 1.11, SUB_Y, 2.22, 0.18, run(sub, T_STAGE_SUB, MUTED), align="ctr"),
    ]


def gate_legend(x=9.10, y=LEGEND_Y):
    """Legend for the diamonds on the rail. Parked at the right so the LEARN
    return path on slide 4 has the left half of the slide to itself."""
    return [
        diamond(x + 0.05, y + 0.09),
        micro(x + 0.22, y + 0.02, "HUMAN GATE AT EVERY TRANSITION", w=3.24, spc=150),
    ]


def ai_band(x0, x1, label="AI AGENTS SUPPORT EVERY STAGE"):
    """The continuous coverage bar under the rail — the counterpart to the
    discrete gate diamonds on it."""
    return [
        card(x0, BAND_Y, x1 - x0, BAND_H, fill=CARD2, line=DIM),
        text(x0, BAND_Y + 0.09, x1 - x0, 0.17,
             run(label, T_MICRO, MUTED, font=MONO, spc=200), align="ctr"),
    ]


def from_to(left, right):
    return [
        micro(M, 2.18, left, w=5.0, color=DIM, spc=200),
        micro(7.56, 2.18, right, w=5.0, color=DIM, spc=200, align="r"),
    ]


def outcome_card(label, statement, accent_label=False):
    return [
        card(M, OUT_CARD_Y, W, OUT_CARD_H),
        micro(M + 0.32, OUT_CARD_Y + 0.20, label, w=6.0,
              color=ACCENT if accent_label else MUTED, spc=200),
        text(M + 0.32, OUT_CARD_Y + 0.48, W - 0.64, 0.24,
             run(statement, T_LEAD, TEXT, bold=True)),
    ]


# --------------------------------------------------------------------------
# slide 1 — cover
# --------------------------------------------------------------------------
COVER_SUB_COLOR = "C9C9CE"   # sampled out of the original cover artwork
T_HERO = 4800                # measured off the original artwork: 48pt

# Glyph-top positions measured in the original 1920x1080 cover bitmap, converted
# to inches. The two hero lines sit 0.8125in apart; keeping that delta fixed makes
# the leading exact regardless of how the renderer resolves font metrics.
HERO_LEAD = 0.8125
COVER_SUB_Y = 4.618 - 0.048  # same gap, scaled to 17pt

# Candidate openers, as (line 1, line 2, hero size). At the artwork's original
# 48pt a hero line fits about 33 characters; C carries the founders' sentence
# verbatim and has to drop to 39pt to fit, which costs a fifth of the hero.
COVER = {
    "A": ("AI writes code.", "It doesn’t finish applications.", 4800),
    "B": ("Code generation is solved.", "Finished applications are not.", 4800),
    "C": ("AI writes code.", "It doesn’t deliver finished applications.", 3900),
}
COVER_VARIANT = "A"

COVER_SUB = ("Enterprise-grade means integrated, tested, audit-proof and "
             "signed off by a person.")
COVER_THESIS = "We deliver the finished application."


def slide1():
    """Cover, fully live text: the claim moves from process ("the chain") to
    outcome ("the finished application")."""
    line1, line2, size = COVER[COVER_VARIANT]
    scale = size / T_HERO
    # 33 characters fit at 48pt; the budget grows as the type shrinks
    for line in (line1, line2):
        assert len(line) <= round(33 / scale), (line, len(line))

    y = 2.708 - 0.136 * scale
    lead = HERO_LEAD * scale
    s = [backdrop()]
    for ry in COVER_RULE_Y:
        s += [hairline(ry, color=COVER_RULE_COLOR)]
    s += [text(0.77, y, 12.0, 0.80 * scale, run(line1, size, TEXT, bold=True))]
    s += [text(0.77, y + lead, 12.0, 0.80 * scale, run(line2, size, MUTED))]
    s += [text(0.77, COVER_SUB_Y, 11.00, 0.24, run(COVER_SUB, T_STAGE, COVER_SUB_COLOR))]
    s += [text(M, 5.02, 9.0, 0.28, run(COVER_THESIS, T_STAGE, ACCENT, bold=True))]
    # the cover wore a larger logo than the content slides; placed so the glyphs
    # land exactly where the artwork had them
    s += [pic(0.660, 6.521, 1.775, 0.418, "rId2", name="Logo")]
    return s, ["image16.png"]


# --------------------------------------------------------------------------
# slide 2 — why systems are hard, and what that costs
# --------------------------------------------------------------------------
# The four conditions are exactly the four things the three shipped systems had
# to solve; none of them is a claim about the customer's own organisation, which
# is what made "still manual" contestable.
HARD = [
    ("Context", "It needs the house rules, the data model and the edge cases. "
                "A prompt does not carry them."),
    ("Integration", "It has to live inside ERP, Slack and the document store, "
                    "not in a sandbox."),
    ("Verification", "Someone signs the output. That takes tests, calibration "
                     "and an audit trail."),
    ("Accountability", "A person owns the decision. That takes gates, not autonomy."),
]


def slide2():
    s = [backdrop()]
    s += header("Everyone builds tools.", " Systems are the hard part.", "The problem")
    s += [text(M, 1.42, 10.42, 0.50,
               run("Code is the cheap part now. What still fails is everything that has "
                   "to be true before someone signs off on the result.", T_LEAD, MUTED))]

    s += [hairline(2.10)]
    s += [eyebrow(M, 2.28, "WHAT SEPARATES A TOOL FROM A SYSTEM", w=6.0, spc=200)]

    cw = (W - 3 * 0.24) / 4
    for i, (name, body) in enumerate(HARD):
        x = M + i * (cw + 0.24)
        s += [card(x, 2.56, cw, 1.95)]
        s += [text(x + 0.28, 2.86, cw - 0.56, 0.31, run(name, 2000, TEXT))]
        s += [hairline(3.34, x=x + 0.28, w=cw - 0.56)]
        s += [text(x + 0.28, 3.50, cw - 0.56, 0.90, run(body, 1100, MUTED),
                   anchor="t", autofit=False)]

    s += [hairline(4.75)]

    # the cost, stated as a conclusion rather than a scare statistic
    s += [card(M, 4.92, W, 1.30)]
    s += [text(1.10, 5.10, 3.0, 0.90,
               [run("61", T_STAT_XL, ACCENT), run("%", 2400, MUTED)])]
    s += [vrule(3.30, 5.14, 0.92, color=RULE)]
    s += [micro(3.62, 5.20, "OF ORGANIZATIONS SEE NO EBIT IMPACT FROM AI", w=6.0, spc=150)]
    s += [text(3.62, 5.48, 8.40, 0.30,
               [run("Pilots are tools, and tools don’t move EBIT. ", T_STAGE, TEXT, bold=True),
                run("Systems do.", T_STAGE, ACCENT, bold=True)])]
    s += [micro(3.62, 5.86,
                "SOURCE: MCKINSEY, THE STATE OF AI IN 2025. 39% ATTRIBUTE ANY EBIT IMPACT TO AI",
                w=8.40, color=DIM, spc=100)]

    s += [logo("rId2")]
    return s, ["image16.png"]


# --------------------------------------------------------------------------
# slide 3 — the chain, told as deliverables
# --------------------------------------------------------------------------
# One slide instead of two, and the columns are what the customer receives, not
# the stage that produced it. The eight stage names survive as mono captions.
CHAIN = [
    ("Scoped spec", "DISCOVER · ANALYZE", "requirements and fit"),
    ("Cited research", "RESEARCH", "sources you can check"),
    ("Compliance gate", "COMPLIANCE", "signed before any code"),
    ("Reviewed build", "AI MEMORY · BUILD", "applied and reviewed"),
    ("Running system", "RELEASE · OPERATE", "released and monitored"),
]


def slide3():
    s = [backdrop()]
    s += header("What you get.", " And where you can stop.", "The chain")
    s += [text(M, 1.40, 10.28, 0.50,
               run("AI agents run every stage, a person opens every gate. Five deliverables "
                   "on the way to a finished application, and no build budget moves without "
                   "a human yes.", T_LEAD, MUTED))]

    s += from_to("FROM  ·  FIRST CONVERSATION", "TO  ·  A FINISHED APPLICATION")

    # the rail: five deliverables, gates between them
    s += [hairline(RAIL_Y - 0.006)]
    for i, (cx, (name, stages, sub)) in enumerate(zip(NODE_X_5, CHAIN), start=1):
        s += rail_node(cx, f"{i:02d}")
        s += [text(cx - 1.11, 3.14, 2.22, 0.24, run(name, T_STAGE, TEXT), align="ctr")]
        s += [text(cx - 1.11, 3.44, 2.22, 0.18, run(sub, T_STAGE_SUB, MUTED), align="ctr")]
        s += [micro(cx - 1.11, 3.68, stages, w=2.22, color=DIM, align="ctr", spc=100)]
    for i in range(4):
        s += [diamond((NODE_X_5[i] + NODE_X_5[i + 1]) / 2, RAIL_Y)]

    # the gates, stated as the buyer's exit rather than as our process step
    s += [diamond(M + 0.05, 4.09)]
    s += [text(M + 0.22, 4.02, 6.4, 0.18,
               run("YOU CAN STOP AT ANY GATE, BEFORE BUILD BUDGET MOVES",
                   T_EYEBROW, ACCENT, font=MONO, spc=150))]

    s += ai_band(NODE_X_5[0] - 0.265, NODE_X_5[-1] + 0.265,
                 "AI AGENTS RUN EVERY STAGE")

    # the five deliverables merge into one finished application
    apex_x, apex_y = NODE_X_5[2], 5.14
    for cx in NODE_X_5:
        s += [line(cx, BAND_Y + BAND_H + 0.06, apex_x, apex_y, w=0.020, color=DIM)]
    s += [ellipse(apex_x - 0.12, apex_y - 0.12, 0.24, fill=BG, line=MUTED, lw=12700)]
    s += [rect(apex_x - 0.010, apex_y + 0.12, 0.020, 0.20, fill=DIM)]
    s += [triangle(apex_x, OUT_CARD_Y - 0.08, 0.20, 0.14, fill=MUTED, rot=10800000)]

    s += outcome_card(
        "OUTPUT  ·  WHAT THIS HAS ALREADY PRODUCED",
        "Audit-grade output, built and verified: signed audit trail, EU-only, "
        "158 tests green.")
    s += [logo("rId2")]
    return s, ["image16.png"]


# --------------------------------------------------------------------------
# slide 5 — the moat
# --------------------------------------------------------------------------
CYCLE = [("Build", "real production work"), ("Capture", "patterns + failures"),
         ("Reuse", "queried before code")]

DEFENSIBLE = [
    ("Earned, not bought.", "The library only grows by running real production builds."),
    ("It compounds.", "Every project makes the next estimate, gate and build safer."),
    ("Capital can’t copy it.", "A bigger round buys code, not failures already survived."),
]


def slide5():
    """The founders removed the "why it's defensible" panel, so the compounding
    loop and the library counts re-flow across the full width instead of leaving
    the right half of the slide empty next to an orphaned divider."""
    s = [backdrop()]
    s += header("Our moat.", " Every build makes the next one safer.", "The moat")
    s += [text(M, 1.40, W, 0.24,
               run("Anyone can generate code. What compounds is what real production "
                   "builds taught us.", T_LEAD, MUTED))]

    # the compounding loop, now the full width of the slide
    s += [eyebrow(M, 2.00, "THE COMPOUNDING LOOP", w=5.0, spc=300)]
    gap = 0.36
    cw = (W - 2 * gap) / 3
    for i, (name, sub) in enumerate(CYCLE):
        x = M + i * (cw + gap)
        s += [card(x, 2.30, cw, 1.00)]
        s += [text(x, 2.54, cw, 0.28, run(name, 2000, TEXT), align="ctr")]
        s += [text(x, 2.93, cw, 0.17, run(sub, T_MICRO, MUTED, font=MONO), align="ctr")]
        if i < 2:
            s += [triangle(x + cw + gap / 2, 2.80, 0.10, 0.12, fill=MUTED, rot=5400000)]

    # the return path: reuse feeds the next build
    first_c, last_c = M + cw / 2, M + 2 * (cw + gap) + cw / 2
    loop_bottom = 3.66
    s += [rect(last_c, 3.30, 0.012, loop_bottom - 3.30, fill=ACCENT)]
    s += [rect(first_c, loop_bottom, last_c - first_c, 0.012, fill=ACCENT)]
    s += [rect(first_c, 3.44, 0.012, loop_bottom - 3.44, fill=ACCENT)]
    s += [triangle(first_c + 0.006, 3.38, 0.12, 0.15)]
    s += [text(first_c, 3.78, last_c - first_c, 0.17,
               run("every build feeds the next", T_EYEBROW, MUTED, font=MONO, spc=100),
               align="ctr")]
    s += [text(M, 4.14, W, 0.22,
               run("Every project writes validated patterns and documented failures back "
                   "into the library. Every next build queries it first.", T_STAGE_SUB, MUTED))]

    # what the library holds
    s += [hairline(4.58)]
    s += [eyebrow(M, 4.76, "THE PATTERN LIBRARY", w=5.0, spc=300)]
    tw = (W - 0.36) / 2
    for i, (num, col, label) in enumerate([("Hundreds", TEXT, "validated patterns"),
                                           ("Thousands", ACCENT, "documented anti-patterns")]):
        x = M + i * (tw + 0.36)
        s += [card(x, 5.02, tw, 1.22)]
        s += [text(x + 0.30, 5.26, tw - 0.60, 0.58, run(num, T_STAT, col))]
        s += [text(x + 0.30, 5.88, tw - 0.60, 0.21, run(label, T_LEAD, TEXT))]

    s += [hairline(6.40)]
    s += [text(M, 6.56, W, 0.24,
               run("The chain fills the library. The library makes the next chain safer. "
                   "That loop is the moat.", T_LEAD, TEXT, bold=True))]
    s += [logo("rId2")]
    return s, ["image16.png"]


# --------------------------------------------------------------------------
# slide 6 — what we have built
# --------------------------------------------------------------------------
BUILDS = [
    dict(rid="rId3", name="CFO Suite", status="BUILT", status_col=MUTED,
         sector="SME financing · corporate finance",
         does="Reads a company’s financials and returns a bank-grade credit rating, "
              "default probability and pricing as a finished PDF.",
         proof_num="Bank scorecard", proof_col=TEXT,
         proof="Calibrated against a real one. Repositioning to pay-per-use."),
    dict(rid="rId4", name="Baru", status="LIVE", status_col=ACCENT,
         sector="B2B sales · outbound acquisition",
         does="Finds and qualifies B2B leads, drafts the outreach, and routes every "
              "send through a Slack approval.",
         proof_num="€90 / month", proof_col=ACCENT,
         proof="Paying customer since June 2026, 150 leads per month."),
    dict(rid="rId5", name="Board Member App", status="BUILT", status_col=MUTED,
         sector="Pharma / CDMO · board level",
         does="Turns a stack of board documents into a cited briefing: a watermarked "
              "PDF with a signed audit trail, EU-only.",
         proof_num="158 tests green", proof_col=TEXT,
         proof="Verified end to end. Offered, not yet deployed."),
]


def slide6():
    s = [backdrop()]
    s += header("What we’ve built.", " Three systems, three problems.", "Builds")
    s += [text(M, 1.44, 9.90, 0.26,
               run("Three systems taken end to end through the chain.", T_LEAD, MUTED))]
    s += [hairline(2.00)]

    cy, ch = 2.20, 3.94
    for i, b in enumerate(BUILDS):
        x = M + i * 3.96
        s += [card(x, cy, 3.61, ch)]
        ix = x + 0.28
        iw = 3.05
        s += [pic(ix, cy + 0.26, 0.24, 0.24, b["rid"])]
        # status chip, top right inside the card
        s += [rect(x + 3.61 - 0.28 - 0.92, cy + 0.22, 0.92, 0.30, fill=BG,
                   line=b["status_col"])]
        s += [micro(x + 3.61 - 0.28 - 0.92, cy + 0.305, b["status"], w=0.92,
                    color=b["status_col"], align="ctr", spc=100)]
        s += [text(ix, cy + 0.62, iw, 0.33, run(b["name"], 2000, TEXT))]
        s += [hairline(cy + 1.12, x=ix, w=iw)]
        s += [micro(ix, cy + 1.30, "SECTOR", w=iw)]
        s += [text(ix, cy + 1.50, iw, 0.20, run(b["sector"], 1050, TEXT))]
        s += [micro(ix, cy + 1.88, "WHAT IT DOES", w=iw)]
        s += [text(ix, cy + 2.08, iw, 0.56, run(b["does"], 1050, TEXT))]
        s += [hairline(cy + 2.84, x=ix, w=iw)]
        s += [micro(ix, cy + 3.02, "PROOF", w=iw)]
        s += [text(ix, cy + 3.22, iw, 0.24, run(b["proof_num"], 1400, b["proof_col"],
                                                bold=True))]
        s += [text(ix, cy + 3.52, iw, 0.38, run(b["proof"], 1050, MUTED))]

    s += [hairline(6.38)]
    s += [text(M, 6.56, W, 0.24,
               run("Three sectors, one chain. The same pipeline produced all three.",
                   T_LEAD, TEXT, bold=True))]
    s += [logo("rId2")]
    return s, ["image16.png", "image13.png", "image14.png", "image15.png"]


# --------------------------------------------------------------------------
# slide 7 — the closing question
# --------------------------------------------------------------------------
def slide7():
    s = [backdrop()]
    s += header("One question.", "", "One question")
    s += [text(M, 1.60, 9.72, 0.22,
               run("I’ll leave you with a question, not a brochure.", T_LEAD, MUTED))]
    s += [text(M, 2.28, 11.25, 1.30, [
        run("Which system would you rebuild today if delivery took ", 3300, TEXT),
        run("twelve weeks", 3300, ACCENT),
        run(" instead of two years?", 3300, TEXT),
    ], anchor="t", autofit=False)]

    s += [hairline(4.16)]
    s += [eyebrow(M, 4.34, "TWO WAYS THIS GOES", w=6.0, spc=300)]

    forks = [
        (M, "We build the application.", TEXT,
         "One system, taken end to end."),
        (6.91, "We deliver the platform.", ACCENT,
         "Multiple systems, that’s the platform conversation."),
    ]
    for x, head, col, body in forks:
        s += [card(x, 4.66, 5.65, 1.34)]
        s += [text(x + 0.34, 4.98, 4.97, 0.31, run(head, 2000, col, bold=True))]
        s += [text(x + 0.34, 5.44, 4.97, 0.22, run(body, 1100, MUTED))]

    s += [logo("rId2")]
    return s, ["image16.png"]


# --------------------------------------------------------------------------
def native_backdrop(part):
    """Swap the full-bleed backdrop bitmap on an untouched slide for a filled
    rectangle, so no slide in the deck depends on a background image. The bitmap
    contributes nothing but the flat ground and an all but invisible dot grid."""
    import re

    path = f"{UNPACKED}/ppt/slides/slide{part}.xml"
    xml = open(path, encoding="utf-8").read()
    m = re.search(r'<p:pic>(?:(?!</p:pic>).)*?name="Picture 1"(?:(?!</p:pic>).)*?</p:pic>',
                  xml, re.S)
    assert m, f"slide{part}.xml has no backdrop picture"
    rid = re.search(r'r:embed="(rId\d+)"', m.group(0)).group(1)

    ci._uid[0] = 900 + part * 10          # keep clear of the slide's own shape ids
    open(path, "w", encoding="utf-8").write(xml.replace(m.group(0), backdrop()))

    rels_path = f"{UNPACKED}/ppt/slides/_rels/slide{part}.xml.rels"
    rx = open(rels_path, encoding="utf-8").read()
    rel = re.search(r'<Relationship Id="%s"[^>]*?/>' % rid, rx)
    assert rel, f"no relationship {rid} on slide{part}"
    open(rels_path, "w", encoding="utf-8").write(rx.replace(rel.group(0), ""))


def prune_dangling_rels():
    """Drop image relationships that no shape on the slide embeds. The source deck
    carried four of these on the later slides, about 100 KB each, declared but
    unreachable."""
    import re

    for name in sorted(os.listdir(f"{UNPACKED}/ppt/slides")):
        if not name.endswith(".xml"):
            continue
        xml = open(f"{UNPACKED}/ppt/slides/{name}", encoding="utf-8").read()
        used = set(re.findall(r'r:(?:embed|link)="(rId\d+)"', xml))
        rels_path = f"{UNPACKED}/ppt/slides/_rels/{name}.rels"
        rx = open(rels_path, encoding="utf-8").read()
        out = rx
        for tag, rid in re.findall(
                r'(<Relationship Id="(rId\d+)"[^>]*?/relationships/image"[^>]*?/>)', rx):
            if rid not in used:
                out = out.replace(tag, "")
                print(f"dropped dangling image rel {rid} on {name}")
        if out != rx:
            open(rels_path, "w", encoding="utf-8").write(out)


def prune_media():
    """Delete media no longer referenced by any part. The three friction icons on
    the old problem slide went out with its chip row, and PowerPoint reports an
    orphaned part as a corrupt file."""
    media_dir = f"{UNPACKED}/ppt/media"
    referenced = set()
    for root, _, files in os.walk(UNPACKED):
        for name in files:
            if not name.endswith(".rels"):
                continue
            body = open(os.path.join(root, name), encoding="utf-8").read()
            for asset in os.listdir(media_dir):
                if asset in body:
                    referenced.add(asset)
    for asset in sorted(set(os.listdir(media_dir)) - referenced):
        os.remove(os.path.join(media_dir, asset))
        print("pruned unused media:", asset)


def drop_slide(part):
    """Take a slide out of the presentation order and delete everything that then
    hangs loose: the slide part, its rels, its content-type override and the
    relationship the presentation used to reach it."""
    import re

    pres = f"{UNPACKED}/ppt/presentation.xml"
    rels = f"{UNPACKED}/ppt/_rels/presentation.xml.rels"
    types = f"{UNPACKED}/[Content_Types].xml"

    rx = open(rels, encoding="utf-8").read()
    m = re.search(r'<Relationship Id="(rId\d+)"[^>]*?Target="slides/slide%d\.xml"[^>]*?/>' % part, rx)
    assert m, f"no relationship for slide{part}.xml"
    rid, rel_tag = m.group(1), m.group(0)

    px = open(pres, encoding="utf-8").read()
    sld = re.search(r'<p:sldId id="\d+" r:id="%s"/>' % rid, px)
    assert sld, f"slide{part}.xml is not in the presentation order"
    open(pres, "w", encoding="utf-8").write(px.replace(sld.group(0), ""))
    open(rels, "w", encoding="utf-8").write(rx.replace(rel_tag, ""))

    tx = open(types, encoding="utf-8").read()
    ov = re.search(r'<Override PartName="/ppt/slides/slide%d\.xml"[^>]*?/>' % part, tx)
    assert ov, f"no content-type override for slide{part}.xml"
    open(types, "w", encoding="utf-8").write(tx.replace(ov.group(0), ""))

    os.remove(f"{UNPACKED}/ppt/slides/slide{part}.xml")
    rp = f"{UNPACKED}/ppt/slides/_rels/slide{part}.xml.rels"
    if os.path.exists(rp):
        os.remove(rp)


# --------------------------------------------------------------------------
# Em dashes on the slides that are otherwise left alone. The en dashes in number
# ranges ($51–74B, Seed–Series E, 6–7 figure) are correct typography and stay.
EM_DASH_FIXES = {
    9: [("<a:t>1% of SAM — </a:t>", "<a:t>1% of SAM. </a:t>"),
        ("<a:t>open source as the adoption lever.</a:t>",
         "<a:t>Open source as the adoption lever.</a:t>")],
    10: [("whole row — and the loop", "whole row, and the loop")],
    11: [("<a:t> — highly experienced", "<a:t>, highly experienced")],
    12: [("vetting the company — all before", "vetting the company, all before")],
}


def main():
    if os.path.exists(UNPACKED):
        shutil.rmtree(UNPACKED)
    with zipfile.ZipFile(SRC) as z:
        z.extractall(UNPACKED)

    for n, fn in zip(SLIDE_PARTS, [slide1, slide2, slide3, slide5, slide6, slide7]):
        ci.reset_ids()
        shapes, images = fn()
        with open(f"{UNPACKED}/ppt/slides/slide{n}.xml", "w", encoding="utf-8") as f:
            f.write(slide_xml(shapes))
        with open(f"{UNPACKED}/ppt/slides/_rels/slide{n}.xml.rels", "w", encoding="utf-8") as f:
            f.write(rels_xml(images))

    drop_slide(DROPPED_PART)
    for part in ORIGINAL_PARTS:
        native_backdrop(part)
    prune_dangling_rels()
    prune_media()

    # Slides 8-12 keep their original layout; only the em dashes come out, so the
    # whole deck reads in one voice.
    for n, pairs in EM_DASH_FIXES.items():
        path = f"{UNPACKED}/ppt/slides/slide{n}.xml"
        with open(path, encoding="utf-8") as f:
            xml = f.read()
        for old, new in pairs:
            assert old in xml, (n, old)
            xml = xml.replace(old, new)
        with open(path, "w", encoding="utf-8") as f:
            f.write(xml)

    if os.path.exists(OUT):
        os.remove(OUT)
    zf = zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED)
    for root, _, files in os.walk(UNPACKED):
        for name in files:
            p = os.path.join(root, name)
            zf.write(p, os.path.relpath(p, UNPACKED))
    zf.close()
    print("wrote", OUT)


if __name__ == "__main__":
    main()
