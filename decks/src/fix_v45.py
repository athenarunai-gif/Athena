"""Patch slides in Pitch_Deck_AthenaRun_v4.5.

Slide 3 — the taxonomy in the boxes
  * "Monitoring & observability?" appeared verbatim in two cards.
  * "Production & Lifecycle" was a catch-all holding speed, QA, operations and
    long-term ownership, which is why it carried nine items against the others'
    five. The imbalance was a taxonomy symptom, not a layout one.
  * "Data quality?" and the over/under-engineering question sat under Business
    Fit, which asks whether the software matches the process.
  * Cards are named for the obligation rather than the domain, and each carries
    the question it answers instead of an ordinal — four parallel categories
    numbered 01 to 04 imply an order that does not exist.
  * Body type from 9.5pt, the smallest running text in the deck, to 11pt.
  * Em dash out of the lead, double space out of the title. The uppercase section
    tag stays: the new front section runs THE STARTING POINT, THE COST, PLATFORM
    PROCESS throughout, so uppercase is its convention.
  Dropped: "Time to concept (TTC)?" and "Time to ship?" — speed is already the
  subject of the escalation line, and TTC is not an established abbreviation.

Slide 8 — the reference slide
  The Baru card carried the Board Agent's sector, description and proof, ending
  in "Offered, not yet deployed" underneath a LIVE chip. Baru's own content —
  the one system with a paying customer — was not on the slide at all. Two
  light-mode product screenshots sat on top of the cards and hid it.
  The screenshots are out, every card now describes its own system in three
  parallel bullets, and each closes on a single hard proof. The closing line
  carries the delivery time, which is the strongest claim available here and the
  one that sets up the twelve-weeks question at the end of the deck.
"""
import os
import re
import shutil
import sys
import zipfile

from ci import *  # noqa: F401,F403
import ci

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUT = os.path.join(HERE, os.pardir, "Pitch_Deck_AthenaRun_v4.5.pptx")
WORK = os.path.join(HERE, "v45_unpacked")

CANVAS_W = 13.3194                    # this deck's canvas is fractionally narrower


# --------------------------------------------------------------------------
# shared
# --------------------------------------------------------------------------
def bullets(x, y, w, h, items, sz=1100):
    """Bulleted list in this deck's own paragraph convention: an en dash in the
    brand orange, 122% line spacing, 3.2pt after each item."""
    i = ci._nid()
    paras = []
    for item in items:
        paras.append(
            '<a:p><a:pPr indent="-141732" lvl="0" marL="141732" marR="0" rtl="0" algn="l">'
            '<a:lnSpc><a:spcPct val="122000"/></a:lnSpc>'
            '<a:spcBef><a:spcPts val="0"/></a:spcBef>'
            '<a:spcAft><a:spcPts val="320"/></a:spcAft>'
            f'<a:buClr><a:srgbClr val="{ACCENT}"/></a:buClr>'
            f'<a:buSzPts val="{sz}"/><a:buFont typeface="Arial"/><a:buChar char="&#8211;"/>'
            '</a:pPr>'
            f'<a:r><a:rPr b="0" i="0" lang="en-US" sz="{sz}" u="none" cap="none" strike="noStrike">'
            f'<a:solidFill><a:srgbClr val="{MUTED}"/></a:solidFill>'
            '<a:latin typeface="Poppins"/><a:ea typeface="Poppins"/>'
            '<a:cs typeface="Poppins"/><a:sym typeface="Poppins"/></a:rPr>'
            f'<a:t>{ci._esc(item)}</a:t></a:r><a:endParaRPr/></a:p>'
        )
    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="TextBox {i}"/>'
        f'<p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/>'
        f'<a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/>'
        '<a:ln><a:noFill/></a:ln></p:spPr>'
        '<p:txBody><a:bodyPr anchorCtr="0" anchor="t" bIns="0" lIns="0" spcFirstLastPara="1"'
        ' rIns="0" wrap="square" tIns="0"><a:noAutofit/></a:bodyPr><a:lstStyle/>'
        + "".join(paras) + '</p:txBody></p:sp>'
    )


def resolve_part(position):
    """Map a presentation position to its slide part. Part numbering is not
    presentation order here: position 3 lives in slide2.xml, and editing by
    filename would rewrite the wrong slide."""
    rels = dict(re.findall(r'Id="(rId\d+)"[^>]*?Target="(slides/slide\d+\.xml)"',
                           open(f"{WORK}/ppt/_rels/presentation.xml.rels",
                                encoding="utf-8").read()))
    order = re.findall(r'<p:sldId id="\d+" r:id="(rId\d+)"/>',
                       open(f"{WORK}/ppt/presentation.xml", encoding="utf-8").read())
    return rels[order[position - 1]].split("/")[-1]


def picture_rids(xml):
    """Sort the slide's pictures by width: backdrop, logo, card icons. Anything
    else is a pasted screenshot and is not carried over."""
    bg = logo = None
    icons = []
    for m in re.finditer(r'<p:pic>.*?r:embed="(rId\d+)".*?<a:ext cx="(\d+)" cy="\d+"',
                         xml, re.S):
        rid, cx = m.group(1), int(m.group(2)) / 914400
        if cx > 10:
            bg = rid
        elif 1.0 < cx < 2.0:
            logo = rid
        elif cx < 0.5:
            icons.append(rid)
    assert bg and logo, f"could not identify backdrop/logo (bg={bg}, logo={logo})"
    return bg, logo, icons


def splice(position, builder, marker):
    part = resolve_part(position)
    path = f"{WORK}/ppt/slides/{part}"
    xml = open(path, encoding="utf-8").read()
    assert marker in xml, f"{part} is not the expected slide (looking for {marker!r})"

    bg, logo, icons = picture_rids(xml)
    head = xml[:xml.index("</p:grpSpPr>") + len("</p:grpSpPr>")]
    tail = xml[xml.index("</p:spTree>"):]
    ci.reset_ids()
    open(path, "w", encoding="utf-8").write(
        head + "".join(builder(bg, logo, icons)) + tail)
    print(f"rebuilt position {position} = {part}")


# --------------------------------------------------------------------------
# slide 3 — what proper engineering still has to answer
# --------------------------------------------------------------------------
S3_CARD_X = [0.76, 3.78, 6.80, 9.82]
S3_CARD_W, S3_CARD_Y, S3_CARD_H = 2.74, 2.58, 3.36
PAD = 0.22

S3_CARDS = [
    ("Fit", "SOLVES THE REAL PROCESS?", [
        "Scope and workflow fit?",
        "A business process, not a tool?",
        "Effective for the people using it?",
        "Over- or under-engineered?"]),
    ("Integration", "LIVES IN YOUR ESTATE?", [
        "Fits the system landscape?",
        "Dependencies and API reliability?",
        "Data models, migration, quality?",
        "Real-time operations?"]),
    ("Assurance", "SOMEONE CAN SIGN IT?", [
        "Compliance and auditability?",
        "Sign-on, access, permissions?",
        "Testing and QA coverage?",
        "Security and vulnerabilities?"]),
    ("Operation", "SURVIVES YEAR TWO?", [
        "Deployment, monitoring, recovery?",
        "Performance and reliability?",
        "Ownership and technical debt?",
        "Where knowledge lives when someone leaves?"]),
]

ESCALATION = [
    ("Easy start", MUTED), (" → ", DIM),
    ("underestimated engineering", MUTED), (" → ", DIM),
    ("hidden work", MUTED), (" → ", DIM),
    ("rework", MUTED), (" → ", DIM),
    ("lost speed & higher cost", TEXT), (" → ", DIM),
    ("lost EBIT", ACCENT),
]


def slide3(bg_rid, logo_rid, _icons):
    s = [pic(0, 0, CANVAS_W, 7.5, bg_rid, name="Picture 1")]
    s += [text(M, 0.62, 10.83, 0.45, [
        run("Complex Software.", T_TITLE, TEXT, bold=True),
        run(" Is it possible with AI tools?", T_TITLE, MUTED)])]
    s += [text(9.09, 0.68, 3.47, 0.24,
               run("THE PROBLEM", T_EYEBROW, MUTED, font=MONO, spc=120), align="r")]
    s += [hairline(1.19)]
    s += [text(M, 1.40, 11.20, 0.62,
               run("Entry barriers to start coding or building tools with an AI IDE, tool "
                   "or chat are low. That leads companies to underestimate the complexity "
                   "of proper software engineering, and to a false sense of simplicity.",
                   T_LEAD, MUTED))]
    s += [eyebrow(M, 2.30, "WHAT PROPER ENGINEERING STILL HAS TO ANSWER", w=7.0, spc=200)]

    for x, (title, question, items) in zip(S3_CARD_X, S3_CARDS):
        ix, iw = x + PAD, S3_CARD_W - 2 * PAD
        s += [card(x, S3_CARD_Y, S3_CARD_W, S3_CARD_H)]
        s += [text(ix, S3_CARD_Y + 0.24, iw, 0.28, run(title, 1500, TEXT, bold=True))]
        s += [micro(ix, S3_CARD_Y + 0.60, question, w=iw, color=DIM, spc=100)]
        s += [hairline(S3_CARD_Y + 1.04, x=ix, w=iw)]
        s += [bullets(ix, S3_CARD_Y + 1.22, iw, S3_CARD_H - 1.44, items)]

    s += [hairline(6.36)]
    s += [text(M, 6.54, 11.80, 0.20, [run(t, 1200, c, bold=True) for t, c in ESCALATION])]
    s += [pic(0.69, 7.04, 1.18, 0.28, logo_rid, name="Logo")]
    return s


# --------------------------------------------------------------------------
# slide 8 — the reference slide
# --------------------------------------------------------------------------
# Three identical cards made the deck's proof slide read like a table. It now
# leads with the one system that has a customer-side number, and the other two
# sit compact beside it. The product screenshots stay out: one shows an empty
# window with a sidebar, the other a "extracting financial data" spinner, so
# neither shows a result at any size.
HERO = dict(
    name="Baru", icon=2, sector="B2B sales · outbound acquisition",
    does=["Finds and qualifies B2B leads",
          "Drafts the outreach",
          "Every send through a Slack approval"],
    result_label="RESULT  ·  PAYING CUSTOMER SINCE JUNE 2026",
    stat="150", stat_unit=" leads a month",
)

COMPACT = [
    dict(name="CFO Suite", icon=0, sector="SME financing · corporate finance",
         does=["Financials in, bank-grade rating out",
               "Default probability and pricing"],
         proof="CALIBRATED AGAINST A REAL BANK SCORECARD"),
    dict(name="Board Agent", icon=1, sector="Pharma / CDMO · board level",
         does=["Board documents into a cited briefing",
               "Watermarked PDF, signed audit trail"],
         proof="158 TESTS GREEN  ·  EU-ONLY, VERIFIED"),
]

HERO_X, HERO_W = 0.76, 6.60
SIDE_X, SIDE_W = 7.62, 4.94
ROW_Y, ROW_H = 2.20, 3.94
SIDE_H = 1.90
S8_PAD = 0.28


def live_chip(x, w, y):
    cx = x + w - S8_PAD - 0.92
    return [rect(cx, y, 0.92, 0.30, fill=BG, line=ACCENT),
            micro(cx, y + 0.085, "LIVE", w=0.92, color=ACCENT, align="ctr", spc=100)]


def slide8(bg_rid, logo_rid, icons):
    s = [pic(0, 0, CANVAS_W, 7.5, bg_rid, name="Picture 1")]
    s += [text(M, 0.62, 10.83, 0.45, [
        run("What we’ve built.", T_TITLE, TEXT, bold=True),
        run(" Three systems, three problems.", T_TITLE, MUTED)])]
    s += [text(9.09, 0.68, 3.47, 0.24,
               run("BUILDS", T_EYEBROW, MUTED, font=MONO, spc=120), align="r")]
    s += [hairline(1.19)]
    s += [text(M, 1.44, 9.90, 0.24,
               run("Three systems taken end to end through the chain. All three in use.",
                   T_LEAD, MUTED))]
    s += [hairline(2.00)]

    # hero — the system with a customer-side number
    ix, iw = HERO_X + S8_PAD, HERO_W - 2 * S8_PAD
    s += [card(HERO_X, ROW_Y, HERO_W, ROW_H)]
    if len(icons) > HERO["icon"]:
        s += [pic(ix, ROW_Y + 0.24, 0.24, 0.24, icons[HERO["icon"]])]
    s += live_chip(HERO_X, HERO_W, ROW_Y + 0.20)
    s += [text(ix, ROW_Y + 0.56, iw, 0.40, run(HERO["name"], 2400, TEXT))]
    s += [hairline(ROW_Y + 1.12, x=ix, w=iw)]
    s += [micro(ix, ROW_Y + 1.28, "SECTOR", w=iw)]
    s += [text(ix, ROW_Y + 1.46, iw, 0.20, run(HERO["sector"], 1050, TEXT))]
    s += [micro(ix, ROW_Y + 1.78, "WHAT IT DOES", w=iw)]
    s += [bullets(ix, ROW_Y + 1.96, iw, 0.70, HERO["does"], sz=1050)]
    s += [hairline(ROW_Y + 2.76, x=ix, w=iw)]
    s += [micro(ix, ROW_Y + 2.92, HERO["result_label"], w=iw, spc=150)]
    s += [text(ix, ROW_Y + 3.10, iw, 0.62, [
        run(HERO["stat"], T_STAT, ACCENT),
        run(HERO["stat_unit"], T_STAGE, MUTED)])]

    # the other two, compact
    for i, b in enumerate(COMPACT):
        y = ROW_Y + i * (SIDE_H + 0.14)
        jx, jw = SIDE_X + S8_PAD, SIDE_W - 2 * S8_PAD
        s += [card(SIDE_X, y, SIDE_W, SIDE_H)]
        if len(icons) > b["icon"]:
            s += [pic(jx, y + 0.22, 0.20, 0.20, icons[b["icon"]])]
        s += live_chip(SIDE_X, SIDE_W, y + 0.18)
        s += [text(jx, y + 0.42, jw, 0.31, run(b["name"], 2000, TEXT))]
        s += [text(jx, y + 0.76, jw, 0.20, run(b["sector"], 1050, MUTED))]
        s += [bullets(jx, y + 0.98, jw, 0.42, b["does"], sz=1050)]
        # the proof reads as a stamp, not as a third bullet
        s += [hairline(y + 1.48, x=jx, w=jw)]
        s += [micro(jx, y + 1.60, b["proof"], w=jw, color=MUTED, spc=100)]

    s += [hairline(6.38)]
    s += [text(M, 6.56, 11.80, 0.24, [
        run("Three sectors, one chain. Every one of them live in ", T_LEAD, TEXT, bold=True),
        run("days or weeks", T_LEAD, ACCENT, bold=True),
        run(".", T_LEAD, TEXT, bold=True)])]
    s += [pic(0.69, 7.04, 1.18, 0.28, logo_rid, name="Logo")]
    return s


# --------------------------------------------------------------------------
def main():
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUT

    if os.path.exists(WORK):
        shutil.rmtree(WORK)
    with zipfile.ZipFile(src) as z:
        z.extractall(WORK)

    splice(3, slide3, "Complex Software.")
    splice(8, slide8, "What we’ve built.")

    if os.path.exists(out):
        os.remove(out)
    zf = zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED)
    for root, _, files in os.walk(WORK):
        for name in files:
            p = os.path.join(root, name)
            zf.write(p, os.path.relpath(p, WORK))
    zf.close()
    shutil.rmtree(WORK)
    print("wrote", out)


if __name__ == "__main__":
    main()
