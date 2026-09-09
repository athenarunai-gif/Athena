"""AthenaRun deck v4 — 13 slides (8 main + 5 appendix).

v4 answers the second design review:
- Poppins everywhere, matching the original export's display face, so the
  rebuilt slides stop reading as a different deck
- slide 2's rule-and-tick strip is replaced by the same node chain used on
  slides 3-4, with the friction stack (handoff / document / wait) sitting in
  each gap: same chain, different transitions
- slide 3's chain gets larger nodes, sublabels and a drawn gate legend
- slide 4's orange swoosh becomes an orthogonal feedback loop
- no glyphs outside Poppins' charset: arrows, gates and brackets are drawn
  as shapes or use ASCII, never box-drawing characters

Slides are flat PNG exports; rebuilt slides get a regenerated background
(flat #0E0E11 + the 44px dot grid) with native, editable text.
Appendix slides are carried over untouched.
"""
import math
import zipfile

from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

from PIL import ImageFont

import icons

SRC, OUT = "deck.pptx", "Pitch_Deck_AthenaRun_v2.pptx"
W, H, PX = 1920, 1080, 6350

BG      = (0x0E, 0x0E, 0x11)
DOT     = (0x15, 0x15, 0x18)
WHITE   = RGBColor(0xEC, 0xEC, 0xEE)
MUTED   = RGBColor(0x9A, 0x9A, 0xA2)
DIM     = RGBColor(0x5A, 0x5A, 0x60)
ORANGE  = RGBColor(0xFF, 0x6B, 0x3D)
RULE    = RGBColor(0x2B, 0x2B, 0x2D)
DIV     = RGBColor(0x1F, 0x1F, 0x22)
PANEL   = RGBColor(0x16, 0x16, 0x19)

SANS, MONO = "Poppins", "Courier New"

TITLE, SUB, MARKER = 27, 14, 11
SECLABEL, STAGE, STAGE_SUB = 11, 17, 12
BODY, BIG, SMALL, SRC_PT = 14, 54, 11, 10

L, R = 110, 1809


def make_background(path="bg.png"):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    for x in range(19, W, 44):
        for y in range(19, H, 44):
            d.rectangle([x, y, x + 1, y + 1], fill=DOT)
    img.save(path)


def redot(draw, x0, y0, x1, y1):
    for x in range(19, W, 44):
        for y in range(19, H, 44):
            if x0 <= x <= x1 and y0 <= y <= y1:
                draw.rectangle([x, y, x + 1, y + 1], fill=DOT)


def shape(slide, kind, x, y, w, h, fill, line_col=None, line_w=1.25, rot=None):
    s = slide.shapes.add_shape(kind, int(x) * PX, int(y) * PX,
                               max(int(w), 1) * PX, max(int(h), 1) * PX)
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if line_col is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line_col
        s.line.width = Pt(line_w)
    s.shadow.inherit = False
    if rot is not None:
        s.rotation = rot
    return s


def text_w(text, pt, bold=False):
    """Width in slide pixels (1 px = 0.5 pt), measured in the real face."""
    f = ImageFont.truetype(
        "fonts/Poppins-SemiBold.ttf" if bold else "fonts/Poppins-Regular.ttf",
        int(pt * 2))
    return f.getlength(text)


def rect(slide, x, y, w, h, colour):
    return shape(slide, MSO_SHAPE.RECTANGLE, x, y, w, h, colour)


def tf_at(slide, x, y, w, h):
    tb = slide.shapes.add_textbox(int(x) * PX, int(y) * PX,
                                  int(w) * PX, int(h) * PX)
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    return tf


def run(p, text, size, colour, font=SANS, bold=False, track=None):
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size); r.font.color.rgb = colour
    r.font.name = font; r.font.bold = bold
    if track:
        r.font._rPr.set("spc", str(int(track * 100)))
    return r


def line(slide, x, y, w, h, parts, align=PP_ALIGN.LEFT, spacing=None):
    tf = tf_at(slide, x, y, w, h)
    p = tf.paragraphs[0]
    p.alignment = align
    if spacing:
        p.line_spacing = Pt(spacing)
    for text, size, col, font, bold, track in parts:
        run(p, text, size, col, font, bold, track)
    return tf


def header(slide, bold_part, muted_part, marker):
    line(slide, L, 90, 1560, 62,
         [(bold_part, TITLE, WHITE, SANS, True, None),
          (" " + muted_part, TITLE, MUTED, SANS, False, None)])
    line(slide, R - 500, 98, 500, 24,
         [(marker, MARKER, MUTED, MONO, False, 1.2)], align=PP_ALIGN.RIGHT)
    rect(slide, L, 172, R - L, 1, RULE)


def logo(slide):
    slide.shapes.add_picture("logo.png", 100 * PX, 1014 * PX, 170 * PX, 40 * PX)


def pic(slide, name, x, y, w, h):
    slide.shapes.add_picture(name, int(x) * PX, int(y) * PX,
                             int(w) * PX, int(h) * PX)


def segment(slide, x1, y1, x2, y2, colour, thickness=1):
    """A straight connector drawn as a thin rotated rectangle."""
    length = math.hypot(x2 - x1, y2 - y1)
    ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    sh = shape(slide, MSO_SHAPE.RECTANGLE, (x1 + x2) / 2 - length / 2,
               (y1 + y2) / 2 - thickness / 2, length, thickness, colour)
    sh.rotation = ang
    return sh


def arrowhead(slide, x, y, ang, colour, size=13):
    """Triangle centred on (x, y) pointing along ang (degrees, y down)."""
    shape(slide, MSO_SHAPE.ISOSCELES_TRIANGLE, x - size / 2, y - size / 2,
          size, size, colour, rot=ang + 90)


def gate(slide, cx, cy, size=15):
    """Human-gate marker: a small orange diamond straddling the spine."""
    shape(slide, MSO_SHAPE.DIAMOND, cx - size / 2, cy - size / 2,
          size, size, ORANGE)


def chip(slide, x, y, label, colour, pt=14, h=56, pad=44):
    """A rounded role tag, sized to its label."""
    w = text_w(label, pt) + pad * 2
    shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, PANEL, colour, 1.25)
    line(slide, x, y, w, h, [(label, pt, colour, SANS, False, None)],
         align=PP_ALIGN.CENTER)
    return w


def chain(slide, y, x0, x1, nodes, start_no=1, gates=False, node_d=88,
          numbers=True, icon_size=36):
    """Spine of circular nodes, each carrying an icon; number above, label below.

    nodes = [(name, sub, icon), ...]
    """
    n = len(nodes)
    pitch = (x1 - x0) / n
    cx = [int(x0 + pitch / 2 + i * pitch) for i in range(n)]
    rect(slide, x0, y, x1 - x0, 1, RULE)
    for i in range(n):
        if gates and i:
            gate(slide, cx[i] - pitch / 2, y)
        shape(slide, MSO_SHAPE.OVAL, cx[i] - node_d / 2, y - node_d / 2,
              node_d, node_d, RGBColor(*BG), MUTED, 1.25)
        pic(slide, nodes[i][2], cx[i] - icon_size / 2, y - icon_size / 2,
            icon_size, icon_size)
        if numbers:
            line(slide, cx[i] - 40, y - node_d / 2 - 26, 80, 24,
                 [(f"{start_no + i:02d}", 11, MUTED, MONO, False, 0.8)],
                 align=PP_ALIGN.CENTER)
    for i, (name, sub, _ic) in enumerate(nodes):
        line(slide, cx[i] - 160, y + node_d / 2 + 22, 320, 34,
             [(name, STAGE, WHITE, SANS, False, None)], align=PP_ALIGN.CENTER)
        if sub:
            line(slide, cx[i] - 160, y + node_d / 2 + 70, 320, 26,
                 [(sub, STAGE_SUB, MUTED, SANS, False, None)],
                 align=PP_ALIGN.CENTER)
    return cx, pitch


# ==========================================================================
# phase A — image surgery
# ==========================================================================
make_background()
icons.build_all()

with zipfile.ZipFile(SRC) as z:
    with z.open("ppt/media/image1.png") as fh:
        opener = Image.open(fh).convert("RGB")
    with z.open("ppt/media/image3.png") as fh:
        Image.open(fh).convert("RGB").crop((100, 1014, 270, 1054)).save("logo.png")

d = ImageDraw.Draw(opener)
d.rectangle([100, 92, 640, 122], fill=BG)
redot(d, 100, 92, 640, 122)
d.rectangle([800, 940, 1870, 1000], fill=BG)
redot(d, 800, 940, 1870, 1000)
opener.save("image1_patched.png")

bg_bytes = open("bg.png", "rb").read()
replace = {
    "ppt/media/image1.png": open("image1_patched.png", "rb").read(),
    "ppt/media/image2.png": bg_bytes,
    "ppt/media/image3.png": bg_bytes,
    "ppt/media/image4.png": bg_bytes,
}
with zipfile.ZipFile(SRC) as zin, \
        zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        zout.writestr(item, replace.get(item.filename, zin.read(item.filename)))

# ==========================================================================
# phase B — native content
# ==========================================================================
prs = Presentation(OUT)
S = list(prs.slides)
blank = S[1].slide_layout


def new_slide():
    s = prs.slides.add_slide(blank)
    s.shapes.add_picture("bg.png", 0, 0, Emu(W * PX), Emu(H * PX))
    return s


# ---- SLIDE 1 — opener -----------------------------------------------------
line(S[0], 116, 726, 1200, 44,
     [("We build the chain, not the generator.", 17, ORANGE, SANS, False, None)])

# ---- SLIDE 2 — the manual chain -------------------------------------------
s2 = S[1]
header(s2, "Still manual.", "And that is where the money goes.",
       "02 — The problem")
line(s2, L, 232, 700, 26,
     [("STILL MANUAL", SECLABEL, MUTED, MONO, False, 3.0)])

P = "ic-person-node.png"
cx2, pitch2 = chain(s2, 366, L, R,
                    [("Requirements", None, P), ("Feasibility", None, P),
                     ("Compliance", None, P), ("Approval", None, P),
                     ("Operations", None, P)], numbers=False)
for i in range(1, 5):                       # friction sits between the steps
    gx = int(cx2[i] - pitch2 / 2)
    for j, ic in enumerate(["ic-handoff.png", "ic-doc.png", "ic-wait.png"]):
        pic(s2, ic, gx - 53 + j * 36, 353, 26, 26)

line(s2, L, 500, 1500, 30,
     [("Five steps around the code. Every one of them a handoff, "
       "a document, a wait.", BODY, MUTED, SANS, False, None)])
rect(s2, L, 556, R - L, 1, RULE)

line(s2, L, 586, 1500, 26,
     [("THEY BOUGHT THE GENERATOR — THE CHAIN AROUND IT IS STILL MANUAL",
       SECLABEL, MUTED, MONO, False, 2.0)])
tf = tf_at(s2, L, 620, 900, 130)
p = tf.paragraphs[0]
run(p, "61", BIG, ORANGE)
run(p, "%", 24, MUTED)
line(s2, L, 772, 1200, 30,
     [("of organizations see no EBIT impact from AI",
       BODY, MUTED, SANS, False, None)])
rect(s2, L, 812, R - L, 1, RULE)
line(s2, L, 838, 1560, 34,
     [("The expensive failures happen before a line of code.",
       16, WHITE, SANS, True, None),
      (" That’s the part we automate.", 16, MUTED, SANS, False, None)])
line(s2, L, 880, 1500, 24,
     [("Source: McKinsey, The State of AI in 2025 — 39% attribute any "
       "EBIT impact to AI", SRC_PT, MUTED, MONO, False, None)])

# ---- SLIDE 3 — idea to build-ready package --------------------------------
s3 = S[2]
header(s3, "From idea to build-ready package.", "", "03 — The chain")
line(s3, L, 196, 1480, 76,
     [("One line, a human gate at every step. AI agents support every stage, ",
       SUB, MUTED, SANS, False, None),
      ("Discover through AI Memory", SUB, WHITE, SANS, True, None),
      (" — from first conversation to a build-ready package.",
       SUB, MUTED, SANS, False, None)], spacing=19)

chain(s3, 440, L, R,
      [("Discover", "from conversation", "ic-chat.png"),
       ("Analyze", "scope + fit", "ic-search.png"),
       ("Research", "cited, deep", "ic-book.png"),
       ("Compliance", "pre-build gate", "ic-shield.png"),
       ("AI Memory", "patterns carried in", "ic-db.png")], gates=True)

gate(s3, L + 7, 622)
line(s3, L + 26, 610, 700, 26,
     [("human gate at every transition", SECLABEL, MUTED, MONO, False, 1.5)])
rect(s3, L, 706, R - L, 1, RULE)
line(s3, L, 736, 900, 26,
     [("IDEA TO BUILD-READY PACKAGE", SECLABEL, MUTED, MONO, False, 3.0)])

# ---- SLIDE 4 — package to running software --------------------------------
s4 = new_slide()
header(s4, "From package to running software.", "", "04 — The chain")
line(s4, L, 196, 1480, 76,
     [("The package is approved. ", SUB, MUTED, SANS, False, None),
      ("Build through Operate", SUB, WHITE, SANS, True, None),
      (" — from approved package to software running in production. "
       "Every decision that matters stays with a person.",
       SUB, MUTED, SANS, False, None)], spacing=19)

# part one, already completed
rect(s4, 150, 440, 300, 1, DIV)
for i in range(5):
    shape(s4, MSO_SHAPE.OVAL, 150 + i * 75 - 7, 433, 14, 14,
          RGBColor(*BG), DIM, 1.0)
line(s4, 110, 472, 380, 24,
     [("01–05 · build-ready package", 10, DIM, MONO, False, 1.0)],
     align=PP_ALIGN.CENTER)

cx4, pitch4 = chain(s4, 440, 520, R,
                    [("Build", "code + review", "ic-code.png"),
                     ("Release", "human approval", "ic-ship.png"),
                     ("Operate", "monitoring", "ic-gauge.png")],
                    start_no=6, gates=True)
gate(s4, 528, 440)

# LEARN: an orthogonal feedback loop, not a swoosh
LOOP_Y, LX, RX = 636, 300, cx4[-1]
rect(s4, RX, 576, 2, LOOP_Y - 576, ORANGE)
rect(s4, LX, LOOP_Y, RX - LX, 2, ORANGE)
rect(s4, LX, 528, 2, LOOP_Y - 528, ORANGE)
shape(s4, MSO_SHAPE.ISOSCELES_TRIANGLE, LX - 8, 508, 18, 22, ORANGE)
line(s4, LX + 40, LOOP_Y + 14, 1100, 26,
     [("LEARN", SECLABEL, ORANGE, MONO, False, 2.0),
      ("  ·  validated patterns from every build carry into the next",
       SECLABEL, MUTED, MONO, False, 1.5)])
rect(s4, L, 706, R - L, 1, RULE)
line(s4, L, 736, 900, 26,
     [("PACKAGE TO RUNNING SOFTWARE", SECLABEL, MUTED, MONO, False, 3.0)])

# ---- SLIDE 5 — the full lifecycle (new) -----------------------------------
sl = new_slide()
header(sl, "The full lifecycle.", "Every phase has an agent.",
       "05 — Lifecycle")
line(sl, L, 196, 1480, 76,
     [("Planning through maintenance — the classic software lifecycle, "
       "run end to end by agents, with a ", SUB, MUTED, SANS, False, None),
      ("human gate at every handover.", SUB, WHITE, SANS, True, None)],
     spacing=19)

CX, CY, RAD, ND = 620, 650, 215, 88
PHASES = [("Planning", "ic-target.png"), ("Analysis", "ic-search.png"),
          ("Design", "ic-layout.png"), ("Implementation", "ic-code.png"),
          ("Testing", "ic-checklist.png"), ("Maintenance", "ic-refresh.png")]
ANG = [-90, -30, 30, 90, 150, 210]
pos = [(CX + RAD * math.cos(math.radians(a)),
        CY + RAD * math.sin(math.radians(a))) for a in ANG]

for i in range(6):
    x1, y1 = pos[i]
    x2, y2 = pos[(i + 1) % 6]
    segment(sl, x1, y1, x2, y2, RULE, 1)
    ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    arrowhead(sl, x1 + (x2 - x1) * 0.76, y1 + (y2 - y1) * 0.76, ang, DIM, 14)
    gate(sl, (x1 + x2) / 2, (y1 + y2) / 2, 16)

for i, (x, y) in enumerate(pos):
    shape(sl, MSO_SHAPE.OVAL, x - ND / 2, y - ND / 2, ND, ND,
          RGBColor(*BG), MUTED, 1.25)
    pic(sl, PHASES[i][1], x - 19, y - 19, 38, 38)

for i, ((x, y), (name, _ic)) in enumerate(zip(pos, PHASES)):
    parts = [(f"{i + 1:02d}  ", 11, MUTED, MONO, False, 0.8),
             (name, 18, WHITE, SANS, False, None)]
    if ANG[i] == -90:
        line(sl, x - 200, y - ND / 2 - 48, 400, 34, parts, align=PP_ALIGN.CENTER)
    elif ANG[i] == 90:
        line(sl, x - 200, y + ND / 2 + 16, 400, 34, parts, align=PP_ALIGN.CENTER)
    elif math.cos(math.radians(ANG[i])) > 0:
        line(sl, x + ND / 2 + 22, y - 17, 320, 34, parts)
    else:
        line(sl, x - ND / 2 - 342, y - 17, 320, 34, parts, align=PP_ALIGN.RIGHT)

line(sl, CX - 200, CY - 30, 400, 26,
     [("ALL SIX PHASES", 10, MUTED, MONO, False, 2.0)], align=PP_ALIGN.CENTER)
line(sl, CX - 200, CY + 2, 400, 38,
     [("agent-run", 21, WHITE, SANS, False, None)], align=PP_ALIGN.CENTER)

# right column: one agent per phase
rect(sl, 1090, 330, 1, 600, DIV)
line(sl, 1150, 344, 700, 26,
     [("ONE AGENT PER PHASE", SECLABEL, MUTED, MONO, False, 2.5)])
AGENTS = [("Planning agent", "scope from first conversation, feasibility and fit"),
          ("Analysis agent", "cited, deep research into the requirements"),
          ("Design agent", "architecture, checked at the compliance gate"),
          ("Build agent", "implementation with code review"),
          ("Test agent", "verification before the release approval"),
          ("Operations agent", "monitoring, patterns back to the library")]
for i, (name, what) in enumerate(AGENTS):
    y = 400 + i * 88
    line(sl, 1150, y, 659, 30, [(name, 16, WHITE, SANS, False, None)])
    line(sl, 1150, y + 34, 659, 30,
         [(what, 12.5, MUTED, SANS, False, None)])

gate(sl, 1157, 946, 16)
line(sl, 1180, 934, 640, 26,
     [("human gate at every handover", SECLABEL, MUTED, MONO, False, 1.5)])

# ---- SLIDE 6 — the payoff (new) -------------------------------------------
sb = new_slide()
header(sb, "The payoff.", "Fewer people. A better starting point.",
       "06 — The payoff")
line(sb, L, 196, 1520, 40,
     [("The chain does the work that used to need a team — every project "
       "starts on what the last one learned.", SUB, MUTED, SANS, False, None)])

line(sb, L, 296, 700, 26,
     [("A TYPICAL PROJECT TEAM", SECLABEL, MUTED, MONO, False, 2.5)])
x = L
for role in ["Business Analyst", "Designer", "Developer"]:
    x += chip(sb, x, 346, role, MUTED) + 20

arrowhead(sb, 962, 374, 0, DIM, 26)

line(sb, 1040, 296, 700, 26,
     [("WITH ATHENARUN", SECLABEL, ORANGE, MONO, False, 2.5)])
w1 = chip(sb, 1040, 346, "One developer", ORANGE, pt=15)
chip(sb, 1040 + w1 + 20, 346, "or a business user", ORANGE, pt=15)
line(sb, 1040, 424, 760, 26,
     [("+ agents on all six lifecycle phases", 12.5, MUTED, SANS, False, None)])

rect(sb, L, 520, R - L, 1, RULE)

BENEFITS = [
    ("ic-people.png", "Fewer roles per project",
     "Eliminates or reduces business analyst, designer and developer "
     "headcount per project."),
    ("ic-person.png", "One developer, internally",
     "AthenaRun runs its own projects with a single developer."),
    ("ic-window.png", "A business user can run it",
     "The platform is operated by the business, not only by engineers."),
    ("ic-layers.png", "A head start on day one",
     "Customers inherit best practices and documented failure learnings "
     "from the first build."),
]
for i, (ic, head, body) in enumerate(BENEFITS):
    y = 552 + i * 74
    pic(sb, ic, L, y + 4, 34, 34)
    line(sb, 166, y, 450, 42, [(head, 17, WHITE, SANS, False, None)])
    line(sb, 640, y, 1169, 42, [(body, 13, MUTED, SANS, False, None)])

rect(sb, L, 830, R - L, 1, RULE)
line(sb, L, 862, 1600, 34,
     [("Same scope, a fraction of the team.", 16, WHITE, SANS, True, None),
      ("  The library is what makes that safe.", 16, MUTED, SANS, False, None)])

# ---- SLIDE 6 — our moat ---------------------------------------------------
s5 = S[3]
header(s5, "Our moat.", "Every build makes the next one safer.",
       "07 — The moat")
x = L
for i, word in enumerate(["Build", "Capture", "Reuse"]):
    w = text_w(word, 22)
    line(s5, x, 232, w + 12, 46, [(word, 22, WHITE, SANS, False, None)])
    x += w + 30
    if i < 2:
        shape(s5, MSO_SHAPE.ISOSCELES_TRIANGLE, x, 250, 13, 15, MUTED, rot=90)
        x += 43
line(s5, L, 302, 1240, 116,
     [("Anyone can generate code. What compounds is what real production "
       "builds taught us — every project writes validated patterns and "
       "documented failures back into the library, and every next build "
       "queries it before a line of code is written.",
       BODY, MUTED, SANS, False, None)], spacing=19)
rect(s5, L, 452, R - L, 1, RULE)

line(s5, L, 484, 700, 26,
     [("THE PATTERN LIBRARY", SECLABEL, MUTED, MONO, False, 3.0)])
line(s5, L, 530, 460, 84, [("Hundreds", 38, WHITE, SANS, False, None)])
line(s5, L, 624, 460, 30,
     [("validated patterns", BODY, WHITE, SANS, False, None)])
line(s5, 590, 530, 480, 84, [("Thousands", 38, ORANGE, SANS, False, None)])
line(s5, 590, 624, 480, 30,
     [("documented anti-patterns", BODY, WHITE, SANS, False, None)])
line(s5, L, 690, 960, 28,
     [("The LEARN loop from the chain is what fills this library.",
       12, MUTED, SANS, False, None)])

rect(s5, 1092, 470, 1, 420, DIV)
rect(s5, 1140, 470, 669, 420, PANEL)
line(s5, 1180, 504, 580, 24,
     [("WHY IT'S DEFENSIBLE", SECLABEL, MUTED, MONO, False, 2.5)])
for i, (head, body) in enumerate([
        ("Earned, not bought.",
         "The library only grows by running real production builds."),
        ("It compounds.",
         "Every project makes the next estimate, gate and build safer."),
        ("Capital can’t copy it.",
         "A bigger round buys code, not failures already survived.")]):
    y = 552 + i * 106
    line(s5, 1180, y, 580, 28, [(head, 13, ORANGE, SANS, True, None)])
    line(s5, 1180, y + 32, 580, 64,
         [(body, SMALL, MUTED, SANS, False, None)], spacing=15)

# ---- SLIDE 6 — references (placeholders kept) -----------------------------
s6 = new_slide()
header(s6, "References.", "Three builds, three problems.", "08 — References")
line(s6, L, 208, 1400, 30,
     [("Shipped software, not pilots. Each one replaced a process that was "
       "running manually.", SUB, MUTED, SANS, False, None)])
rect(s6, L, 288, R - L, 1, RULE)
for i, (name, ic) in enumerate([("CFO App", "ic-chart.png"),
                                ("Lead Generation", "ic-funnel.png"),
                                ("Board Assistant", "ic-bubble.png")]):
    x = L + i * 570
    rect(s6, x, 340, 520, 450, PANEL)
    pic(s6, ic, x + 40, 378, 34, 34)
    line(s6, x + 40, 428, 440, 44, [(name, 20, WHITE, SANS, False, None)])
    for j, (lab, ph) in enumerate([("CLIENT / SECTOR", "[Kunde oder Branche]"),
                                   ("WHAT WE BUILT", "[was gebaut wurde]"),
                                   ("RESULT", "[Ergebnis in einer Zeile]")]):
        y = 500 + j * 92
        line(s6, x + 40, y, 440, 20, [(lab, 9, MUTED, MONO, False, 2.0)])
        line(s6, x + 40, y + 26, 440, 54,
             [(ph, 13, ORANGE, SANS, False, None)], spacing=16)
line(s6, L, 828, 1500, 24,
     [("PLACEHOLDER — replace the three bracketed fields per tile before "
       "this deck goes to an investor.", SRC_PT, ORANGE, MONO, False, None)])

# ---- SLIDE 7 — one question ----------------------------------------------
s7 = new_slide()
header(s7, "One question.", "", "09 — One question")
line(s7, L, 292, 1400, 32,
     [("Ich lasse Ihnen eine Frage da, keinen Prospekt.",
       SUB, MUTED, SANS, False, None)])
line(s7, L, 348, 1620, 260,
     [("Welcher Prozess bei Ihnen läuft heute in ", 33, WHITE, SANS, False, None),
      ("Excel", 33, ORANGE, SANS, False, None),
      (" und sollte es seit einem Jahr nicht mehr?", 33, WHITE, SANS, False, None)],
     spacing=44)
line(s7, L, 668, 1400, 80,
     [("Wenn Ihnen dazu gerade etwas eingefallen ist — sprechen Sie mich an. "
       "Wir machen daraus eine Anwendung. Und wenn Ihnen zwanzig einfallen, "
       "reden wir über die Plattform statt über die Anwendung.",
       12, MUTED, SANS, False, None)], spacing=16)
line(s7, R - 700, 950, 700, 26,
     [("[Name · E-Mail · Telefon]", SRC_PT, ORANGE, MONO, False, None)],
     align=PP_ALIGN.RIGHT)

# ---- SLIDE 8 — appendix divider ------------------------------------------
s8 = new_slide()
header(s8, "Further questions.", "", "10 — Appendix")

for s in (s2, s3, s4, sl, sb, s5, s6, s7, s8):
    logo(s)

# ---- reorder by identity, so adding a slide cannot shift the mapping ------
desired = [S[0], s2, s3, s4, sl, sb, s5, s6, s7, s8] + S[4:9]
lst = prs.slides._sldIdLst
ids = list(lst)
current = list(prs.slides)
for e in ids:
    lst.remove(e)
for slide in desired:
    lst.append(ids[current.index(slide)])

prs.save(OUT)
print(f"wrote {OUT}")
