"""Corporate-identity primitives extracted from Pitch_Deck_AthenaRun_v3.pptx.

Every colour, typeface, size and geometric convention in here was read out of the
existing deck — nothing is invented. The slide builders import from this module so
the rebuilt slides stay pixel-consistent with the untouched ones (8-12).
"""

EMU = 914400

# --- palette (verbatim from the original slide XML) -------------------------
BG = "0E0E11"      # slide background
TEXT = "ECECEE"    # primary type
MUTED = "9A9AA2"   # secondary type / node strokes
DIM = "5A5A60"     # tertiary type / stub strokes
ACCENT = "FF6B3D"  # brand orange
RULE = "2B2B2D"    # hairlines and card borders
CARD = "161619"    # card / band fill
CARD2 = "1F1F22"   # vertical divider fill

# --- typefaces --------------------------------------------------------------
SANS = "Poppins"
MONO = "Courier New"

# --- type scale (hundredths of a point, as OOXML wants) ---------------------
T_TITLE = 2700      # slide title, bold + regular two-tone
T_LEAD = 1400       # lead paragraph under the title
T_STAGE = 1700      # chain stage name / card heading
T_STAGE_SUB = 1200  # chain stage descriptor
T_EYEBROW = 1100    # Courier section label
T_META = 1000       # Courier meta / source line
T_MICRO = 900       # Courier micro label inside cards
T_STAT = 3800       # stat number
T_STAT_XL = 5400    # hero stat number
T_SOWHAT = 1600     # closing statement

# --- grid -------------------------------------------------------------------
M = 0.76            # left margin
RIGHT = 12.56       # right content edge
W = RIGHT - M       # 11.80
TITLE_Y = 0.62
RULE_Y = 1.19
LOGO = (0.69, 7.04, 1.18, 0.28)

# chain rail node centres, taken from the original slides 3 and 4
NODE_X_5 = [1.935, 4.295, 6.655, 9.015, 11.375]
NODE_X_3 = [5.095, 8.085, 11.075]
NODE_D = 0.53       # node circle diameter
GATE_D = 0.10       # gate diamond size


def emu(v):
    return int(round(v * EMU))


_uid = [100]


def _nid():
    _uid[0] += 1
    return _uid[0]


def reset_ids():
    _uid[0] = 100


def _fill(color):
    return f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>' if color else "<a:noFill/>"


def _line(color, w):
    if not color:
        return "<a:ln><a:noFill/></a:ln>"
    return f'<a:ln w="{int(w)}">{_fill(color)}</a:ln>'


def shape(prst, x, y, w, h, fill=None, line=None, lw=9525, rot=None, name=None):
    """A prstGeom autoshape, styled the way the original deck styles its shapes."""
    i = _nid()
    name = name or f"{prst} {i}"
    r = f' rot="{rot}"' if rot else ""
    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="{name}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm{r}><a:off x="{emu(x)}" y="{emu(y)}"/>'
        f'<a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>'
        f'<a:prstGeom prst="{prst}"><a:avLst/></a:prstGeom>'
        f"{_fill(fill)}{_line(line, lw)}<a:effectLst/></p:spPr>"
        f'<p:txBody><a:bodyPr rtlCol="0" anchor="ctr"/><a:lstStyle/><a:p><a:pPr algn="ctr"/></a:p></p:txBody></p:sp>'
    )


def rect(x, y, w, h, fill=None, line=None, lw=9525):
    return shape("rect", x, y, w, h, fill, line, lw)


def hairline(y, x=M, w=W, color=RULE):
    """The deck's signature 1px divider: a 0.012in rect, never a line shape."""
    return rect(x, y, w, 0.012, fill=color)


def vrule(x, y, h, color=CARD2):
    return rect(x, y, 0.012, h, fill=color)


def line(x1, y1, x2, y2, w=0.012, color=RULE):
    """A hairline between two arbitrary points, drawn as a rotated rect so it
    keeps the deck's rectangle-based hairline look."""
    import math
    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy)
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    rot = int(round(math.degrees(math.atan2(dy, dx)) * 60000)) % 21600000
    return shape("rect", cx - length / 2, cy - w / 2, length, w,
                 fill=color, line=None, rot=rot)


def ellipse(x, y, d, fill=BG, line=MUTED, lw=15875):
    return shape("ellipse", x, y, d, d, fill, line, lw)


def dot(cx, cy, d, fill):
    return shape("ellipse", cx - d / 2, cy - d / 2, d, d, fill, None)


def diamond(cx, cy, d=GATE_D, fill=ACCENT):
    return shape("diamond", cx - d / 2, cy - d / 2, d, d, fill, None)


def triangle(cx, cy, w, h, fill=ACCENT, rot=None):
    return shape("triangle", cx - w / 2, cy - h / 2, w, h, fill, None, rot=rot)


def run(text, sz, color=TEXT, bold=False, font=SANS, spc=None):
    return (text, sz, color, bold, font, spc)


def _esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _runs_xml(runs):
    out = []
    for text, sz, color, bold, font, spc in runs:
        sp = f' spc="{spc}"' if spc else ""
        out.append(
            f'<a:r><a:rPr sz="{sz}" b="{1 if bold else 0}"{sp}>'
            f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
            f'<a:latin typeface="{font}"/></a:rPr><a:t>{_esc(text)}</a:t></a:r>'
        )
    return "".join(out)


def text(x, y, w, h, runs, align="l", anchor="ctr", autofit=True, line_spc=None):
    """Text box using the original deck's body properties (zero insets, autofit)."""
    i = _nid()
    if isinstance(runs, tuple):
        runs = [runs]
    fit = "<a:spAutoFit/>" if autofit else ""
    ls = f'<a:lnSpc><a:spcPct val="{line_spc}"/></a:lnSpc>' if line_spc else ""
    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="TextBox {i}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
        f'<p:txBody><a:bodyPr wrap="square" lIns="0" rIns="0" tIns="0" bIns="0" anchor="{anchor}">{fit}</a:bodyPr>'
        f'<a:lstStyle/><a:p><a:pPr algn="{align}">{ls}</a:pPr>{_runs_xml(runs)}</a:p></p:txBody></p:sp>'
    )


def pic(x, y, w, h, rid, name=None):
    i = _nid()
    name = name or f"Picture {i}"
    return (
        f'<p:pic><p:nvPicPr><p:cNvPr id="{i}" name="{name}"/><p:cNvPicPr/><p:nvPr/></p:nvPicPr>'
        f'<p:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>'
        f'<p:spPr><a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>'
    )


# --- composite CI components ------------------------------------------------

def background(rid="rId2"):
    return pic(0, 0, 13.333, 7.5, rid, name="Picture 1")


def backdrop():
    """The dark ground as a real shape instead of a full-bleed bitmap.

    The original artwork's backdrop is a flat 0E0E11 plus a 44px dot grid in
    151518 — seven levels of luminance on 0.19% of the pixels. A filled rectangle
    reproduces everything except that texture, and keeps the slide free of images.
    """
    return rect(0, 0, 13.3333, 7.5, fill=BG)


# The cover artwork also carried two frame rules, lighter and thinner than the
# section rules used on the content slides. Positions measured off the bitmap.
COVER_RULE_COLOR = "1F1F22"
COVER_RULE_Y = (1.000, 6.431)


def logo(rid="rId3"):
    return pic(*LOGO, rid, name="Logo")


def header(title_bold, title_rest, tag):
    """Title / right-hand section tag / rule — the deck's fixed slide header."""
    runs = [run(title_bold, T_TITLE, TEXT, True)]
    if title_rest:
        runs.append(run(title_rest, T_TITLE, MUTED, False))
    return (
        text(M, TITLE_Y, 10.83, 0.43, runs)
        + text(9.09, 0.68, 3.47, 0.17, run(tag, T_EYEBROW, MUTED, font=MONO, spc=120), align="r")
        + hairline(RULE_Y)
    )


def eyebrow(x, y, label, w=6.0, color=MUTED, spc=300, align="l"):
    return text(x, y, w, 0.18, run(label, T_EYEBROW, color, font=MONO, spc=spc), align=align)


def micro(x, y, label, w=3.0, color=MUTED, align="l", spc=100):
    return text(x, y, w, 0.15, run(label, T_MICRO, color, font=MONO, spc=spc), align=align)


def card(x, y, w, h, fill=CARD, line=RULE):
    return rect(x, y, w, h, fill=fill, line=line)


SLIDE_HEAD = (
    "<?xml version='1.0' encoding='UTF-8' standalone='yes'?>\n"
    '<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
    ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
    ' xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
    ' xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"'
    ' xmlns:a14="http://schemas.microsoft.com/office/drawing/2010/main"'
    ' showMasterSp="1" showMasterPhAnim="1"><p:cSld><p:spTree>'
    '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
    '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
    '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
)

SLIDE_TAIL = (
    "</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>"
    '<p:transition xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main"'
    ' spd="med" advClick="1"/></p:sld>'
)


def slide_xml(shapes):
    return SLIDE_HEAD + "".join(shapes) + SLIDE_TAIL


RELS_HEAD = (
    "<?xml version='1.0' encoding='UTF-8' standalone='yes'?>\n"
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout"'
    ' Target="../slideLayouts/slideLayout7.xml"/>'
)


def rels_xml(images):
    """images: list of media file names, mapped to rId2, rId3, ..."""
    parts = [RELS_HEAD]
    for n, img in enumerate(images, start=2):
        parts.append(
            f'<Relationship Id="rId{n}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"'
            f' Target="../media/{img}"/>'
        )
    parts.append("</Relationships>")
    return "".join(parts)
