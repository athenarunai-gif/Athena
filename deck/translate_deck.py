"""Build the German deck from the English one.

Every run is looked up in de_text.DE; anything left over is reported rather
than silently shipped in English. Slide 1 is a special case: its headline and
sub-line are baked into the picture, so that band of the image is repainted
with the plain dot grid and the German headline is set as real text.

Outputs:
  Pitch_Deck_AthenaRun_DE.pptx          — Poppins, the deck itself
  AthenaRun_Pitch_Deck_DE_Keynote.pptx  — Helvetica, to import into Keynote
"""
import io
import re
import sys

from PIL import Image
from pptx import Presentation
from pptx.util import Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

from de_text import DE, KEEP, TITLE_DE, SUB_DE

SRC = "Pitch_Deck_AthenaRun_v2.pptx"
PX = 6350
W, H = 1920, 1080
L, R = 110, 1809
WHITE = RGBColor(0xEC, 0xEC, 0xEE)
MUTED = RGBColor(0x9A, 0x9A, 0xA2)

# the band of slide 1's picture that carries the English headline and sub-line
BAND = (372, 700)
TITLE_SIZE = 56


def repaint_title_band():
    """Return slide 1's picture with the headline band reset to the dot grid."""
    prs = Presentation(SRC)
    pic = [sh for sh in list(prs.slides)[0].shapes if sh.shape_type == 13][0]
    baked = Image.open(io.BytesIO(pic.image.blob)).convert("RGB")
    grid = Image.open("bg.png").convert("RGB").resize(baked.size)
    y0, y1 = BAND
    baked.paste(grid.crop((0, y0, baked.width, y1)), (0, y0))
    out = io.BytesIO()
    baked.save(out, format="PNG")
    return out.getvalue()


def line(sl, x, y, w, h, parts, font, size, align=PP_ALIGN.LEFT):
    tb = sl.shapes.add_textbox(int(x) * PX, int(y) * PX, int(w) * PX, int(h) * PX)
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = align
    for text, colour, bold in parts:
        r = p.add_run()
        r.text = text
        r.font.size = Pt(size)
        r.font.color.rgb = colour
        r.font.name = font
        r.font.bold = bold
    return tb


def build(out_path, font):
    prs = Presentation(SRC)
    slides = list(prs.slides)

    # ---- slide 1: repaint the baked band, then set the German headline ----
    first = slides[0]
    pic = [sh for sh in first.shapes if sh.shape_type == 13][0]
    rId = pic._element.blip_rId
    first.part.related_part(rId)._blob = repaint_title_band()

    l1, l2 = TITLE_DE
    line(first, L, 382, R - L, 118, [(l1, WHITE, True)], font, TITLE_SIZE)
    line(first, L, 499, R - L, 118, [(l2, MUTED, False)], font, TITLE_SIZE)
    line(first, L, 661, 1500, 34, [(SUB_DE, MUTED, False)], font, 14)

    # ---- slide 8: the three words are wider in German than in English ----
    #      so the row is laid out again around the two arrowheads
    moat = slides[7]
    words, arrows = [], []
    for sh in moat.shapes:
        if sh.has_text_frame and sh.text_frame.text.strip() in ("Build", "Capture", "Reuse"):
            words.append(sh)
        else:
            try:
                if int(sh.auto_shape_type) == 7:
                    arrows.append(sh)
            except Exception:
                pass
    words.sort(key=lambda s: s.left)
    arrows.sort(key=lambda s: s.left)
    widths = [150, 200, 420]          # German: Bauen / Erfassen / Wiederverwenden
    x = 110
    for i, sh in enumerate(words):
        sh.left, sh.width = int(x) * PX, widths[i] * PX
        x += widths[i]
        if i < len(arrows):
            a = arrows[i]
            a.left = int(x + 20 - a.width / PX / 2) * PX
            x += 60

    # ---- every other run: straight lookup --------------------------------
    missing = []
    for i, sl in enumerate(prs.slides, 1):
        for sh in sl.shapes:
            if not sh.has_text_frame:
                continue
            for p in sh.text_frame.paragraphs:
                for r in p.runs:
                    t = r.text
                    if not t.strip():
                        continue
                    if t in DE:
                        r.text = DE[t]
                    elif t not in KEEP and t not in (l1, l2, SUB_DE):
                        if re.search(r"[A-Za-z]{3}", t):
                            missing.append((i, t))
                    if font != "Poppins" and (r.font.name or "") == "Poppins":
                        r.font.name = font

    prs.save(out_path)
    print(f"wrote {out_path}: {len(prs.slides)} slides ({font})")
    for i, t in missing:
        print(f"  UNTRANSLATED slide {i}: {t!r}")
    return missing


if __name__ == "__main__":
    miss = build("Pitch_Deck_AthenaRun_DE.pptx", "Poppins")
    build("AthenaRun_Pitch_Deck_DE_Keynote.pptx", "Helvetica")
    sys.exit(1 if miss else 0)
