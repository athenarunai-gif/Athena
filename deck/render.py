"""Render a pptx to PNGs by walking its real shape tree.

LibreOffice cannot load pptx in this environment, so QA reads the geometry back
out of the saved file instead of trusting the generator. DejaVu stands in for
Arial/Courier and runs wider, so anything that fits here fits in PowerPoint.
"""
import io
import sys

from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.util import Emu

PX = 6350
W, H = 1920, 1080
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
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
                pic = Image.open(io.BytesIO(sh.image.blob)).convert("RGB")
                img.paste(pic.resize((max(1, int(w)), max(1, int(h)))),
                          (int(x), int(y)))
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
                    if total > h + 2:
                        warnings.append(
                            f"slide {idx}: text overflows box "
                            f"({total:.0f}px in {h:.0f}px) — {sh.text_frame.text[:48]!r}")
                    top = y + max(0, (h - total) / 2) + pi * lead
                    for li, ln in enumerate(lines):
                        wl = sum(d.textlength(t, font=f) for t, f, _ in ln)
                        cx = x + (w - wl) if para.alignment == 3 else x
                        if cx + wl > 1880:
                            warnings.append(
                                f"slide {idx}: line runs to x={cx+wl:.0f} — {ln[0][0]!r}")
                        for t, f, col in ln:
                            a = f.getmetrics()[0]
                            d.text((cx, top + li * lead + (asc - a)), t, font=f, fill=col)
                            cx += d.textlength(t, font=f)
                continue
            try:                                          # plain filled rectangle
                c = sh.fill.fore_color.rgb
                d.rectangle([x, y, x + w, y + h], fill=(c[0], c[1], c[2]))
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
