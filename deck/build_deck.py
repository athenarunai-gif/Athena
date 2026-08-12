"""Restructure the AthenaRun deck to 13 slides (8 main + 5 appendix).

Every original slide is a flat PNG export. Slides that only lose an element are
edited in the image; slides that are restructured, and the four new slides, get
a regenerated background (flat #0E0E11 plus the deck's 44px dot grid, matched
pixel for pixel) with native, editable text on top.

The five appendix slides are carried over untouched.
"""
import copy
import zipfile

from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

SRC, OUT = "deck.pptx", "Pitch_Deck_AthenaRun_v2.pptx"
W, H, PX = 1920, 1080, 6350          # export size in px, EMU per px

BG      = (0x0E, 0x0E, 0x11)
DOT     = (0x15, 0x15, 0x18)
WHITE   = RGBColor(0xEC, 0xEC, 0xEE)
MUTED   = RGBColor(0x9A, 0x9A, 0xA2)
ORANGE  = RGBColor(0xFF, 0x6B, 0x3D)
RULE    = RGBColor(0x2B, 0x2B, 0x2D)
DIV     = RGBColor(0x1F, 0x1F, 0x22)
PANEL   = RGBColor(0x16, 0x16, 0x19)

SANS, MONO = "Arial", "Courier New"

# type scale in pt, measured off the original export (1 px = 0.5 pt)
TITLE, SUB, MARKER = 23, 12, 11
SECLABEL, STAGE, STAGE_BIG, STAGE_SUB = 11, 13, 19, 10
BODY, BIG, BIG2, SMALL, SRC_PT, LEAD = 12, 64, 50, 10, 8, 22

L, R = 110, 1809                     # content margins


# --------------------------------------------------------------------------
# background: flat fill plus the deck's dot grid (2x2 px, 44 px pitch, at 19/19)
# --------------------------------------------------------------------------
def make_background(path="bg.png"):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    for x in range(19, W, 44):
        for y in range(19, H, 44):
            d.rectangle([x, y, x + 1, y + 1], fill=DOT)
    img.save(path)
    return path


# --------------------------------------------------------------------------
# drawing helpers -- all coordinates in export pixels
# --------------------------------------------------------------------------
def rect(slide, x, y, w, h, colour):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x * PX, y * PX,
                               max(w, 1) * PX, max(h, 1) * PX)
    s.fill.solid()
    s.fill.fore_color.rgb = colour
    s.line.fill.background()
    s.shadow.inherit = False
    return s


def tf_at(slide, x, y, w, h, anchor=MSO_ANCHOR.MIDDLE, wrap=True):
    tb = slide.shapes.add_textbox(x * PX, y * PX, w * PX, h * PX)
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    return tf


def run(p, text, size, colour, font=SANS, bold=False, track=None):
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.color.rgb = colour
    r.font.name = font
    r.font.bold = bold
    if track:                       # character spacing, in hundredths of a point
        r.font._rPr.set("spc", str(int(track * 100)))
    return r


def line(slide, x, y, w, h, colour, parts, align=PP_ALIGN.LEFT, spacing=None):
    """parts = [(text, size, colour, font, bold, track), ...]"""
    tf = tf_at(slide, x, y, w, h)
    p = tf.paragraphs[0]
    p.alignment = align
    if spacing:
        p.line_spacing = Pt(spacing)
    for text, size, col, font, bold, track in parts:
        run(p, text, size, col, font, bold, track)
    return tf


def header(slide, bold_part, muted_part, marker):
    """Standard slide header: title at y100-142, marker top right, rule at y172."""
    line(slide, L, 96, 1400, 50, WHITE,
         [(bold_part, TITLE, WHITE, SANS, True, None),
          (" " + muted_part, TITLE, MUTED, SANS, False, None)])
    line(slide, R - 500, 98, 500, 22, MUTED,
         [(marker, MARKER, MUTED, MONO, False, 1.2)], align=PP_ALIGN.RIGHT)
    rect(slide, L, 172, R - L, 1, RULE)


def logo(slide):
    slide.shapes.add_picture("logo.png", 100 * PX, 1014 * PX, 170 * PX, 40 * PX)


def stage_strip(slide, y_rule, stages, big=False, div_h=100):
    """The deck's process-strip motif: tick marks sitting on a full-width rule,
    stage names beneath, thin dividers between the columns."""
    n = len(stages)
    span = R - L
    pitch = span / n
    name_pt = STAGE_BIG if big else STAGE
    tick_h, tick_w = (6, 64) if big else (4, 44)
    name_y = y_rule + (34 if big else 30)
    name_h = 46 if big else 26

    rect(slide, L, y_rule, span, 1, RULE)
    rect(slide, L, y_rule + 1, span, 1, MUTED)

    for i, (name, sub) in enumerate(stages):
        x = int(L + i * pitch)
        rect(slide, x, y_rule, tick_w, tick_h, MUTED)
        if i:
            rect(slide, x - 40, y_rule + tick_h, 1, div_h, DIV)
        line(slide, x, name_y, int(pitch) - 24, name_h, WHITE,
             [(name, name_pt, WHITE, SANS, False, None)])
        if sub:
            line(slide, x, name_y + name_h + 6, int(pitch) - 24, 22, MUTED,
                 [(sub, STAGE_SUB, MUTED, SANS, False, None)])


# ==========================================================================
# phase A -- image surgery on the original package
# ==========================================================================
make_background()

with zipfile.ZipFile(SRC) as z:
    with z.open("ppt/media/image1.png") as fh:
        opener = Image.open(fh).convert("RGB")
    with z.open("ppt/media/image3.png") as fh:
        Image.open(fh).convert("RGB").crop((100, 1014, 270, 1054)).save("logo.png")

# slide 1: drop the "INVESTOR BRIEFING - CONFIDENTIAL" line (x111-614, y100-113)
d = ImageDraw.Draw(opener)
d.rectangle([100, 92, 640, 122], fill=BG)
for x in range(19, W, 44):                      # restore the dot grid underneath
    for y in range(19, H, 44):
        if 100 <= x <= 640 and 92 <= y <= 122:
            d.rectangle([x, y, x + 1, y + 1], fill=DOT)
opener.save("image1_patched.png")

bg_bytes = open("bg.png", "rb").read()
replace = {
    "ppt/media/image1.png": open("image1_patched.png", "rb").read(),
    "ppt/media/image2.png": bg_bytes,           # slide 2, rebuilt
    "ppt/media/image3.png": bg_bytes,           # slide 3, rebuilt
    "ppt/media/image4.png": bg_bytes,           # moat, rebuilt
}
with zipfile.ZipFile(SRC) as zin, \
        zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        zout.writestr(item, replace.get(item.filename, zin.read(item.filename)))

# ==========================================================================
# phase B -- native content
# ==========================================================================
prs = Presentation(OUT)
S = list(prs.slides)
blank = S[1].slide_layout


def new_slide():
    s = prs.slides.add_slide(blank)
    s.shapes.add_picture("bg.png", 0, 0, Emu(W * PX), Emu(H * PX))
    return s


# ---- SLIDE 2 -- Still manual ---------------------------------------------
s2 = S[1]
header(s2, "Still manual.", "And that is where the money goes.", "02 — The problem")
line(s2, L, 290, 600, 20, MUTED,
     [("STILL MANUAL", SECLABEL, MUTED, MONO, False, 3.0)])
stage_strip(s2, 340, [("Requirements", None), ("Feasibility", None),
                      ("Compliance", None), ("Approval", None),
                      ("Operations", None)], big=True, div_h=130)
line(s2, L, 500, 1400, 30, MUTED,
     [("Five steps around the code. Every one of them a handoff, "
       "a document, a wait.", BODY + 1, MUTED, SANS, False, None)])
rect(s2, L, 580, R - L, 1, RULE)

tf = tf_at(s2, L, 630, 900, 110)
p = tf.paragraphs[0]
run(p, "39", BIG, WHITE)
run(p, "%", 26, MUTED)
line(s2, L, 762, 1200, 26, MUTED,
     [("of organizations report any EBIT impact from AI",
       BODY, MUTED, SANS, False, None)])
rect(s2, L, 830, R - L, 1, RULE)
line(s2, L, 866, 1500, 32, WHITE,
     [("The expensive failures happen before a line of code.",
       BODY + 2, WHITE, SANS, True, None),
      (" That’s the part we automate.", BODY + 2, MUTED, SANS, False, None)])
line(s2, L, 908, 1400, 20, MUTED,
     [("Source: McKinsey, The State of AI in 2025",
       SRC_PT, MUTED, MONO, False, None)])

# ---- SLIDE 3 -- idea to build-ready package -------------------------------
s3 = S[2]
header(s3, "From idea to running software.", "", "03 — The chain, part 1")
line(s3, L, 160, 1480, 102, MUTED,
     [("One line, a human gate at every step. AI agents support every stage, ",
       SUB, MUTED, SANS, False, None),
      ("Discover through AI Memory", SUB, WHITE, SANS, True, None),
      (" — from first conversation to a build-ready package.",
       SUB, MUTED, SANS, False, None)], spacing=17)
stage_strip(s3, 540, [("Discover", "from conversation"), ("Analyze", "scope + fit"),
                      ("Research", "cited, deep"), ("Compliance", "pre-build gate"),
                      ("AI Memory", "patterns carried in")])
line(s3, L, 700, 900, 20, MUTED,
     [("IDEA TO BUILD-READY PACKAGE", SECLABEL, MUTED, MONO, False, 3.0)])

# ---- SLIDE 4 -- package to running software (new) -------------------------
s4 = new_slide()
header(s4, "From idea to running software.", "", "04 — The chain, part 2")
line(s4, L, 160, 1480, 102, MUTED,
     [("The package is approved. ", SUB, MUTED, SANS, False, None),
      ("Build through Operate", SUB, WHITE, SANS, True, None),
      (" — from approved package to software running in production. "
       "Every decision that matters stays with a person.",
       SUB, MUTED, SANS, False, None)], spacing=17)
stage_strip(s4, 540, [("Build", "code + review"), ("Release", "human approval"),
                      ("Operate", "monitoring")])
line(s4, L, 700, 900, 20, MUTED,
     [("PACKAGE TO RUNNING SOFTWARE", SECLABEL, MUTED, MONO, False, 3.0)])
rect(s4, L, 770, R - L, 1, RULE)
line(s4, L, 800, 1500, 26, MUTED,
     [("LEARN", SECLABEL, ORANGE, MONO, False, 1.5),
      ("   ·   validated patterns from every project carry into the next build",
       SECLABEL, MUTED, MONO, False, 1.5)])

# ---- SLIDE 5 -- our moat --------------------------------------------------
s5 = S[3]
header(s5, "Our moat.", "Every build makes the next one safer.", "05 — The moat")
line(s5, L, 270, 900, 50, WHITE,
     [("Build", LEAD, WHITE, SANS, False, None),
      ("   →   ", LEAD, MUTED, SANS, False, None),
      ("Capture", LEAD, WHITE, SANS, False, None),
      ("   →   ", LEAD, MUTED, SANS, False, None),
      ("Reuse", LEAD, WHITE, SANS, False, None)])
line(s5, L, 348, 1080, 102, MUTED,
     [("Anyone can generate code. What compounds is what real production builds "
       "taught us — every project writes validated patterns and documented "
       "failures back into the library, and every next build queries it before "
       "a line of code is written.", BODY, MUTED, SANS, False, None)], spacing=17)
rect(s5, L, 488, R - L, 1, RULE)

line(s5, L, 522, 700, 20, MUTED,
     [("THE PATTERN LIBRARY", SECLABEL, MUTED, MONO, False, 3.0)])
line(s5, L, 576, 460, 92, WHITE,
     [("Hundreds", BIG - 24, WHITE, SANS, False, None)])
line(s5, L, 688, 460, 22, MUTED,
     [("VALIDATED PATTERNS", SECLABEL, MUTED, MONO, False, 2.5)])
line(s5, 590, 576, 460, 92, ORANGE,
     [("Thousands", BIG - 24, ORANGE, SANS, False, None)])
line(s5, 590, 688, 460, 22, MUTED,
     [("DOCUMENTED ANTI-PATTERNS", SECLABEL, MUTED, MONO, False, 2.5)])

rect(s5, 1092, 540, 1, 360, DIV)
rect(s5, 1140, 540, 669, 360, PANEL)
line(s5, 1180, 578, 580, 22, MUTED,
     [("WHY IT'S DEFENSIBLE", SECLABEL, MUTED, MONO, False, 2.5)])
for i, (head, body) in enumerate([
        ("Earned, not bought.",
         "The library only grows by running real production builds."),
        ("It compounds.",
         "Every project makes the next estimate, gate and build safer."),
        ("Capital can’t copy it.",
         "A bigger round buys code, not failures already survived.")]):
    y = 630 + i * 88
    line(s5, 1180, y, 580, 24, WHITE,
         [(head, BODY, WHITE, SANS, True, None)])
    line(s5, 1180, y + 28, 580, 52, MUTED,
         [(body, SMALL, MUTED, SANS, False, None)], spacing=13)

# ---- SLIDE 6 -- references (placeholder scaffold) -------------------------
s6 = new_slide()
header(s6, "References.", "Three builds, three problems.", "06 — References")
line(s6, L, 200, 1400, 30, MUTED,
     [("Shipped software, not pilots. Each one replaced a process that was "
       "running manually.", SUB, MUTED, SANS, False, None)])
rect(s6, L, 300, R - L, 1, RULE)
for i, name in enumerate(["CFO App", "Lead Generation", "Board Assistant"]):
    x = L + i * 570
    rect(s6, x, 360, 520, 430, PANEL)
    rect(s6, x + 40, 400, 44, 4, MUTED)
    line(s6, x + 40, 430, 440, 40, WHITE,
         [(name, LEAD - 3, WHITE, SANS, False, None)])
    for j, (lab, ph) in enumerate([("CLIENT / SECTOR", "⟨Kunde oder Branche⟩"),
                                   ("WHAT WE BUILT", "⟨was gebaut wurde⟩"),
                                   ("RESULT", "⟨Ergebnis in einer Zeile⟩")]):
        y = 505 + j * 88
        line(s6, x + 40, y, 440, 18, MUTED,
             [(lab, 8, MUTED, MONO, False, 2.0)])
        line(s6, x + 40, y + 24, 440, 60, ORANGE,
             [(ph, BODY, ORANGE, SANS, False, None)], spacing=15)
line(s6, L, 830, 1500, 22, MUTED,
     [("PLACEHOLDER — replace the three bracketed fields per tile before "
       "this deck goes to an investor.", SRC_PT, ORANGE, MONO, False, None)])

# ---- SLIDE 7 -- the ask ---------------------------------------------------
s7 = new_slide()
header(s7, "The ask.", "", "07 — The ask")
line(s7, L, 300, 1400, 30, MUTED,
     [("Ich lasse Ihnen eine Frage da, keinen Prospekt.",
       SUB + 2, MUTED, SANS, False, None)])
line(s7, L, 352, 1620, 252, WHITE,
     [("Welcher Prozess bei Ihnen läuft heute in Excel und sollte es seit "
       "einem Jahr nicht mehr?", 34, WHITE, SANS, False, None), ], spacing=42)
line(s7, L, 662, 1400, 108, MUTED,
     [("Wenn Ihnen dazu gerade etwas eingefallen ist — sprechen Sie mich an. "
       "Wir machen daraus eine Anwendung. Und wenn Ihnen zwanzig einfallen, "
       "reden wir über die Plattform statt über die Anwendung.",
       SUB + 1, MUTED, SANS, False, None)], spacing=18)

# ---- SLIDE 8 -- appendix divider ------------------------------------------
s8 = new_slide()
header(s8, "Further questions.", "", "08 — Appendix")

for s in (s2, s3, s4, s5, s6, s7, s8):
    logo(s)

# ---- reorder: o1 o2 o3 NEW4 o4 NEW6 NEW7 NEW8 o5 o6 o7 o8 o9 --------------
lst = prs.slides._sldIdLst
ids = list(lst)
order = [0, 1, 2, 9, 3, 10, 11, 12, 4, 5, 6, 7, 8]
for e in ids:
    lst.remove(e)
for i in order:
    lst.append(ids[i])

prs.save(OUT)
print(f"wrote {OUT} with {len(prs.slides.__iter__.__self__._sldIdLst)} slides")
