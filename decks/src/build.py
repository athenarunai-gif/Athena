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
BAND_Y, BAND_H = 4.25, 0.34
OUT_CARD_Y, OUT_CARD_H = 5.72, 0.86


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


def patch_cover_art():
    """The cover sub-line is baked into the background artwork, em dash and all.
    Lift it out of the bitmap by copying a clean strip of the dotted backdrop
    over it (the dot grid has a 44 px period, so a 88 px offset lands exactly on
    the grid) and re-set the line as live Poppins text."""
    from PIL import Image
    src = f"{UNPACKED}/ppt/media/image1.png"
    im = Image.open(src).convert("RGB")
    clean = im.crop((0, 744, im.width, 788))
    im.paste(clean, (0, 656))
    im.save(src)


def slide1():
    """The hero headline stays in the brand artwork. The sub-line is repainted as
    live text so it can lose its em dash."""
    s = [background("rId2")]
    s += [text(0.77, 4.57, 9.5, 0.24,
               run("The bottleneck has moved from writing code to everything around it.",
                   T_STAGE, COVER_SUB_COLOR))]
    s += [text(M, 5.02, 9.0, 0.28,
               run("We build the chain, not the generator.", T_STAGE, ACCENT, bold=True))]
    return s, ["image1.png"]


# --------------------------------------------------------------------------
# slide 2 — the problem
# --------------------------------------------------------------------------
STEPS_MANUAL = ["Requirements", "Feasibility", "Compliance", "Approval", "Operations"]


def slide2():
    s = [background("rId2")]
    s += header("Still manual.", " And that is where the money goes.", "The problem")

    # band A — the five manual steps that sit around the code
    s += [eyebrow(M, 1.45, "FIVE STEPS AROUND THE CODE. NOT ONE OF THEM IS CODE",
                  w=9.0, spc=200)]
    s += [text(M, 1.74, 10.42, 0.21,
               run("Every one of them a handoff, a document, a wait.", T_LEAD, MUTED))]

    rail_y = 2.42
    s += [hairline(rail_y - 0.006)]
    for cx, (num, name) in zip(NODE_X_5, enumerate(STEPS_MANUAL, 1)):
        s += [ellipse(cx - NODE_D / 2, rail_y - NODE_D / 2, NODE_D),
              text(cx - 0.28, rail_y - 0.105, 0.56, 0.21,
                   run(f"{num:02d}", 1300, MUTED, font=MONO), align="ctr")]
        s += [text(cx - 1.11, 2.80, 2.22, 0.24, run(name, T_STAGE, TEXT), align="ctr")]
        s += [text(cx - 1.11, 3.08, 2.22, 0.15,
                   run("handoff · document · wait", T_MICRO, DIM, font=MONO),
                   align="ctr")]

    s += [hairline(3.46)]

    # band B left — what it costs
    s += [text(M, 4.02, 3.0, 0.90,
               [run("61", T_STAT_XL, ACCENT), run("%", 2400, MUTED)])]
    s += [text(2.42, 4.20, 4.50, 0.55,
               run("of organizations see no EBIT impact from AI", T_LEAD, MUTED))]

    # 100-dot waffle: the 61 / 39 split behind the headline number
    d, pitch = 0.105, 0.155
    for i in range(100):
        col, row = i % 20, i // 20
        s += [dot(M + 0.05 + col * pitch, 5.16 + row * pitch, d,
                  ACCENT if i < 61 else RULE)]
    s += [text(M, 5.92, 6.0, 0.15, [
        run("61 NO EBIT IMPACT", T_MICRO, ACCENT, font=MONO, spc=100),
        run("     39 ANY EBIT IMPACT", T_MICRO, DIM, font=MONO, spc=100),
    ])]

    # band B right — the so-what
    s += [card(7.10, 3.92, 5.46, 2.22)]
    s += [micro(7.44, 4.16, "WHERE THE MONEY GOES", w=4.78, spc=200)]
    s += [text(7.44, 4.46, 4.78, 0.72,
               run("The expensive failures happen before a line of code.",
                   2000, TEXT, bold=True))]
    s += [text(7.44, 5.30, 4.78, 0.24,
               run("That’s the part we automate.", T_SOWHAT, ACCENT, bold=True))]
    cx = 7.44
    for label, rid, cw in [("HANDOFF", "rId4", 1.45), ("DOCUMENT", "rId5", 1.55),
                           ("WAIT", "rId6", 1.15)]:
        s += [rect(cx, 5.70, cw, 0.32, fill=BG, line=RULE)]
        s += [pic(cx + 0.15, 5.79, 0.15, 0.15, rid)]
        s += [micro(cx + 0.38, 5.805, label, w=cw - 0.50, color=MUTED, spc=100)]
        cx += cw + 0.16

    # footer
    s += [hairline(6.30)]
    s += [text(M, 6.50, 9.0, 0.17,
               run("Source: McKinsey, The State of AI in 2025. 39% attribute any EBIT impact to AI",
                   T_META, DIM, font=MONO))]
    s += [logo("rId3")]
    return s, ["image2.png", "image16.png", "image10.png", "image11.png", "image12.png"]


# --------------------------------------------------------------------------
# slide 3 — the chain, stages 01-05
# --------------------------------------------------------------------------
CHAIN_A = [("Discover", "from conversation"), ("Analyze", "scope + fit"),
           ("Research", "cited, deep"), ("Compliance", "pre-build gate"),
           ("AI Memory", "patterns carried in")]


def slide3():
    s = [background("rId2")]
    s += header("From idea to build-ready package.", "", "The chain")
    s += [text(M, 1.36, 10.28, 0.53, [
        run("One line, a human gate at every step. AI agents support every stage, ",
            T_LEAD, MUTED),
        run("Discover through AI Memory", T_LEAD, MUTED, bold=True),
        run(". From first conversation to a build-ready package.", T_LEAD, MUTED),
    ])]

    s += from_to("FROM  ·  FIRST CONVERSATION", "TO  ·  BUILD-READY PACKAGE")

    # the rail
    s += [hairline(RAIL_Y - 0.006)]
    for cx, (num, (name, sub)) in zip(NODE_X_5, enumerate(CHAIN_A, 1)):
        s += rail_node(cx, f"{num:02d}")
        s += rail_stage(cx, name, sub)
    for i in range(4):
        s += [diamond((NODE_X_5[i] + NODE_X_5[i + 1]) / 2, RAIL_Y)]

    s += gate_legend()
    s += ai_band(NODE_X_5[0] - 0.265, NODE_X_5[-1] + 0.265)

    # the five stages merge into one artifact — drawn at DIM weight with a real
    # merge node, so the diagram reads at presentation distance
    apex_x, apex_y = NODE_X_5[2], 5.32
    for cx in NODE_X_5:
        s += [line(cx, BAND_Y + BAND_H + 0.06, apex_x, apex_y, w=0.020, color=DIM)]
    s += [ellipse(apex_x - 0.12, apex_y - 0.12, 0.24, fill=BG, line=MUTED, lw=12700)]
    s += [rect(apex_x - 0.010, apex_y + 0.12, 0.020, 0.32, fill=DIM)]
    s += [triangle(apex_x, OUT_CARD_Y - 0.08, 0.20, 0.14, fill=MUTED, rot=10800000)]

    s += outcome_card(
        "OUTPUT  ·  ONE APPROVED ARTIFACT",
        "Requirements, scope, cited research, compliance and prior patterns. Approved before code.")
    s += [logo("rId3")]
    return s, ["image3.png", "image16.png"]


# --------------------------------------------------------------------------
# slide 4 — the chain, stages 06-08 and the LEARN loop
# --------------------------------------------------------------------------
CHAIN_B = [("Build", "code + review"), ("Release", "human approval"),
           ("Operate", "monitoring")]


def slide4():
    s = [background("rId2")]
    s += header("From package to running software.", "", "The chain")
    s += [text(M, 1.36, 10.28, 0.53, [
        run("The package is approved. ", T_LEAD, MUTED),
        run("Build through Operate", T_LEAD, MUTED, bold=True),
        run(" takes it from approved package to software running in production. "
            "Every decision that matters stays with a person.", T_LEAD, MUTED),
    ])]

    s += from_to("FROM  ·  BUILD-READY PACKAGE", "TO  ·  SOFTWARE IN PRODUCTION")

    # carried-over stub for stage 05
    s += [rect(1.04, RAIL_Y - 0.006, 2.08, 0.012, fill=RULE)]
    for x in (0.99, 1.51, 2.03, 2.56, 3.08):
        s += [shape("ellipse", x, RAIL_Y - 0.05, 0.10, 0.10, BG, DIM, 12700)]
    s += [micro(M, RAIL_Y + 0.22, "05 · BUILD-READY PACKAGE", w=2.64, color=DIM,
                align="ctr", spc=100)]

    # the rail
    s += [rect(3.61, RAIL_Y - 0.006, RIGHT - 3.61, 0.012, fill=RULE)]
    s += [diamond(3.66, RAIL_Y)]
    for cx, (num, (name, sub)) in zip(NODE_X_3, enumerate(CHAIN_B, 6)):
        s += rail_node(cx, f"{num:02d}")
        s += rail_stage(cx, name, sub)
    for i in range(2):
        s += [diamond((NODE_X_3[i] + NODE_X_3[i + 1]) / 2, RAIL_Y)]

    s += gate_legend()
    s += ai_band(NODE_X_3[0] - 0.265, NODE_X_3[-1] + 0.265)

    # the LEARN loop — the return path that feeds stage 05 on the previous slide
    loop_y, loop_x = 5.20, 2.08
    right_x = NODE_X_3[-1] + 0.265
    s += [rect(right_x, BAND_Y + BAND_H, 0.012, loop_y - (BAND_Y + BAND_H), fill=ACCENT)]
    s += [rect(loop_x, loop_y, right_x - loop_x, 0.012, fill=ACCENT)]
    s += [rect(loop_x, RAIL_Y + 0.62, 0.012, loop_y - (RAIL_Y + 0.62), fill=ACCENT)]
    s += [triangle(loop_x + 0.006, RAIL_Y + 0.55, 0.12, 0.15)]
    # label sits on the return path and interrupts it, so the loop reads as a
    # routed connection rather than a closed box
    s += [rect(3.86, loop_y - 0.16, 5.60, 0.34, fill=BG)]
    s += [text(3.86, loop_y - 0.07, 5.60, 0.18, [
        run("LEARN", T_EYEBROW, ACCENT, font=MONO, spc=200),
        run("  ·  every build teaches the next", T_EYEBROW, MUTED, font=MONO, spc=100),
    ], align="ctr")]

    s += outcome_card(
        "OUTPUT  ·  SOFTWARE RUNNING IN PRODUCTION",
        "Eight stages, one line, a person on every gate, and a library that grows with every build.")
    s += [logo("rId3")]
    return s, ["image2.png", "image16.png"]


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
    s = [background("rId2")]
    s += header("Our moat.", " Every build makes the next one safer.", "The moat")
    s += [text(M, 1.40, 6.90, 0.50,
               run("Anyone can generate code. What compounds is what real production "
                   "builds taught us.", T_LEAD, MUTED))]

    # left — the compounding loop, drawn as a closed cycle
    s += [eyebrow(M, 2.16, "THE COMPOUNDING LOOP", w=5.0, spc=300)]
    cw, gap = 2.06, 0.30
    for i, (name, sub) in enumerate(CYCLE):
        x = M + i * (cw + gap)
        s += [card(x, 2.46, cw, 0.92)]
        s += [text(x, 2.66, cw, 0.28, run(name, 2000, TEXT), align="ctr")]
        s += [text(x, 3.01, cw, 0.17, run(sub, T_MICRO, MUTED, font=MONO), align="ctr")]
        if i < 2:
            s += [triangle(x + cw + gap / 2, 2.92, 0.10, 0.12, fill=MUTED, rot=5400000)]

    # the return path: reuse feeds the next build
    loop_bottom = 3.72
    s += [rect(M + 2 * (cw + gap) + cw / 2, 3.38, 0.012, loop_bottom - 3.38, fill=ACCENT)]
    s += [rect(M + cw / 2, loop_bottom, 2 * (cw + gap), 0.012, fill=ACCENT)]
    s += [rect(M + cw / 2, 3.52, 0.012, loop_bottom - 3.52, fill=ACCENT)]
    s += [triangle(M + cw / 2 + 0.006, 3.46, 0.12, 0.15)]
    s += [text(M + cw / 2, 3.82, 2 * (cw + gap), 0.17,
               run("every build feeds the next", T_EYEBROW, MUTED, font=MONO, spc=100),
               align="ctr")]
    s += [text(M, 4.14, 6.82, 0.42,
               run("Every project writes validated patterns and documented failures back "
                   "into the library, and every next build queries it before a line of "
                   "code is written.", T_STAGE_SUB, MUTED))]

    # left — what the library holds
    s += [hairline(4.72, x=M, w=6.82)]
    s += [eyebrow(M, 4.90, "THE PATTERN LIBRARY", w=5.0, spc=300)]
    for x, w, num, col, label in [(M, 3.30, "Hundreds", TEXT, "validated patterns"),
                                  (4.20, 3.38, "Thousands", ACCENT, "documented anti-patterns")]:
        s += [text(x, 5.18, w, 0.58, run(num, T_STAT, col))]
        s += [text(x, 5.84, w, 0.21, run(label, T_LEAD, TEXT))]

    # right — why it is defensible
    s += [vrule(7.58, 2.16, 4.00)]
    s += [card(7.92, 2.16, 4.64, 4.00)]
    s += [micro(8.24, 2.46, "WHY IT’S DEFENSIBLE", w=4.03, spc=200)]
    for i, (head, body) in enumerate(DEFENSIBLE):
        y = 2.90 + i * 1.10
        s += [text(8.24, y, 4.00, 0.20, run(head, 1300, ACCENT, bold=True))]
        s += [text(8.24, y + 0.30, 4.00, 0.44, run(body, 1100, MUTED))]

    s += [hairline(6.36)]
    s += [text(M, 6.54, W, 0.24,
               run("The chain fills the library. The library makes the next chain safer. "
                   "That loop is the moat.", T_LEAD, TEXT, bold=True))]
    s += [logo("rId3")]
    return s, ["image4.png", "image16.png"]


# --------------------------------------------------------------------------
# slide 6 — what we have built
# --------------------------------------------------------------------------
BUILDS = [
    dict(rid="rId4", name="CFO Suite", status="BUILT", status_col=MUTED,
         sector="SME financing · corporate finance",
         does="Reads a company’s financials and returns a bank-grade credit rating, "
              "default probability and pricing as a finished PDF.",
         proof_num="Bank scorecard", proof_col=TEXT,
         proof="Calibrated against a real one. Repositioning to pay-per-use."),
    dict(rid="rId5", name="Baru", status="LIVE", status_col=ACCENT,
         sector="B2B sales · outbound acquisition",
         does="Finds and qualifies B2B leads, drafts the outreach, and routes every "
              "send through a Slack approval.",
         proof_num="€90 / month", proof_col=ACCENT,
         proof="Paying customer since June 2026, 150 leads per month."),
    dict(rid="rId6", name="Board Member App", status="BUILT", status_col=MUTED,
         sector="Pharma / CDMO · board level",
         does="Turns a stack of board documents into a cited briefing: a watermarked "
              "PDF with a signed audit trail, EU-only.",
         proof_num="158 tests green", proof_col=TEXT,
         proof="Verified end to end. Offered, not yet deployed."),
]


def slide6():
    s = [background("rId2")]
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
    s += [logo("rId3")]
    return s, ["image2.png", "image16.png", "image13.png", "image14.png", "image15.png"]


# --------------------------------------------------------------------------
# slide 7 — the closing question
# --------------------------------------------------------------------------
def slide7():
    s = [background("rId2")]
    s += header("One question.", "", "One question")
    s += [text(M, 1.60, 9.72, 0.22,
               run("I’ll leave you with a question, not a brochure.", T_LEAD, MUTED))]
    s += [text(M, 2.28, 11.25, 1.30, [
        run("Which process at your company still runs in ", 3300, TEXT),
        run("Excel", 3300, ACCENT),
        run(", and shouldn’t have for the past year?", 3300, TEXT),
    ], anchor="t", autofit=False)]

    s += [hairline(4.16)]
    s += [eyebrow(M, 4.34, "TWO WAYS THIS GOES", w=6.0, spc=300)]

    forks = [
        (M, "We build the application.", TEXT,
         "One process, taken end to end through the chain."),
        (6.91, "We deliver the platform.", ACCENT,
         "Multiple processes, that’s the platform conversation."),
    ]
    for x, head, col, body in forks:
        s += [card(x, 4.66, 5.65, 1.34)]
        s += [text(x + 0.34, 4.98, 4.97, 0.31, run(head, 2000, col, bold=True))]
        s += [text(x + 0.34, 5.44, 4.97, 0.22, run(body, 1100, MUTED))]

    s += [logo("rId3")]
    return s, ["image2.png", "image16.png"]


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

    patch_cover_art()

    for n, fn in enumerate([slide1, slide2, slide3, slide4, slide5, slide6, slide7], 1):
        ci.reset_ids()
        shapes, images = fn()
        with open(f"{UNPACKED}/ppt/slides/slide{n}.xml", "w", encoding="utf-8") as f:
            f.write(slide_xml(shapes))
        with open(f"{UNPACKED}/ppt/slides/_rels/slide{n}.xml.rels", "w", encoding="utf-8") as f:
            f.write(rels_xml(images))

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
