#!/usr/bin/env python3
"""Split the "Application Engineering Platform" slide into a two-slide spread.

Slide 4 carries stages 01-03 (intent to a signed concept, everything before
code), slide 5 carries 04-06 (build to running software). Both are rebuilt on
the deck's grid so the rail, the agent bracket and the closing band line up
across the pair.
"""
from lib import (E, run, para, textbox, rect, pic, nid, background, logo,
                 title, eyebrow, hrule, kicker, lead,
                 CARD, RULE, TEXT, MUTED, FAINT, ACCENT, BG, POP, MONO,
                 COL_X, COL_W, _id)

# ------------------------------------------------------------------ rail bits

def ellipse(x, y, d, fill=BG, line=MUTED, line_w=15875):
    return (
        '<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="Shape {i}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
        '<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{d}" cy="{d}"/></a:xfrm>'
        '<a:prstGeom prst="ellipse"><a:avLst/></a:prstGeom>'
        '<a:solidFill><a:srgbClr val="{f}"/></a:solidFill>'
        '<a:ln cap="flat" cmpd="sng" w="{lw}"><a:solidFill><a:srgbClr val="{c}"/></a:solidFill>'
        '<a:prstDash val="solid"/><a:round/><a:headEnd len="sm" w="sm" type="none"/>'
        '<a:tailEnd len="sm" w="sm" type="none"/></a:ln></p:spPr>'
        '<p:txBody><a:bodyPr anchorCtr="0" anchor="ctr" bIns="45700" lIns="91425" '
        'spcFirstLastPara="1" rIns="91425" wrap="square" tIns="45700"><a:noAutofit/></a:bodyPr>'
        '<a:lstStyle/><a:p><a:pPr indent="0" lvl="0" marL="0" marR="0" rtl="0" algn="ctr">'
        '<a:lnSpc><a:spcPct val="100000"/></a:lnSpc><a:spcBef><a:spcPts val="0"/></a:spcBef>'
        '<a:spcAft><a:spcPts val="0"/></a:spcAft><a:buNone/></a:pPr><a:r><a:t></a:t></a:r>'
        '<a:endParaRPr/></a:p></p:txBody></p:sp>'
    ).format(i=nid(), x=E(x), y=E(y), d=E(d), f=fill, c=line, lw=line_w)


def diamond(x, y, d, fill=ACCENT):
    return (
        '<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="Shape {i}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
        '<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{d}" cy="{d}"/></a:xfrm>'
        '<a:prstGeom prst="diamond"><a:avLst/></a:prstGeom>'
        '<a:solidFill><a:srgbClr val="{f}"/></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr>'
        '<p:txBody><a:bodyPr anchorCtr="0" anchor="ctr" bIns="45700" lIns="91425" '
        'spcFirstLastPara="1" rIns="91425" wrap="square" tIns="45700"><a:noAutofit/></a:bodyPr>'
        '<a:lstStyle/><a:p><a:pPr indent="0" lvl="0" marL="0" marR="0" rtl="0" algn="ctr">'
        '<a:lnSpc><a:spcPct val="100000"/></a:lnSpc><a:spcBef><a:spcPts val="0"/></a:spcBef>'
        '<a:spcAft><a:spcPts val="0"/></a:spcAft><a:buNone/></a:pPr><a:r><a:t></a:t></a:r>'
        '<a:endParaRPr/></a:p></p:txBody></p:sp>'
    ).format(i=nid(), x=E(x), y=E(y), d=E(d), f=fill)


def centered(text, x, y, w, size, color, font=POP):
    return textbox(x, y, w, size / 72.0 * 1.42, [
        para([run(text, size, color, font)], size, color, font, algn="ctr")])


# ---------------------------------------------------------------- the spread

RAIL_Y = 2.98
DIA = 0.53
STEP_TOP = 3.34

# geometry shared by both slides so the two halves line up exactly
CENTERS = [COL_X + COL_W / 6.0 + i * (COL_W / 3.0) for i in range(3)]
AGENT_Y, AGENT_H = 4.50, 0.42
BAND_Y, BAND_H = 5.30, 1.14


def stage_row(steps):
    """Three numbered nodes on one rail, evenly spread across the column."""
    s = []
    # rail runs node to node - no track dangling into empty space
    s.append(rect(CENTERS[0], RAIL_Y, CENTERS[-1] - CENTERS[0], 0.01214, fill=RULE))
    for i in range(len(CENTERS) - 1):
        mid = (CENTERS[i] + CENTERS[i + 1]) / 2.0
        s.append(diamond(mid - 0.05, RAIL_Y - 0.045, 0.10))

    for cx, (num, head, sub, tag) in zip(CENTERS, steps):
        s.append(ellipse(cx - DIA / 2, RAIL_Y - DIA / 2, DIA))
        s.append(textbox(cx - 0.28, RAIL_Y - 0.11, 0.56, 0.22,
                         [para([run(num, 13, MUTED, MONO)], 13, MUTED, MONO, algn="ctr")]))
        w = COL_W / 3.0 - 0.30
        s.append(centered(head, cx - w / 2, STEP_TOP, w, 17, TEXT))
        s.append(centered(sub, cx - w / 2, STEP_TOP + 0.38, w, 11, MUTED))
        s.append(centered(tag, cx - w / 2, STEP_TOP + 0.68, w, 9, FAINT, MONO))
    return s


def agent_bracket():
    """The 'agents run every stage' bracket, as a plain strip instead of the
    tangle of converging lines the original drew."""
    s = [rect(COL_X, AGENT_Y, COL_W, AGENT_H, fill=CARD, line=RULE)]
    s.append(textbox(COL_X, AGENT_Y, COL_W, AGENT_H,
                     [para([run("AI AGENTS RUN EVERY STAGE", 9, MUTED, MONO)],
                           9, MUTED, MONO, algn="ctr")], anchor="ctr", autofit=False))
    return s


def band(label, label_color, line_runs):
    s = [rect(COL_X, BAND_Y, COL_W, BAND_H, fill=CARD, line=RULE)]
    s.append(textbox(COL_X + 0.32, BAND_Y + 0.26, COL_W - 0.64, 0.155,
                     [para([run(label, 9, label_color, MONO)], 9, label_color, MONO)]))
    s.append(textbox(COL_X + 0.32, BAND_Y + 0.56, COL_W - 0.64, 0.28,
                     [para(line_runs, 15)]))
    return s


def frame(eyebrow_text, from_label, to_label):
    """Everything the two halves share, top of slide down to the rail labels."""
    s = [background("rId3")]
    s.append(title("Application Engineering Platform"))
    s.append(eyebrow(eyebrow_text))
    s.append(hrule(1.19))
    s.append(lead([run("Business practices x Software Engineering. "
                       "Run by AI powered Workflows.", 14, MUTED, POP)],
                  COL_X, 1.40, 11.20, 0.30))
    s.append(kicker(from_label, COL_X, 2.20, 5.60))
    s.append(textbox(COL_X + COL_W - 5.60, 2.20, 5.60, 0.185,
                     [para([run(to_label, 11, MUTED, MONO)], 11, MUTED, MONO, algn="r")]))
    return s


def slide4():
    s = frame("PLATFORM PROCESS · 1/2", "FROM  ·  INTENT", "TO  ·  A SIGNED CONCEPT")
    s += stage_row([
        ("01", "Scope & Business Fit", "requirements and outcome", "DISCOVER · ANALYZE"),
        ("02", "Research & Concept", "sources you can check", "RESEARCH · DESIGN"),
        ("03", "Compliance", "signed before any code", "COMPLIANCE · SIGN-OFF"),
    ])
    s += agent_bracket()
    s += band("GATE  ·  YOU DECIDE", ACCENT, [
        run("You can stop at any gate — ", 15, TEXT, POP, bold=True),
        run("before build budget moves.", 15, ACCENT, POP, bold=True)])
    s.append(logo("rId4"))
    return "".join(s)


def slide5():
    s = frame("PLATFORM PROCESS · 2/2", "FROM  ·  A SIGNED CONCEPT",
              "TO  ·  AN OPERATING SOFTWARE")
    s += stage_row([
        ("04", "Build & Verify", "applied and reviewed", "AI MEMORY · BUILD"),
        ("05", "Secure & Release", "secured and released", "SECURE · RELEASE"),
        ("06", "Operate & Evolve", "monitored and improved", "OPERATE · EVOLVE"),
    ])
    s += agent_bracket()
    s += band("OUTPUT  ·  WHAT THIS PRODUCES", MUTED, [
        run("Audit-grade output, built and verified: ", 15, TEXT, POP, bold=True),
        run("signed audit trail, human in the loop.", 15, MUTED, POP, bold=True)])
    s.append(logo("rId4"))
    return "".join(s)


def replace_tree(path, body):
    x = open(path, encoding="utf-8").read()
    head, sep, _ = x.partition("</p:nvGrpSpPr>")
    grp = ('<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
           '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>')
    open(path, "w", encoding="utf-8").write(
        head + sep + grp + body + "</p:spTree></p:cSld>"
        '<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>')


if __name__ == "__main__":
    import sys
    base = sys.argv[1] if len(sys.argv) > 1 else "unpacked/ppt/slides/"
    a = sys.argv[2] if len(sys.argv) > 2 else "slide1.xml"
    b = sys.argv[3] if len(sys.argv) > 3 else "slide2.xml"
    _id[0] = 3000
    replace_tree(base + a, slide4())
    _id[0] = 4000
    replace_tree(base + b, slide5())
    print("built %s (stages 01-03) and %s (stages 04-06)" % (a, b))
