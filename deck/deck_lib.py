#!/usr/bin/env python3
"""Rebuild slides 2 and 3 of the AthenaRun pitch deck in the deck's own design system.

Design tokens lifted from slides 4-7 of the source deck:
  bg 0E0E11 | card 161619 | border/rule 2B2B2D | text ECECEE | muted 9A9AA2 | accent FF6B3D
  Poppins for prose, Courier New for mono labels.
Grid: content column x=0.76" w=11.80", title 0.62", rule 1.19", logo 6437376 EMU.
"""
import re

EMU = 914400


def E(inches):
    return int(round(inches * EMU))


BG = "0E0E11"
CARD = "161619"
RULE = "2B2B2D"
TEXT = "ECECEE"
MUTED = "9A9AA2"
FAINT = "5A5A60"
ACCENT = "FF6B3D"

POP = "Poppins"
MONO = "Courier New"

COL_X = 0.76
COL_W = 11.80

_id = [1000]


def nid():
    _id[0] += 1
    return _id[0]


def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _font(f):
    return ('<a:latin typeface="{f}"/><a:ea typeface="{f}"/>'
            '<a:cs typeface="{f}"/><a:sym typeface="{f}"/>').format(f=f)


def run(text, size, color=TEXT, font=POP, bold=False):
    """One <a:r>. size in points."""
    return (
        '<a:r><a:rPr b="{b}" i="0" lang="en-US" sz="{sz}" u="none" cap="none" strike="noStrike">'
        '<a:solidFill><a:srgbClr val="{c}"/></a:solidFill>{f}</a:rPr>'
        '<a:t>{t}</a:t></a:r>'
    ).format(b=1 if bold else 0, sz=int(size * 100), c=color, f=_font(font), t=esc(text))


def para(runs, size, color=TEXT, font=POP, algn="l", space_after=0,
         line_pct=100, bullet=None):
    """One <a:p> holding pre-built runs."""
    if bullet:
        bu = ('<a:buClr><a:srgbClr val="{bc}"/></a:buClr><a:buSzPts val="{bs}"/>'
              '<a:buFont typeface="Arial"/><a:buChar char="{ch}"/>').format(
            bc=bullet["color"], bs=int(bullet["size"] * 100), ch=bullet["char"])
        marL, indent = E(0.155), E(-0.155)
    else:
        bu = ('<a:buClr><a:srgbClr val="{c}"/></a:buClr><a:buSzPts val="{s}"/>'
              '<a:buFont typeface="{f}"/><a:buNone/>').format(
            c=color, s=int(size * 100), f=font)
        marL, indent = 0, 0
    return (
        '<a:p><a:pPr indent="{ind}" lvl="0" marL="{marl}" marR="0" rtl="0" algn="{a}">'
        '<a:lnSpc><a:spcPct val="{lp}"/></a:lnSpc>'
        '<a:spcBef><a:spcPts val="0"/></a:spcBef>'
        '<a:spcAft><a:spcPts val="{sa}"/></a:spcAft>{bu}</a:pPr>'
        '{r}<a:endParaRPr/></a:p>'
    ).format(ind=indent, marl=marL, a=algn, lp=int(line_pct * 1000),
             sa=int(space_after * 100), bu=bu, r="".join(runs))


def textbox(x, y, w, h, paras, anchor="ctr", autofit=True):
    """A borderless text box positioned in inches."""
    fit = "<a:spAutoFit/>" if autofit else "<a:noAutofit/>"
    return (
        '<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="Shape {i}"/>'
        '<p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
        '<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>'
        '<p:txBody><a:bodyPr anchorCtr="0" anchor="{an}" bIns="0" lIns="0" '
        'spcFirstLastPara="1" rIns="0" wrap="square" tIns="0">{fit}</a:bodyPr>'
        '<a:lstStyle/>{p}</p:txBody></p:sp>'
    ).format(i=nid(), x=E(x), y=E(y), w=E(w), h=E(h), an=anchor, fit=fit, p="".join(paras))


def rect(x, y, w, h, fill=None, line=None, line_w=9525):
    """A filled / stroked rectangle with an empty text body (deck idiom)."""
    f = ('<a:solidFill><a:srgbClr val="%s"/></a:solidFill>' % fill) if fill else '<a:noFill/>'
    if line:
        ln = ('<a:ln cap="flat" cmpd="sng" w="{w}"><a:solidFill><a:srgbClr val="{c}"/></a:solidFill>'
              '<a:prstDash val="solid"/><a:round/><a:headEnd len="sm" w="sm" type="none"/>'
              '<a:tailEnd len="sm" w="sm" type="none"/></a:ln>').format(w=line_w, c=line)
    else:
        ln = '<a:ln><a:noFill/></a:ln>'
    return (
        '<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="Shape {i}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
        '<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cw}" cy="{ch}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>{f}{ln}</p:spPr>'
        '<p:txBody><a:bodyPr anchorCtr="0" anchor="ctr" bIns="45700" lIns="91425" '
        'spcFirstLastPara="1" rIns="91425" wrap="square" tIns="45700"><a:noAutofit/></a:bodyPr>'
        '<a:lstStyle/><a:p><a:pPr indent="0" lvl="0" marL="0" marR="0" rtl="0" algn="ctr">'
        '<a:lnSpc><a:spcPct val="100000"/></a:lnSpc><a:spcBef><a:spcPts val="0"/></a:spcBef>'
        '<a:spcAft><a:spcPts val="0"/></a:spcAft><a:buClr><a:srgbClr val="000000"/></a:buClr>'
        '<a:buSzPts val="1800"/><a:buFont typeface="Calibri"/><a:buNone/></a:pPr>'
        '<a:r><a:t></a:t></a:r><a:endParaRPr b="0" i="0" sz="1800" u="none" cap="none" '
        'strike="noStrike"><a:solidFill><a:srgbClr val="000000"/></a:solidFill>'
        '<a:latin typeface="Calibri"/><a:ea typeface="Calibri"/><a:cs typeface="Calibri"/>'
        '<a:sym typeface="Calibri"/></a:endParaRPr></a:p></p:txBody></p:sp>'
    ).format(i=nid(), x=E(x), y=E(y), cw=E(w), ch=E(h), f=f, ln=ln)


def pic(rid, x, y, w, h):
    return (
        '<p:pic><p:nvPicPr><p:cNvPr id="{i}" name="Shape {i}"/>'
        '<p:cNvPicPr preferRelativeResize="0"/><p:nvPr/></p:nvPicPr>'
        '<p:blipFill rotWithShape="1"><a:blip r:embed="{r}"><a:alphaModFix/></a:blip>'
        '<a:srcRect b="0" l="0" r="0" t="0"/><a:stretch/></p:blipFill>'
        '<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln>'
        '</p:spPr></p:pic>'
    ).format(i=nid(), r=rid, x=x, y=y, w=w, h=h)


# ---------------------------------------------------------------- primitives

def background(rid):
    return pic(rid, 0, 0, 12191693, 6858000)


def logo(rid):
    return pic(rid, 630936, 6437376, 1078992, 256032)


def title(lead, tail=""):
    runs = [run(lead, 27, TEXT, POP, bold=True)]
    if tail:
        runs.append(run(tail, 27, MUTED, POP, bold=False))
    return textbox(COL_X, 0.62, 10.83, 0.4544, [para(runs, 27)])


def eyebrow(text):
    return textbox(9.0894, 0.6797, 3.4694, 0.2355,
                   [para([run(text, 11, MUTED, MONO)], 11, MUTED, MONO, algn="r")])


def hrule(y, x=COL_X, w=COL_W):
    return rect(x, y, w, 0.01214, fill=RULE)


def kicker(text, x, y, w=6.0):
    """Small mono section label."""
    return textbox(x, y, w, 0.185, [para([run(text, 11, MUTED, MONO)], 11, MUTED, MONO)])


def lead(text_runs, x, y, w, h):
    return textbox(x, y, w, h, [para(text_runs, 14, MUTED, POP, line_pct=140)],
                   anchor="t", autofit=False)


