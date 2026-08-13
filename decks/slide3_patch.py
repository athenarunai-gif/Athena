"""Replace the bullet-03 body text on the Ausgangslage slide.

The slide is a flat raster, so the old two lines are painted over with the
background (grid dots restored) and re-set in Sora at the size, colour,
baseline and left edge measured off the surrounding, untouched paragraphs.
"""
import io, pypdf
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

W, H = 959.0, 540.0
BG, INK = HexColor('#FAF7F1'), HexColor('#736D68')
DOT, GRID, PHASE, DOTR = HexColor('#F2EFE9'), 22.0, 9.88, 0.75

X0, BASE1, LEADING = 596.0, 379.2, 14.0   # left edge, first baseline, line pitch
SIZE, WRAP = 8.95, 205.0
FONT='Sora-Regular'
WIPE=(593.0, 368.0, 806.0, 398.5)         # x0, ytop, x1, ybot

TEXT='Cidcar, Bestellsysteme, Excel — kein System hat das vollständige Bild.'

def wrap(txt, font, size, width):
    lines, cur = [], ''
    for word in txt.split(' '):
        trial = f'{cur} {word}'.strip()
        if cur and pdfmetrics.stringWidth(trial, font, size) > width:
            lines.append(cur); cur = word
        else:
            cur = trial
    if cur: lines.append(cur)
    return lines

def overlay_page(fontdir='fonts'):
    pdfmetrics.registerFont(TTFont(FONT, f'{fontdir}/{FONT}.ttf'))
    buf=io.BytesIO(); c=canvas.Canvas(buf, pagesize=(W,H))
    x0,yt,x1,yb = WIPE
    c.setFillColor(BG); c.rect(x0, H-yb, x1-x0, yb-yt, stroke=0, fill=1)

    c.setFillColor(DOT)                                  # put the grid dots back
    gy = PHASE
    while gy < H:
        if yt <= gy <= yb:
            gx = PHASE
            while gx < W:
                if x0 <= gx <= x1: c.circle(gx, H-gy, DOTR, stroke=0, fill=1)
                gx += GRID
        gy += GRID

    c.setFillColor(INK); c.setFont(FONT, SIZE)
    for i, line in enumerate(wrap(TEXT, FONT, SIZE, WRAP)):
        c.drawString(X0, H-(BASE1 + i*LEADING), line)
    c.save(); buf.seek(0)
    return pypdf.PdfReader(buf).pages[0]

if __name__=='__main__':
    print(wrap(TEXT, FONT, SIZE, WRAP)) if pdfmetrics.registerFont(TTFont(FONT,f'fonts/{FONT}.ttf')) is None else None
