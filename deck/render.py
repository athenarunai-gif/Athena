"""Render a pptx to PNGs by walking its real shape tree.

LibreOffice cannot load pptx in this environment, so QA reads the geometry back
out of the saved file instead of trusting the generator. Poppins is the real
display face, so text metrics here match PowerPoint; Courier stands in for the
mono labels and runs slightly wider.
"""
import io
import math
import sys

from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.util import Emu

PX = 6350
W, H = 1920, 1080
SANS = "fonts/Poppins-Regular.ttf"
SANS_B = "fonts/Poppins-SemiBold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

warnings = []


def font_for(r):
    name = (r.font.name or "Arial").lower()
    size = int((r.font.size.pt if r.font.size else 12) * 2)
    path = MONO if "courier" in name else (SANS_B if r.font.bold else SANS)
    return ImageFont.truetype(path, size)


def colour_of(r, default=(236, 236, 238)):
    try:
        c = r.font.color.rgb
        return (c[0], c[1], c[2])
    except Exception:
        return default


def render(path, out_prefix):
    prs = Presentation(path)
    for idx, slide in enumerate(prs.slides, 1):
        img = Image.new("RGB", (W, H), (14, 14, 17))
        d = ImageDraw.Draw(img)
        for sh in slide.shapes:
            x, y = sh.left / PX, sh.top / PX
            w, h = sh.width / PX, sh.height / PX
            if sh.shape_type == 13:                       # picture
                pic = Image.open(io.BytesIO(sh.image.blob)).convert("RGBA")
                pic = pic.resize((max(1, int(w)), max(1, int(h))))
                img.paste(pic, (int(x), int(y)), pic)
                continue
            if sh.has_text_frame and sh.text_frame.text.strip():
                tf = sh.text_frame
                for pi, para in enumerate(tf.paragraphs):
                    runs = [r for r in para.runs if r.text]
                    if not runs:
                        continue
                    fonts = [font_for(r) for r in runs]
                    asc = max(f.getmetrics()[0] for f in fonts)
                    dsc = max(f.getmetrics()[1] for f in fonts)
                    lead = (para.line_spacing.pt * 2
                            if para.line_spacing else asc + dsc)
                    # wrap the concatenated runs into lines of width w
                    lines, cur, curw = [], [], 0.0
                    for r, f in zip(runs, fonts):
                        for word in r.text.replace("\n", " ").split(" "):
                            if not word:
                                continue
                            tok = word + " "
                            tw = d.textlength(tok, font=f)
                            if curw + tw > w and cur:
                                lines.append(cur)
                                cur, curw = [], 0.0
                            cur.append((tok, f, colour_of(r)))
                            curw += tw
                    if cur:
                        lines.append(cur)
                    total = lead * len(lines)
                    if len(lines) > 1 and total > h + 2:
                        warnings.append(
                            f"slide {idx}: text overflows box "
                            f"({total:.0f}px in {h:.0f}px) — {sh.text_frame.text[:48]!r}")
                    top = y + max(0, (h - total) / 2) + pi * lead
                    for li, ln in enumerate(lines):
                        wl = sum(d.textlength(t, font=f) for t, f, _ in ln)
                        if para.alignment == 3:
                            cx = x + (w - wl)
                        elif para.alignment == 2:
                            cx = x + (w - wl) / 2
                        else:
                            cx = x
                        if cx + wl > 1880:
                            warnings.append(
                                f"slide {idx}: line runs to x={cx+wl:.0f} — {ln[0][0]!r}")
                        for t, f, col in ln:
                            a = f.getmetrics()[0]
                            d.text((cx, top + li * lead + (asc - a)), t, font=f, fill=col)
                            cx += d.textlength(t, font=f)
                continue
            try:
                try:
                    st = int(sh.auto_shape_type)   # OVAL=9, DIAMOND=4
                except Exception:
                    st = int(sh.shape_type)
                rot = sh.rotation or 0

                def spin(pts):
                    if not rot:
                        return pts
                    a = math.radians(rot)
                    ox, oy = x + w / 2, y + h / 2
                    return [(ox + (px - ox) * math.cos(a) - (py - oy) * math.sin(a),
                             oy + (px - ox) * math.sin(a) + (py - oy) * math.cos(a))
                            for px, py in pts]

                if st == 7:                               # isosceles triangle
                    c = sh.fill.fore_color.rgb
                    d.polygon(spin([(x + w/2, y), (x + w, y + h), (x, y + h)]),
                              fill=(c[0], c[1], c[2]))
                elif st == 9:                             # oval
                    fc = sh.fill.fore_color.rgb
                    lc = sh.line.color.rgb
                    lw = max(1, int((sh.line.width.pt if sh.line.width else 1) * 2))
                    d.ellipse([x, y, x + w, y + h],
                              fill=(fc[0], fc[1], fc[2]),
                              outline=(lc[0], lc[1], lc[2]), width=lw)
                elif st == 4:                             # diamond
                    c = sh.fill.fore_color.rgb
                    d.polygon([(x + w/2, y), (x + w, y + h/2),
                               (x + w/2, y + h), (x, y + h/2)],
                              fill=(c[0], c[1], c[2]))
                else:
                    try:
                        c = sh.fill.fore_color.rgb
                        fill = (c[0], c[1], c[2])
                    except Exception:
                        fill = None
                    try:
                        lc = sh.line.color.rgb
                        outline = (lc[0], lc[1], lc[2])
                    except Exception:
                        outline = None
                    d.polygon(spin([(x, y), (x + w, y), (x + w, y + h), (x, y + h)]),
                              fill=fill, outline=outline)
            except Exception:
                pass
        img.save(f"{out_prefix}-{idx:02d}.png")
    return len(prs.slides._sldIdLst)


if __name__ == "__main__":
    n = render(sys.argv[1], sys.argv[2])
    print(f"rendered {n} slides")
    for line in warnings:
        print("  WARN", line)
    if not warnings:
        print("  no overflow warnings")
