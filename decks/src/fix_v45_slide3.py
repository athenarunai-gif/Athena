"""Rebuild slide 3 of Pitch_Deck_AthenaRun_v4.5.

The slide was structurally sound and on-brand; the problems were in the taxonomy
and in a handful of consistency slips. What changes:

  * "Monitoring & observability?" appeared verbatim in two cards. Gone once.
  * "Production & Lifecycle" was a catch-all holding speed, QA, operations and
    long-term ownership, which is why it carried nine items against the others'
    five. Split: QA moves to Assurance, the rest becomes Operation.
  * "Data quality?" and "over- or under-engineering?" sat under Business Fit,
    which is about whether the software matches the process. Data quality moves
    to Integration; the engineering judgement stays but is reworded.
  * Cards are named for the obligation, not the domain, and each carries the
    question it answers instead of an ordinal. The four are parallel categories,
    so numbering them implied an order that does not exist.
  * Body type goes from 9.5pt, the smallest running text anywhere in the deck,
    to 11pt.
  * Em dash out of the lead, double space out of the title. The uppercase section
    tag stays: the new front section of this deck runs THE STARTING POINT, THE
    COST, PLATFORM PROCESS throughout, so uppercase is its convention, not a slip.
    It is the inherited back half that is sentence case.

Items dropped and why: "Time to concept (TTC)?" and "Time to ship?" — speed is
already the subject of the escalation line at the foot of the slide, and TTC is
not an established abbreviation.
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
SLIDE_POSITION = 3                    # the slide as the audience counts it

CARD_X = [0.76, 3.78, 6.80, 9.82]
CARD_W, CARD_Y, CARD_H = 2.74, 2.58, 3.36
PAD = 0.22

CARDS = [
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


def bullets(x, y, w, h, items, sz=1100):
    """Bulleted list using this deck's own paragraph conventions: an en dash in
    the brand orange, 122% line spacing, 3.2pt after each item."""
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
    pres = open(f"{WORK}/ppt/presentation.xml", encoding="utf-8").read()
    rels = dict(re.findall(r'Id="(rId\d+)"[^>]*?Target="(slides/slide\d+\.xml)"',
                           open(f"{WORK}/ppt/_rels/presentation.xml.rels",
                                encoding="utf-8").read()))
    order = re.findall(r'<p:sldId id="\d+" r:id="(rId\d+)"/>', pres)
    return rels[order[position - 1]].split("/")[-1]


def picture_rids(xml):
    """Pick the backdrop and the logo out of the slide's existing pictures by
    their size, so the rewritten slide keeps the relationships it already has."""
    bg = logo = None
    for m in re.finditer(r'<p:pic>.*?r:embed="(rId\d+)".*?<a:ext cx="(\d+)" cy="\d+"',
                         xml, re.S):
        rid, cx = m.group(1), int(m.group(2)) / 914400
        if cx > 10:
            bg = rid
        elif cx < 2:
            logo = rid
    assert bg and logo, f"could not identify backdrop/logo (bg={bg}, logo={logo})"
    return bg, logo


def build_slide3(bg_rid, logo_rid):
    ci.reset_ids()
    s = [pic(0, 0, CANVAS_W, 7.5, bg_rid, name="Picture 1")]

    s += [text(M, 0.62, 10.83, 0.45, [
        run("Complex Software.", T_TITLE, TEXT, bold=True),
        run(" Is it possible with AI tools?", T_TITLE, MUTED),
    ])]
    s += [text(9.09, 0.68, 3.47, 0.24,
               run("THE PROBLEM", T_EYEBROW, MUTED, font=MONO, spc=120), align="r")]
    s += [hairline(1.19)]

    s += [text(M, 1.40, 11.20, 0.62,
               run("Entry barriers to start coding or building tools with an AI IDE, tool "
                   "or chat are low. That leads companies to underestimate the complexity "
                   "of proper software engineering, and to a false sense of simplicity.",
                   T_LEAD, MUTED))]

    s += [eyebrow(M, 2.30, "WHAT PROPER ENGINEERING STILL HAS TO ANSWER", w=7.0, spc=200)]

    for x, (title, question, items) in zip(CARD_X, CARDS):
        ix, iw = x + PAD, CARD_W - 2 * PAD
        s += [card(x, CARD_Y, CARD_W, CARD_H)]
        s += [text(ix, CARD_Y + 0.24, iw, 0.28, run(title, 1500, TEXT, bold=True))]
        s += [micro(ix, CARD_Y + 0.60, question, w=iw, color=DIM, spc=100)]
        s += [hairline(CARD_Y + 1.04, x=ix, w=iw)]
        s += [bullets(ix, CARD_Y + 1.22, iw, CARD_H - 1.44, items)]

    s += [hairline(6.36)]
    s += [text(M, 6.54, 11.80, 0.20,
               [run(t, 1200, c, bold=True) for t, c in ESCALATION])]
    s += [pic(0.69, 7.04, 1.18, 0.28, logo_rid, name="Logo")]
    return s


def main():
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUT

    if os.path.exists(WORK):
        shutil.rmtree(WORK)
    with zipfile.ZipFile(src) as z:
        z.extractall(WORK)

    part = resolve_part(SLIDE_POSITION)
    path = f"{WORK}/ppt/slides/{part}"
    xml = open(path, encoding="utf-8").read()
    assert "Complex Software." in xml, f"{part} is not the Complex Software slide"

    bg_rid, logo_rid = picture_rids(xml)
    head = xml[:xml.index("</p:grpSpPr>") + len("</p:grpSpPr>")]
    tail = xml[xml.index("</p:spTree>"):]
    open(path, "w", encoding="utf-8").write(
        head + "".join(build_slide3(bg_rid, logo_rid)) + tail)
    print(f"rebuilt position {SLIDE_POSITION} = {part} (bg={bg_rid}, logo={logo_rid})")

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
