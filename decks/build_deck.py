"""Merge Autohaus Goebel deck with two slides from the AthenaRun Loesungsskizze
and renumber the corner slide labels so they stay consecutive."""
import io, numpy as np
from PIL import Image
import pypdfium2 as pdfium, pypdf
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

SRC='/root/.claude/uploads/db740190-8188-5d74-b382-8c526618dace'
GB=f'{SRC}/b1ef59bb-Autohaus_Goebel_Light___AthenaRun_bearbeitet_1.pdf'
SK=f'{SRC}/d87cc5cc-20260723__AthenaRun_Loesungsskizze_DE4.pdf'
S=4  # render scale: pages are 959x540 / 960x540 pt -> exactly 4 px/pt

_docs={}
def doc(p):
    if p not in _docs: _docs[p]=pdfium.PdfDocument(p)
    return _docs[p]

def render(pdf, idx):
    return doc(pdf)[idx].render(scale=S).to_pil().convert('RGB')

def find_label(arr, W):
    """Locate the corner label: bbox + the x-groups of its glyphs."""
    xlo, xhi, ytop, ybot = int(W*0.78), W, 200, 480
    reg=arr[ytop:ybot, xlo:xhi]; lum=reg.sum(2)
    bg=np.percentile(lum,92)
    ys,xs=np.nonzero(lum<bg-90)
    box=(xlo+xs.min(), ytop+ys.min(), xlo+xs.max(), ytop+ys.max())
    x0,y0,x1,y1=box; pad=6
    band=arr[y0-pad:y1+pad, x0-pad:x1+pad]
    blum=band.sum(2); bink=blum < np.percentile(blum,95)-90
    col=bink.sum(0); groups=[]; cur=None
    for i,v in enumerate(col):
        if v>0 and cur is None: cur=i
        elif v==0 and cur is not None: groups.append((cur+x0-pad, i+x0-pad)); cur=None
    if cur is not None: groups.append((cur+x0-pad, x1+pad))
    return box, groups

def digit_slot(arr, gx0, gx1, y0, y1):
    """Tight ink bbox of one digit plus the local background / ink colours."""
    pad=8
    sub=arr[y0-pad:y1+pad, gx0-3:gx1+3]
    lum=sub.sum(2)
    bg_lum=np.percentile(lum,90)
    ink=lum < bg_lum-60
    ys,xs=np.nonzero(ink)
    ty0, ty1 = y0-pad+ys.min(), y0-pad+ys.max()+1
    tx0, tx1 = gx0-3+xs.min(), gx0-3+xs.max()+1
    bg=np.array([np.percentile(arr[y0-pad:y1+pad, gx0-3:gx1+3,c],90) for c in range(3)])
    core=arr[ty0:ty1, tx0:tx1]
    dark=core.sum(2)
    fg=core[dark <= np.percentile(dark,8)].mean(0)
    return (tx0,ty0,tx1,ty1), bg, fg

def alpha_of(arr, box, bg, fg):
    """Per-pixel ink coverage of a glyph region, un-compositing bg/fg."""
    tx0,ty0,tx1,ty1=box
    px=arr[ty0:ty1, tx0:tx1]
    denom=(bg-fg)
    denom[np.abs(denom)<1e-6]=1e-6
    a=((bg-px)/denom).mean(2)
    return np.clip(a,0,1)

# ---------------------------------------------------------------- glyph library
GLYPHS={}
def learn(pdf, idx, W, digits):
    im=render(pdf,idx); arr=np.asarray(im).astype(float)
    box,groups=find_label(arr,W)
    y0,y1=box[1],box[3]
    for k,d in enumerate(digits):
        if d is None: continue
        gb,bg,fg=digit_slot(arr, groups[k][0], groups[k][1], y0, y1)
        GLYPHS[d]=alpha_of(arr, gb, bg, fg)

learn(GB,1,3836,[None,'2'])  # "02 - Ausgangslage"
learn(GB,2,3836,[None,'3'])  # "03 - Agenda"
learn(GB,5,3836,['0','6'])   # "06 - Nutzen"
learn(GB,6,3836,[None,'7'])  # "07 - Reaktivierung"
learn(GB,7,3836,[None,'8'])  # "08 - Schwarzbuch"
learn(GB,8,3836,[None,'9'])  # "09 - Konditionen"
learn(SK,9,3840,['1',None])  # "10 - Naechste Schritte"

# ------------------------------------------------------------------- patching
def patch_number(pdf, idx, W, new_digits):
    """Return (PIL patch image, rect in PDF points) replacing the label's digits."""
    im=render(pdf,idx); arr=np.asarray(im).astype(float)
    box,groups=find_label(arr,W)
    y0,y1=box[1],box[3]
    slots=[digit_slot(arr, groups[k][0], groups[k][1], y0, y1) for k in (0,1)]
    bg=slots[0][1]; fg=slots[0][2]

    m=10  # margin around the patch, in 4x pixels
    px0=min(s[0][0] for s in slots)-m; px1=max(s[0][2] for s in slots)+m
    py0=min(s[0][1] for s in slots)-m; py1=max(s[0][3] for s in slots)+m
    region=arr[py0:py1, px0:px1].copy()

    for (gb,_,_), nd in zip(slots, new_digits):
        tx0,ty0,tx1,ty1=gb
        # wipe the old glyph (plus its antialiasing fringe) back to plain background
        e=3
        region[ty0-py0-e:ty1-py0+e, tx0-px0-e:tx1-px0+e]=bg
        if nd is None: continue
        g=GLYPHS[nd]
        gh,gw=g.shape
        # baseline-align (digits share a common baseline) and left-align
        by0=ty1-gh-py0; bx0=tx0-px0
        tgt=region[by0:by0+gh, bx0:bx0+gw]
        a=g[...,None]
        region[by0:by0+gh, bx0:bx0+gw]=tgt*(1-a)+fg*a

    patch=Image.fromarray(np.clip(region,0,255).astype('uint8'))
    H=2160
    rect=(px0/S, (H-py1)/S, (px1-px0)/S, (py1-py0)/S)   # x, y, w, h in points
    return patch, rect

def overlay(page_w, page_h, patch, rect):
    buf=io.BytesIO()
    c=canvas.Canvas(buf, pagesize=(page_w, page_h))
    c.drawImage(ImageReader(patch), rect[0], rect[1], rect[2], rect[3])
    c.save(); buf.seek(0)
    return pypdf.PdfReader(buf).pages[0]

# ------------------------------------------------------------------- assemble
# (source pdf, page index, page width pt, new two-digit number or None)
PLAN=[
    (GB,0,959,None),          # 1  title
    (GB,2,959,'02'),          # 2  Agenda        (war Folie 3)
    (GB,1,959,'03'),          # 3  Ausgangslage  (war Folie 2)
    (GB,3,959,None),          # 4  04 Reaktivierung
    (GB,4,959,None),          # 5  05 Reaktivierung
    (SK,4,960,'06'),          # 6  <- Skizze S.5  Telefon-Agent
    (GB,5,959,'07'),          # 7  Nutzen
    (GB,6,959,'08'),          # 8  Werthebel
    (GB,7,959,'09'),          # 9  Schwarzbuch
    (GB,8,959,'10'),          # 10 Konditionen
]

TARGET_W, TARGET_H = 959.0, 540.0   # the Goebel deck's page box

readers={GB:pypdf.PdfReader(GB), SK:pypdf.PdfReader(SK)}
writer=pypdf.PdfWriter()
for pdf,idx,W,num in PLAN:
    page=readers[pdf].pages[idx]
    if num:
        patch,rect=patch_number(pdf, idx, W*S, list(num))
        page.merge_page(overlay(float(page.mediabox.width), float(page.mediabox.height), patch, rect))
    # give every slide the same page box so viewers don't rescale between slides
    pw, ph = float(page.mediabox.width), float(page.mediabox.height)
    if (pw, ph) != (TARGET_W, TARGET_H):
        page.add_transformation(pypdf.Transformation().scale(TARGET_W/pw, TARGET_H/ph))
        page.mediabox=pypdf.generic.RectangleObject([0,0,TARGET_W,TARGET_H])
        for k in ('/CropBox','/TrimBox','/BleedBox','/ArtBox'):
            if k in page: del page[k]
    writer.add_page(page)

writer.add_metadata({'/Title':'Autohaus Göbel × AthenaRun','/Producer':'pypdf'})
out='/tmp/claude-0/-home-user-Athena/db740190-8188-5d74-b382-8c526618dace/scratchpad/Autohaus_Goebel_AthenaRun.pdf'
with open(out,'wb') as fh: writer.write(fh)
print('written', out)
