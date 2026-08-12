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


def build_all():
    handoff("ic-handoff.png"); doc("ic-doc.png"); wait("ic-wait.png")
    chart("ic-chart.png"); funnel("ic-funnel.png"); bubble("ic-bubble.png")
    learn_arc("ic-arc.png")


if __name__ == "__main__":
    build_all()
    print("icons written")
