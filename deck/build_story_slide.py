#!/usr/bin/env python3
"""Build the story slide that goes between slide 1 and the old slide 2.

Six stations on one rail. The emphasis carries the arc rather than decorating
it: station 1 is in full text colour (the system was fine), stations 2-5 fade
to muted (the erosion), station 6 flares to accent (the reckoning).
"""
import sys
sys.path.insert(0, ".")

from lib import (E, run, para, textbox, rect, nid, background, logo,
                 title, eyebrow, hrule, kicker, lead,
                 CARD, RULE, TEXT, MUTED, FAINT, ACCENT, BG, POP, MONO,
                 COL_X, COL_W, _id)


def diamond(x, y, d, fill):
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


# marker, statement, colour of the statement
STATIONS = [
    ("2015",           "Das Reporting läuft. Und es läuft gut.", TEXT),
    ("DANN",           "Neue gesetzliche Anforderung.",           MUTED),
    ("DER HERSTELLER", "Nächstes Release: frühestens 2027.",      MUTED),
    ("2023",           "Der Kollege geht. Mit ihm die Logik.",    MUTED),
    ("SEITDEM",        "Es läuft daneben, in Excel.",             MUTED),
    ("DER PRÜFER",     "Wer hat was wann freigegeben?",           ACCENT),
]

RAIL_Y = 3.16
MARK_Y = 2.72
TEXT_Y = 3.40
BAND_Y, BAND_H = 5.10, 1.20


def story_slide():
    s = [background("rId3")]

    s.append(title("Das System ist nicht schlecht.", " Es ist von 2015."))
    s.append(eyebrow("DIE AUSGANGSLAGE"))
    s.append(hrule(1.19))
    s.append(lead([run("Der Prozess ist gewachsen. Das Werkzeug nicht.", 14, MUTED, POP)],
                  COL_X, 1.40, 11.20, 0.30))

    s.append(kicker("EIN KONZERN  ·  ZWÖLF GESELLSCHAFTEN  ·  EIN REPORTING", COL_X, 2.14, 8.0))

    # the rail, and one station per sixth of the column
    s.append(rect(COL_X, RAIL_Y, COL_W, 0.01214, fill=RULE))
    col = COL_W / 6.0
    for i, (mark, stmt, colour) in enumerate(STATIONS):
        cx = COL_X + col / 2.0 + i * col
        last = (i == len(STATIONS) - 1)
        w = col - 0.16

        s.append(textbox(cx - w / 2, MARK_Y, w, 0.155,
                         [para([run(mark, 9, ACCENT if last else FAINT, MONO)],
                               9, MUTED, MONO, algn="ctr")]))
        s.append(diamond(cx - 0.05, RAIL_Y - 0.045, 0.10, ACCENT if last else FAINT))

        s.append(textbox(cx - w / 2, TEXT_Y, w, 0.80,
                         [para([run(stmt, 13, colour, POP)], 13, colour, POP,
                               algn="ctr", line_pct=132)], anchor="t", autofit=False))

    # the line the whole slide exists for
    s.append(rect(COL_X, BAND_Y, COL_W, BAND_H, fill=CARD, line=RULE))
    s.append(textbox(COL_X + 0.40, BAND_Y, COL_W - 0.80, BAND_H,
                     [para([run("Ihre Systeme haben Daten.  ", 20, TEXT, POP, bold=True),
                            run("Ihr Prozess hat kein Gedächtnis.", 20, ACCENT, POP, bold=True)],
                           20)], anchor="ctr", autofit=False))

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
    target = sys.argv[1]
    _id[0] = 5000
    replace_tree(target, story_slide())
    print("story slide written to", target)
