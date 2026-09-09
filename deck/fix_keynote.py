"""Fix the Keynote deck (AthenaRun_short_Pitch_Deck_8.09.key).

1. Slides 10-12 are flat PNG exports (Data/image5-47, image6-51, image7-106)
   carrying baked-in section markers "05 — Market size", "06 — Competitive map",
   "07 — Team". The number prefix is erased from the image, the label stays
   right-aligned, so the three match the unnumbered markers on the native slides.
   The same erase is applied to Keynote's cached -small variants and st-*.jpg
   slide thumbnails so the navigator does not show a stale "05".
   The marker is found as the right-anchored glyph group in the title band
   (gap > 40px separates it from the title); the cut sits after the second
   space ("NN — |Label"). Everything is scale-aware: image7 is a 959x540 export.

2. Variant A (…_fix.key): only Data/* replaced, zip rewritten with the original
   entry order and STORE method -> minimal risk.
   Variant B (…_fix_fonts.key): additionally DocumentStylesheet.iwa fontName
   ArialMT/Arial-BoldMT/Calibri/Calibri-Bold -> Helvetica/Helvetica-Bold, packed
   with keynote-parser (CourierNewPSMT kept for mono labels).

Requires: pip install keynote-parser pillow numpy ; keynote-parser unpack deck.key
"""
import io, os, zipfile
import numpy as np
from PIL import Image, ImageDraw

SRC = "deck.key"
PAIRS = [("image5-47.png", "image5-small-48.png", "st-4F50CDCF-DC26-4D60-A28E-784100A26C9C-44.jpg"),
         ("image6-51.png", "image6-small-52.png", "st-8FBE96AD-0FF4-46BD-9840-353006D8AE5D-49.jpg"),
         ("image7-106.png", "image7-small-107.png", "st-9152466C-2BFF-44B9-A0D3-0AA1A089202A-104.jpg")]
FONTS = {"Arial-BoldMT": "Helvetica-Bold", "ArialMT": "Helvetica",
         "Calibri-Bold": "Helvetica-Bold", "Calibri": "Helvetica"}


def erase_prefix(z, name, small, thumb, outdir):
    im = Image.open(io.BytesIO(z.read("Data/" + name))).convert("RGB")
    W, H = im.size; S = W / 1920.0
    a = np.array(im).astype(int)
    bg = tuple(int(v) for v in np.median(a[int(20*S):int(60*S), int(1400*S):int(1800*S)].reshape(-1, 3), axis=0))
    BX, BY = int(900*S), int(70*S)
    ink = (np.abs(a[BY:int(160*S), BX:int(1840*S)] - np.array(bg)).sum(axis=2) > 40)
    cols = np.where(ink.any(axis=0))[0]
    cl, s, p = [], cols[0], cols[0]
    for c in cols[1:]:
        if c - p > 1: cl.append((s, p)); s = c
        p = c
    cl.append((s, p))
    grp = [cl[-1]]
    for i in range(len(cl) - 2, -1, -1):
        if cl[i+1][0] - cl[i][1] < 40*S: grp.insert(0, cl[i])
        else: break
    x0, x1 = BX + grp[0][0], BX + grp[-1][1]
    rows = np.where(ink[:, grp[0][0]:grp[-1][1]+1].any(axis=1))[0]; y0, y1 = BY + rows.min(), BY + rows.max()
    spaces = [(BX+grp[i][1], BX+grp[i+1][0]) for i in range(len(grp)-1) if grp[i+1][0]-grp[i][1] >= 9*S]
    cut, pad = int(spaces[1][1] - 3*S), int(4*S) + 1
    box = [x0-pad, y0-pad-2, cut, y1+pad+2]
    d = ImageDraw.Draw(im); d.rectangle(box, fill=bg)
    if S > 0.9:                                   # restore the 44px dot grid on full-res exports
        for gx in range(19, W, 44):
            for gy in range(19, H, 44):
                if box[0] <= gx <= box[2] and box[1] <= gy <= box[3]: d.rectangle([gx, gy, gx+1, gy+1], fill=(21, 21, 24))
    im.save(os.path.join(outdir, name))
    for fn in (small, thumb):
        t = Image.open(io.BytesIO(z.read("Data/" + fn))).convert("RGB"); f = t.size[0] / W
        ImageDraw.Draw(t).rectangle([v*f for v in box], fill=bg)
        t.save(os.path.join(outdir, fn), **({"quality": 92} if fn.endswith(".jpg") else {}))
    return box


if __name__ == "__main__":
    z = zipfile.ZipFile(SRC); os.makedirs("patched", exist_ok=True)
    for name, small, thumb in PAIRS:
        print(name, "erased", erase_prefix(z, name, small, thumb, "patched"))
    # variant A: same entries, same order, STORE
    out = zipfile.ZipFile("AthenaRun_short_Pitch_Deck_8.09_fix.key", "w", zipfile.ZIP_STORED)
    for info in z.infolist():
        p = os.path.join("patched", os.path.basename(info.filename))
        out.writestr(info, open(p, "rb").read() if info.filename.startswith("Data/") and os.path.exists(p) else z.read(info.filename))
    out.close()
    # variant B: unpacked dir "deck/" from keynote-parser, fonts unified, then `keynote-parser pack deck -o ..._fix_fonts.key`
    ss = "deck/Index/DocumentStylesheet.iwa.yaml"
    if os.path.exists(ss):
        t = open(ss).read()
        for a, b in FONTS.items(): t = t.replace(f"fontName: {a}", f"fontName: {b}")
        open(ss, "w").write(t)
        for name, small, thumb in PAIRS:
            for fn in (name, small, thumb): os.replace(os.path.join("patched", fn), os.path.join("deck/Data", fn))
        print("stylesheet unified; now run: keynote-parser pack deck -o AthenaRun_short_Pitch_Deck_8.09_fix_fonts.key")
