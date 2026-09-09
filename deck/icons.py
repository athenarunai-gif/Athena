"""Line icons for the deck, drawn at 4x and downscaled, transparent RGBA."""
from PIL import Image, ImageDraw

MUTED = (154, 154, 162, 255)
ORANGE = (255, 107, 61, 255)


def _canvas():
    return Image.new("RGBA", (128, 128), (0, 0, 0, 0))


def _save(img, name, size):
    img.resize((size, size), Image.LANCZOS).save(name)


def handoff(name, size=28, col=MUTED):
    im = _canvas(); d = ImageDraw.Draw(im)
    d.line([(20, 44), (100, 44)], fill=col, width=8)
    d.polygon([(112, 44), (90, 30), (90, 58)], fill=col)
    d.line([(28, 84), (108, 84)], fill=col, width=8)
    d.polygon([(16, 84), (38, 70), (38, 98)], fill=col)
    _save(im, name, size)


def doc(name, size=28, col=MUTED):
    im = _canvas(); d = ImageDraw.Draw(im)
    d.line([(28, 16), (80, 16), (100, 36), (100, 112), (28, 112), (28, 16)],
           fill=col, width=8, joint="curve")
    d.line([(80, 16), (80, 36), (100, 36)], fill=col, width=6)
    d.line([(44, 66), (84, 66)], fill=col, width=6)
    d.line([(44, 88), (84, 88)], fill=col, width=6)
    _save(im, name, size)


def wait(name, size=28, col=MUTED):
    im = _canvas(); d = ImageDraw.Draw(im)
    d.ellipse([16, 16, 112, 112], outline=col, width=8)
    d.line([(64, 64), (64, 34)], fill=col, width=8)
    d.line([(64, 64), (88, 74)], fill=col, width=8)
    _save(im, name, size)


def chart(name, size=36, col=MUTED):
    im = _canvas(); d = ImageDraw.Draw(im)
    d.line([(20, 108), (108, 108)], fill=col, width=8)
    d.rectangle([30, 66, 48, 100], outline=col, width=7)
    d.rectangle([56, 40, 74, 100], outline=col, width=7)
    d.rectangle([82, 76, 100, 100], outline=col, width=7)
    _save(im, name, size)


def funnel(name, size=36, col=MUTED):
    im = _canvas(); d = ImageDraw.Draw(im)
    d.line([(20, 24), (108, 24)], fill=col, width=8)
    d.line([(20, 24), (56, 70)], fill=col, width=8)
    d.line([(108, 24), (72, 70)], fill=col, width=8)
    d.line([(56, 70), (56, 108)], fill=col, width=8)
    d.line([(72, 70), (72, 108)], fill=col, width=8)
    _save(im, name, size)


def bubble(name, size=36, col=MUTED):
    im = _canvas(); d = ImageDraw.Draw(im)
    d.rounded_rectangle([16, 22, 112, 86], radius=18, outline=col, width=8)
    d.polygon([(38, 84), (34, 110), (62, 84)], fill=col)
    _save(im, name, size)


def learn_arc(name, w=1180, h=170, col=ORANGE):
    """Downward bow from right back to left, arrowhead at the left end."""
    S = 3
    im = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pad = 14 * S
    d.arc([pad, -h * S, w * S - pad, h * S - 8 * S], start=20, end=160,
          fill=col, width=3 * S)
    import math
    # arc endpoint at 160deg of that ellipse
    cx, cy = w * S / 2, (-h * S + h * S - 8 * S) / 2
    rx, ry = (w * S - 2 * pad) / 2, (h * S - 8 * S - (-h * S)) / 2
    ax = cx + rx * math.cos(math.radians(160))
    ay = cy + ry * math.sin(math.radians(160))
    d.polygon([(ax - 10 * S, ay - 2 * S), (ax + 14 * S, ay - 14 * S),
               (ax + 10 * S, ay + 12 * S)], fill=col)
    im.resize((w, h), Image.LANCZOS).save(name)


def person(name, size=36, col=MUTED, cx=64):
    im = _canvas(); d = ImageDraw.Draw(im)
    d.ellipse([cx - 20, 24, cx + 20, 64], outline=col, width=8)
    d.arc([cx - 34, 72, cx + 34, 140], start=180, end=360, fill=col, width=8)
    _save(im, name, size)


def people(name, size=36, col=MUTED):
    im = _canvas(); d = ImageDraw.Draw(im)
    for cx, r in ((30, 13), (98, 13)):          # two behind
        d.ellipse([cx - r, 30, cx + r, 30 + 2 * r], outline=col, width=7)
        d.arc([cx - 24, 62, cx + 24, 110], start=180, end=360, fill=col, width=7)
    d.ellipse([46, 20, 82, 56], outline=col, width=8)
    d.arc([34, 62, 94, 122], start=180, end=360, fill=col, width=8)
    _save(im, name, size)


def layers(name, size=36, col=MUTED):
    im = _canvas(); d = ImageDraw.Draw(im)
    for dy in (0, 38, 76):
        d.polygon([(64, 18 + dy), (110, 34 + dy), (64, 50 + dy), (18, 34 + dy)],
                  outline=col, width=7)
    _save(im, name, size)


# --- stage / phase glyphs, all drawn on the same 128px grid ---------------
def chat(name, size=40, col=MUTED):
    im = _canvas(); d = ImageDraw.Draw(im)
    d.rounded_rectangle([16, 24, 112, 88], radius=16, outline=col, width=8)
    d.polygon([(38, 86), (34, 112), (62, 86)], fill=col)
    _save(im, name, size)


def search(name, size=40, col=MUTED):
    im = _canvas(); d = ImageDraw.Draw(im)
    d.ellipse([20, 20, 88, 88], outline=col, width=8)
    d.line([(84, 84), (110, 110)], fill=col, width=10)
    _save(im, name, size)


def book(name, size=40, col=MUTED):
    im = _canvas(); d = ImageDraw.Draw(im)
    d.line([(64, 34), (64, 104)], fill=col, width=8)
    d.line([(64, 34), (20, 26), (20, 96), (64, 104)], fill=col, width=8, joint="curve")
    d.line([(64, 34), (108, 26), (108, 96), (64, 104)], fill=col, width=8, joint="curve")
    _save(im, name, size)


def shield(name, size=40, col=MUTED):
    im = _canvas(); d = ImageDraw.Draw(im)
    d.line([(64, 16), (108, 34), (108, 70), (64, 112), (20, 70), (20, 34), (64, 16)],
           fill=col, width=8, joint="curve")
    d.line([(44, 62), (60, 78), (88, 46)], fill=col, width=9, joint="curve")
    _save(im, name, size)


def database(name, size=40, col=MUTED):
    im = _canvas(); d = ImageDraw.Draw(im)
    d.ellipse([20, 16, 108, 48], outline=col, width=8)
    d.line([(20, 32), (20, 96)], fill=col, width=8)
    d.line([(108, 32), (108, 96)], fill=col, width=8)
    d.arc([20, 80, 108, 112], start=0, end=180, fill=col, width=8)
    d.arc([20, 48, 108, 80], start=0, end=180, fill=col, width=8)
    _save(im, name, size)


def code(name, size=40, col=MUTED):
    im = _canvas(); d = ImageDraw.Draw(im)
    d.line([(46, 30), (14, 64), (46, 98)], fill=col, width=9, joint="curve")
    d.line([(82, 30), (114, 64), (82, 98)], fill=col, width=9, joint="curve")
    _save(im, name, size)


def ship(name, size=40, col=MUTED):
    im = _canvas(); d = ImageDraw.Draw(im)
    d.line([(64, 108), (64, 34)], fill=col, width=9)
    d.polygon([(64, 14), (92, 46), (36, 46)], fill=col)
    d.line([(20, 112), (108, 112)], fill=col, width=8)
    _save(im, name, size)


def gauge(name, size=40, col=MUTED):
    im = _canvas(); d = ImageDraw.Draw(im)
    d.arc([16, 30, 112, 126], start=180, end=360, fill=col, width=8)
    d.line([(64, 78), (92, 50)], fill=col, width=9)
    d.ellipse([57, 71, 71, 85], fill=col)
    _save(im, name, size)


def target(name, size=40, col=MUTED):
    im = _canvas(); d = ImageDraw.Draw(im)
    d.ellipse([16, 16, 112, 112], outline=col, width=8)
    d.ellipse([44, 44, 84, 84], outline=col, width=8)
    d.ellipse([58, 58, 70, 70], fill=col)
    _save(im, name, size)


def layout(name, size=40, col=MUTED):
    im = _canvas(); d = ImageDraw.Draw(im)
    d.rectangle([18, 22, 110, 106], outline=col, width=8)
    d.line([(18, 54), (110, 54)], fill=col, width=8)
    d.line([(62, 54), (62, 106)], fill=col, width=8)
    _save(im, name, size)


def checklist(name, size=40, col=MUTED):
    im = _canvas(); d = ImageDraw.Draw(im)
    d.rectangle([24, 20, 104, 110], outline=col, width=8)
    d.line([(40, 52), (52, 64), (86, 34)], fill=col, width=8, joint="curve")
    d.line([(40, 84), (88, 84)], fill=col, width=7)
    _save(im, name, size)


def refresh(name, size=40, col=MUTED):
    im = _canvas(); d = ImageDraw.Draw(im)
    d.arc([20, 20, 108, 108], start=40, end=300, fill=col, width=8)
    d.polygon([(96, 20), (116, 46), (84, 50)], fill=col)
    _save(im, name, size)


def window(name, size=40, col=MUTED):
    im = _canvas(); d = ImageDraw.Draw(im)
    d.rounded_rectangle([14, 22, 114, 100], radius=10, outline=col, width=8)
    d.line([(14, 46), (114, 46)], fill=col, width=7)
    d.polygon([(60, 58), (60, 96), (86, 80)], fill=col)
    _save(im, name, size)


def build_all():
    handoff("ic-handoff.png"); doc("ic-doc.png"); wait("ic-wait.png")
    chart("ic-chart.png"); funnel("ic-funnel.png"); bubble("ic-bubble.png")
    learn_arc("ic-arc.png")
    people("ic-people.png"); person("ic-person.png"); layers("ic-layers.png")
    person("ic-person-orange.png", col=ORANGE)
    chat("ic-chat.png"); search("ic-search.png"); book("ic-book.png")
    shield("ic-shield.png"); database("ic-db.png"); code("ic-code.png")
    ship("ic-ship.png"); gauge("ic-gauge.png"); target("ic-target.png")
    layout("ic-layout.png"); checklist("ic-checklist.png")
    refresh("ic-refresh.png"); window("ic-window.png")
    person("ic-person-node.png", size=40)


if __name__ == "__main__":
    build_all()
    print("icons written")
