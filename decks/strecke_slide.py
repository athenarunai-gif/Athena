"""Build the "Vom Bestand zum Termin" pipeline slide in the deck's visual language.

Geometry and palette were measured off the existing Goebel slides, so the new
page shares their margins, type sizes, rule positions and background grid.
"""
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

W, H = 959.0, 540.0
FONTS='fonts'
for n in ('Sora-Regular','Sora-Medium','Sora-SemiBold','SpaceMono-Regular'):
    pdfmetrics.registerFont(TTFont(n, f'{FONTS}/{n}.ttf'))

BG      = HexColor('#FAF7F1')
DOT     = HexColor('#F2EFE9')
RULE    = HexColor('#E5E3DC')
INK     = HexColor('#1F1E1C')
MUTED   = HexColor('#6E6862')
GREY    = HexColor('#A9A59B')
ACCENT  = HexColor('#DD653E')
PANEL   = HexColor('#EFE9DF')
LOOP    = HexColor('#D8D4CB')

ML, MR = 55.5, 903.5            # content margins
GRID, PHASE, DOTR = 22.0, 9.88, 0.75

def y(v):  # measurements are top-down, reportlab is bottom-up
    return H - v

def track_width(txt, font, size, cs):
    return pdfmetrics.stringWidth(txt, font, size) + cs*max(len(txt)-1, 0)

def text(c, x, ytop, txt, font, size, colour, cs=0.0, align='left'):
    w = track_width(txt, font, size, cs)
    if align=='center': x -= w/2
    elif align=='right': x -= w
    t=c.beginText(x, y(ytop))
    t.setFont(font, size); t.setFillColor(colour); t.setCharSpace(cs)
    t.textOut(txt)
    c.drawText(t)

def background(c):
    c.setFillColor(BG); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(DOT)
    gy = PHASE
    while gy < H:
        gx = PHASE
        while gx < W:
            c.circle(gx, y(gy), DOTR, stroke=0, fill=1)
            gx += GRID
        gy += GRID

def arrow(c, cx, cy, size=6.5):
    """Small solid arrow head pointing right, matching the deck's inline arrows."""
    c.setStrokeColor(ACCENT); c.setLineWidth(1.1)
    c.line(cx-size, y(cy), cx+size*0.15, y(cy))
    c.setFillColor(ACCENT)
    p=c.beginPath()
    p.moveTo(cx+size*0.9, y(cy)); p.lineTo(cx-size*0.1, y(cy)-size*0.52)
    p.lineTo(cx-size*0.1, y(cy)+size*0.52); p.close()
    c.drawPath(p, stroke=0, fill=1)

STEPS=[('Anbinden',''),
       ('Bereinigen','Dubletten, Adressen'),
       ('Anlass','Finanzierung, Service'),
       ('Auswahl','mit Begründung'),
       ('Freigabe','Mensch entscheidet'),
       ('Ansprache','Mail, Telefon'),
       ('Rückfluss','Ergebnis ins System')]
GROUPS=[('BESTAND ZU ANLASS', 0, 3), ('ANLASS ZU TERMIN', 4, 6)]

GAP   = 14.0
BOXW  = (MR-ML - GAP*(len(STEPS)-1)) / len(STEPS)
BOXT, BOXH, BAR = 244.0, 64.0, 2.6
LOOPY, CAPY = 378.0, 382.0
GRPY, GRPRULE = 200.0, 212.0

def centre(i): return ML + i*(BOXW+GAP) + BOXW/2

def build(path, corner='07 — Strecke'):
    c=canvas.Canvas(path, pagesize=(W,H))
    background(c)

    text(c, ML,  52.25, 'DIE STRECKE · ENDE ZU ENDE', 'SpaceMono-Regular', 7.0, ACCENT, cs=1.75)
    text(c, ML,  82.00, 'Vom Bestand zum Termin',     'Sora-SemiBold',    21.0, INK)
    text(c, MR,  84.75, corner,                       'SpaceMono-Regular', 8.0, GREY, cs=1.55, align='right')
    c.setStrokeColor(RULE); c.setLineWidth(0.6)
    c.line(ML, y(103), MR, y(103))

    # group headers
    for label, a, b in GROUPS:
        x0, x1 = ML + a*(BOXW+GAP), ML + b*(BOXW+GAP) + BOXW
        text(c, (x0+x1)/2, GRPY, label, 'SpaceMono-Regular', 7.0, GREY, cs=1.7, align='center')
        c.setStrokeColor(RULE); c.setLineWidth(0.6)
        c.line(x0, y(GRPRULE), x1, y(GRPRULE))

    # step boxes
    for i,(title, sub) in enumerate(STEPS):
        x0 = ML + i*(BOXW+GAP)
        c.setFillColor(PANEL); c.rect(x0, y(BOXT+BOXH), BOXW, BOXH, stroke=0, fill=1)
        c.setFillColor(ACCENT); c.rect(x0, y(BOXT+BAR), BOXW, BAR, stroke=0, fill=1)
        text(c, x0+BOXW/2, BOXT+29.0, title, 'Sora-SemiBold', 11.5, INK,   align='center')
        if sub:   # keep the titles on one baseline across the row
            text(c, x0+BOXW/2, BOXT+47.0, sub, 'Sora-Regular', 7.0, MUTED, align='center')
        if i < len(STEPS)-1:
            arrow(c, x0+BOXW+GAP/2, BOXT+BOXH/2+1)

    # learning loop: Rückfluss back into Anbinden
    xa, xz = centre(0), centre(len(STEPS)-1)
    cap='Lernen: jeder Durchlauf verbessert den nächsten'
    cw=pdfmetrics.stringWidth(cap,'Sora-Medium',9.5)
    c.setStrokeColor(LOOP); c.setLineWidth(0.9); c.setLineCap(0)
    c.line(xz, y(BOXT+BOXH), xz, y(LOOPY))
    c.line(xz, y(LOOPY), W/2+cw/2+18, y(LOOPY))
    c.line(W/2-cw/2-18, y(LOOPY), xa, y(LOOPY))
    c.line(xa, y(LOOPY), xa, y(BOXT+BOXH+7))
    p=c.beginPath()                                   # head into the first box
    p.moveTo(xa, y(BOXT+BOXH)); p.lineTo(xa-3.4, y(BOXT+BOXH+6.4)); p.lineTo(xa+3.4, y(BOXT+BOXH+6.4)); p.close()
    c.setFillColor(ACCENT); c.drawPath(p, stroke=0, fill=1)
    text(c, W/2, CAPY, cap, 'Sora-Medium', 9.5, INK, align='center')

    c.showPage(); c.save()

if __name__=='__main__':
    build('strecke.pdf'); print('ok')
