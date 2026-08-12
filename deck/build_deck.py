"""AthenaRun deck v3 — 13 slides (8 main + 5 appendix).

v3 implements the design review on top of the v2 restructure:
- type scale one step up everywhere (nothing below 10pt)
- real process graphics: friction icons between the manual steps (slide 2),
  numbered node chains with orange human gates (slides 3-4), LEARN loop
  drawn as an arc (slide 4)
- orange carries exactly one meaning per slide (61, gates, arc, results, Excel)
- slide 1 gains the tagline under the thesis, loses its tiny footer twin
- slide 2 stat inverted to 61% "no EBIT impact" (same McKinsey figure)
- slides 3/4 titled by what they actually deliver
- slide 7 renamed "One question."

Slides are flat PNG exports; rebuilt slides get a regenerated background
(flat #0E0E11 + the 44px dot grid) with native, editable text.
Appendix slides are carried over untouched.
"""
import zipfile

from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

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

SANS, MONO = "Arial", "Courier New"

# type scale, one step up from v2 (1 px = 0.5 pt)
TITLE, SUB, MARKER = 28, 14, 11
SECLABEL, STAGE, STAGE_SUB = 11, 16, 12
BODY, BIG, SMALL, SRC_PT = 14, 64, 11, 10

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


def rect(slide, x, y, w, h, colour):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x * PX, y * PX,
                               max(w, 1) * PX, max(h, 1) * PX)
    s.fill.solid(); s.fill.fore_color.rgb = colour
    s.line.fill.background(); s.shadow.inherit = False
    return s


def circle(slide, cx, cy, d_, line_col, line_w=1.5, fill=None):
    s = slide.shapes.add_shape(MSO_SHAPE.OVAL, int(cx - d_ / 2) * PX,
                               int(cy - d_ / 2) * PX, d_ * PX, d_ * PX)
    if fill is None:
        s.fill.solid(); s.fill.fore_color.rgb = RGBColor(*BG)
    else:
        s.fill.solid(); s.fill.fore_color.rgb = fill
    s.line.color.rgb = line_col
    s.line.width = Pt(line_w)
    s.shadow.inherit = False
    return s


def diamond(slide, cx, cy, d_, colour):
    s = slide.shapes.add_shape(MSO_SHAPE.DIAMOND, int(cx - d_ / 2) * PX,
                               int(cy - d_ / 2) * PX, d_ * PX, d_ * PX)
    s.fill.solid(); s.fill.fore_color.rgb = colour
    s.line.fill.background(); s.shadow.inherit = False
    return s


def tf_at(slide, x, y, w, h, anchor=MSO_ANCHOR.MIDDLE):
    tb = slide.shapes.add_textbox(x * PX, y * PX, w * PX, h * PX)
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.word_wrap = True
    tf.vertical_anchor = anchor
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
    line(slide, R - 500, 98, 500, 22,
         [(marker, MARKER, MUTED, MONO, False, 1.2)], align=PP_ALIGN.RIGHT)
    rect(slide, L, 172, R - L, 1, RULE)


def logo(slide):
    slide.shapes.add_picture("logo.png", 100 * PX, 1014 * PX, 170 * PX, 40 * PX)


def pic(slide, name, x, y, w, h):
    slide.shapes.add_picture(name, x * PX, y * PX, w * PX, h * PX)


def node_chain(slide, y_mid, x0, x1, nodes, start_no=1, gate_entry=False):
    """Numbered circle nodes on a continuous line, orange diamond gates
    between them. nodes = [(name, sub), ...]"""
    n = len(nodes)
    pitch = (x1 - x0) / n
    centers = [int(x0 + pitch / 2 + i * pitch) for i in range(n)]
    rect(slide, x0, y_mid, x1 - x0, 1, RULE)
    if gate_entry:
        diamond(slide, x0 + 8, y_mid, 16, ORANGE)
    for i, cx in enumerate(centers):
        if i:
            diamond(slide, int(cx - pitch / 2), y_mid, 16, ORANGE)
    for i, (cx, (name, sub)) in enumerate(zip(centers, nodes)):
        circle(slide, cx, y_mid, 64, MUTED, 1.5)
        line(slide, cx - 40, y_mid - 16, 80, 32,
             [(f"{start_no + i:02d}", 13, MUTED, MONO, False, 1.0)],
             align=PP_ALIGN.CENTER)
        line(slide, cx - 150, y_mid + 48, 300, 34,
             [(name, STAGE, WHITE, SANS, False, None)], align=PP_ALIGN.CENTER)
        if sub:
            line(slide, cx - 150, y_mid + 84, 300, 26,
                 [(sub, STAGE_SUB, MUTED, SANS, False, None)],
                 align=PP_ALIGN.CENTER)
    return centers


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
d.rectangle([100, 92, 640, 122], fill=BG)          # "INVESTOR BRIEFING" line
redot(d, 100, 92, 640, 122)
d.rectangle([800, 940, 1870, 1000], fill=BG)       # tiny footer tagline
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


# ---- SLIDE 1 — opener: tagline joins the thesis ---------------------------
s1 = S[0]
line(s1, 116, 726, 1200, 44,
     [("We build the chain, not the generator.", 17, ORANGE, SANS, False, None)])

# ---- SLIDE 2 — Still manual ----------------------------------------------
s2 = S[1]
header(s2, "Still manual.", "And that is where the money goes.",
       "02 — The problem")
line(s2, L, 242, 600, 28,
     [("STILL MANUAL", SECLABEL, MUTED, MONO, False, 3.0)])

pitch2 = (R - L) / 5
rect(s2, L, 300, R - L, 1, RULE)
rect(s2, L, 301, R - L, 1, MUTED)
for i, name in enumerate(["Requirements", "Feasibility", "Compliance",
                          "Approval", "Operations"]):
    x = int(L + i * pitch2)
    rect(s2, x, 300, 64, 6, MUTED)
    line(s2, x, 336, int(pitch2) - 104, 50,
         [(name, 19, WHITE, SANS, False, None)])
    if i:                                # friction stack in each gap
        gx = x - 70
        pic(s2, "ic-handoff.png", gx, 336, 28, 28)
        pic(s2, "ic-doc.png", gx, 376, 28, 28)
        pic(s2, "ic-wait.png", gx, 416, 28, 28)
line(s2, L, 480, 1500, 30,
     [("Five steps around the code. Every one of them a handoff, "
       "a document, a wait.", BODY, MUTED, SANS, False, None)])
rect(s2, L, 556, R - L, 1, RULE)

line(s2, L, 588, 1500, 28,
     [("THEY BOUGHT THE GENERATOR — THE CHAIN AROUND IT IS STILL MANUAL",
       SECLABEL, MUTED, MONO, False, 2.0)])
tf = tf_at(s2, L, 626, 900, 130)
p = tf.paragraphs[0]
run(p, "61", BIG, ORANGE)
run(p, "%", 26, MUTED)
line(s2, L, 766, 1200, 30,
     [("of organizations see no EBIT impact from AI",
       BODY, MUTED, SANS, False, None)])
rect(s2, L, 830, R - L, 1, RULE)
line(s2, L, 862, 1560, 34,
     [("The expensive failures happen before a line of code.",
       16, WHITE, SANS, True, None),
      (" That’s the part we automate.", 16, MUTED, SANS, False, None)])
line(s2, L, 908, 1500, 24,
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
line(s3, L, 376, 900, 28,
     [("IDEA TO BUILD-READY PACKAGE", SECLABEL, MUTED, MONO, False, 3.0)])
node_chain(s3, 560, L, R,
           [("Discover", "from conversation"), ("Analyze", "scope + fit"),
            ("Research", "cited, deep"), ("Compliance", "pre-build gate"),
            ("AI Memory", "patterns carried in")])
line(s3, L, 740, 1200, 26,
     [("◆", 12, ORANGE, SANS, False, None),
      ("   human gate at every transition", SECLABEL, MUTED, MONO, False, 1.5)])

# ---- SLIDE 4 — package to running software --------------------------------
s4 = new_slide()
header(s4, "From package to running software.", "", "04 — The chain")
line(s4, L, 196, 1480, 76,
     [("The package is approved. ", SUB, MUTED, SANS, False, None),
      ("Build through Operate", SUB, WHITE, SANS, True, None),
      (" — from approved package to software running in production. "
       "Every decision that matters stays with a person.",
       SUB, MUTED, SANS, False, None)], spacing=19)
line(s4, L, 376, 900, 28,
     [("PACKAGE TO RUNNING SOFTWARE", SECLABEL, MUTED, MONO, False, 3.0)])

# mini-trail: part 1, already done
rect(s4, 140, 560, 400, 1, DIV)
for i in range(5):
    circle(s4, 140 + i * 100, 560, 14, DIM, 1.0)
line(s4, 110, 596, 460, 22,
     [("01–05 · build-ready package", 10, DIM, MONO, False, 1.0)],
     align=PP_ALIGN.CENTER)
rect(s4, 540, 560, 60, 1, RULE)

node_chain(s4, 560, 600, R,
           [("Build", "code + review"), ("Release", "human approval"),
            ("Operate", "monitoring")], start_no=6, gate_entry=True)

pic(s4, "ic-arc.png", 330, 640, 1280, 170)
line(s4, 310, 830, 1300, 26,
     [("LEARN", SECLABEL, ORANGE, MONO, False, 2.0),
      ("  ·  validated patterns from every build carry into the next",
       SECLABEL, MUTED, MONO, False, 1.5)], align=PP_ALIGN.CENTER)

# ---- SLIDE 5 — our moat ---------------------------------------------------
s5 = S[3]
header(s5, "Our moat.", "Every build makes the next one safer.",
       "05 — The moat")
line(s5, L, 236, 900, 50,
     [("Build", 22, WHITE, SANS, False, None),
      ("  ►  ", 16, MUTED, SANS, False, None),
      ("Capture", 22, WHITE, SANS, False, None),
      ("  ►  ", 16, MUTED, SANS, False, None),
      ("Reuse", 22, WHITE, SANS, False, None)])
line(s5, L, 306, 1080, 124,
     [("Anyone can generate code. What compounds is what real production "
       "builds taught us — every project writes validated patterns and "
       "documented failures back into the library, and every next build "
       "queries it before a line of code is written.",
       BODY, MUTED, SANS, False, None)], spacing=19)
rect(s5, L, 452, R - L, 1, RULE)

line(s5, L, 482, 700, 28,
     [("THE PATTERN LIBRARY", SECLABEL, MUTED, MONO, False, 3.0)])
line(s5, L, 530, 460, 88,
     [("Hundreds", 40, WHITE, SANS, False, None)])
line(s5, L, 626, 460, 30,
     [("validated patterns", BODY, WHITE, SANS, False, None)])
line(s5, 590, 530, 480, 88,
     [("Thousands", 40, ORANGE, SANS, False, None)])
line(s5, 590, 626, 480, 30,
     [("documented anti-patterns", BODY, WHITE, SANS, False, None)])
line(s5, L, 690, 960, 28,
     [("The LEARN loop from the chain is what fills this library.",
       12, MUTED, SANS, False, None)])

rect(s5, 1092, 470, 1, 420, DIV)
rect(s5, 1140, 470, 669, 420, PANEL)
line(s5, 1180, 502, 580, 22,
     [("WHY IT'S DEFENSIBLE", SECLABEL, MUTED, MONO, False, 2.5)])
for i, (head, body) in enumerate([
        ("Earned, not bought.",
         "The library only grows by running real production builds."),
        ("It compounds.",
         "Every project makes the next estimate, gate and build safer."),
        ("Capital can’t copy it.",
         "A bigger round buys code, not failures already survived.")]):
    y = 548 + i * 108
    line(s5, 1180, y, 580, 28,
         [(head, 13, ORANGE, SANS, True, None)])
    line(s5, 1180, y + 32, 580, 58,
         [(body, SMALL, MUTED, SANS, False, None)], spacing=15)

# ---- SLIDE 6 — references (placeholders stay) -----------------------------
s6 = new_slide()
header(s6, "References.", "Three builds, three problems.", "06 — References")
line(s6, L, 208, 1400, 30,
     [("Shipped software, not pilots. Each one replaced a process that was "
       "running manually.", SUB, MUTED, SANS, False, None)])
rect(s6, L, 288, R - L, 1, RULE)
for i, (name, ic) in enumerate([("CFO App", "ic-chart.png"),
                                ("Lead Generation", "ic-funnel.png"),
                                ("Board Assistant", "ic-bubble.png")]):
    x = L + i * 570
    rect(s6, x, 340, 520, 450, PANEL)
    pic(s6, ic, x + 40, 378, 36, 36)
    line(s6, x + 40, 430, 440, 40,
         [(name, 20, WHITE, SANS, False, None)])
    for j, (lab, ph) in enumerate([("CLIENT / SECTOR", "⟨Kunde oder Branche⟩"),
                                   ("WHAT WE BUILT", "⟨was gebaut wurde⟩"),
                                   ("RESULT", "⟨Ergebnis in einer Zeile⟩")]):
        y = 500 + j * 92
        line(s6, x + 40, y, 440, 18,
             [(lab, 9, MUTED, MONO, False, 2.0)])
        line(s6, x + 40, y + 24, 440, 56,
             [(ph, 13, ORANGE, SANS, False, None)], spacing=16)
line(s6, L, 828, 1500, 24,
     [("PLACEHOLDER — replace the three bracketed fields per tile before "
       "this deck goes to an investor.", SRC_PT, ORANGE, MONO, False, None)])

# ---- SLIDE 7 — one question ----------------------------------------------
s7 = new_slide()
header(s7, "One question.", "", "07 — One question")
line(s7, L, 292, 1400, 32,
     [("Ich lasse Ihnen eine Frage da, keinen Prospekt.",
       SUB, MUTED, SANS, False, None)])
line(s7, L, 348, 1620, 256,
     [("Welcher Prozess bei Ihnen läuft heute in ",
       34, WHITE, SANS, False, None),
      ("Excel", 34, ORANGE, SANS, False, None),
      (" und sollte es seit einem Jahr nicht mehr?",
       34, WHITE, SANS, False, None)], spacing=42)
line(s7, L, 664, 1400, 76,
     [("Wenn Ihnen dazu gerade etwas eingefallen ist — sprechen Sie mich an. "
       "Wir machen daraus eine Anwendung. Und wenn Ihnen zwanzig einfallen, "
       "reden wir über die Plattform statt über die Anwendung.",
       12, MUTED, SANS, False, None)], spacing=16)
line(s7, R - 700, 950, 700, 24,
     [("⟨Name · E-Mail · Telefon⟩", SRC_PT, ORANGE, MONO, False, None)],
     align=PP_ALIGN.RIGHT)

# ---- SLIDE 8 — appendix divider ------------------------------------------
s8 = new_slide()
header(s8, "Further questions.", "", "08 — Appendix")

for s in (s2, s3, s4, s5, s6, s7, s8):
    logo(s)

# ---- reorder --------------------------------------------------------------
lst = prs.slides._sldIdLst
ids = list(lst)
order = [0, 1, 2, 9, 3, 10, 11, 12, 4, 5, 6, 7, 8]
for e in ids:
    lst.remove(e)
for i in order:
    lst.append(ids[i])

prs.save(OUT)
print(f"wrote {OUT}")
