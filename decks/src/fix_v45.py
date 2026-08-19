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
  parallel bullets, and each closes on a single hard proof.
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
S8_CARD_X = [0.76, 4.72, 8.68]
S8_CARD_W, S8_CARD_Y, S8_CARD_H = 3.61, 2.20, 3.94
S8_PAD = 0.28

BUILDS = [
    dict(name="CFO Suite", sector="SME financing · corporate finance",
         does=["Reads a company’s financials",
               "Bank-grade rating and default probability",
               "Priced, delivered as a finished PDF"],
         proof="Bank scorecard", proof_col=TEXT,
         note="Calibrated against a real one."),
    dict(name="Board Agent", sector="Pharma / CDMO · board level",
         does=["Board documents into a cited briefing",
               "Watermarked PDF, signed audit trail",
               "EU-only, local models, no training"],
         proof="158 tests green", proof_col=TEXT,
         note="Verified end to end."),
    dict(name="Baru", sector="B2B sales · outbound acquisition",
         does=["Finds and qualifies B2B leads",
               "Drafts the outreach",
               "Every send through a Slack approval"],
         proof="Paying customer", proof_col=ACCENT,
         note="Live since June 2026."),
]


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

    for i, (x, b) in enumerate(zip(S8_CARD_X, BUILDS)):
        ix, iw = x + S8_PAD, S8_CARD_W - 2 * S8_PAD
        s += [card(x, S8_CARD_Y, S8_CARD_W, S8_CARD_H)]
        if i < len(icons):
            s += [pic(ix, S8_CARD_Y + 0.24, 0.24, 0.24, icons[i])]
        chip_x = x + S8_CARD_W - S8_PAD - 0.92
        s += [rect(chip_x, S8_CARD_Y + 0.20, 0.92, 0.30, fill=BG, line=ACCENT)]
        s += [micro(chip_x, S8_CARD_Y + 0.285, "LIVE", w=0.92, color=ACCENT,
                    align="ctr", spc=100)]
        s += [text(ix, S8_CARD_Y + 0.56, iw, 0.34, run(b["name"], 2000, TEXT))]
        s += [hairline(S8_CARD_Y + 1.04, x=ix, w=iw)]
        s += [micro(ix, S8_CARD_Y + 1.20, "SECTOR", w=iw)]
        s += [text(ix, S8_CARD_Y + 1.38, iw, 0.20, run(b["sector"], 1050, TEXT))]
        s += [micro(ix, S8_CARD_Y + 1.70, "WHAT IT DOES", w=iw)]
        s += [bullets(ix, S8_CARD_Y + 1.88, iw, 0.90, b["does"], sz=1050)]
        s += [hairline(S8_CARD_Y + 2.86, x=ix, w=iw)]
        s += [micro(ix, S8_CARD_Y + 3.02, "PROOF", w=iw)]
        s += [text(ix, S8_CARD_Y + 3.20, iw, 0.24,
                   run(b["proof"], T_LEAD, b["proof_col"], bold=True))]
        s += [text(ix, S8_CARD_Y + 3.50, iw, 0.20, run(b["note"], 1050, MUTED))]

    s += [hairline(6.38)]
    s += [text(M, 6.56, 11.80, 0.24,
               run("Three sectors, one chain. The same pipeline produced all three.",
                   T_LEAD, TEXT, bold=True))]
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
