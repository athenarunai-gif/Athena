"""Cross-check the chosen body size using cap height, which is independent of
the advance-width differences between Sora versions."""
import numpy as np, pypdfium2 as pdfium
from fontTools.ttLib import TTFont
S=16
orig=pdfium.PdfDocument('/root/.claude/uploads/db740190-8188-5d74-b382-8c526618dace/b1ef59bb-Autohaus_Goebel_Light___AthenaRun_bearbeitet_1.pdf')
a=np.asarray(orig[1].render(scale=S).to_pil().convert('RGB')).astype(int)   # Ausgangslage, unpatched

def glyph_box(x0,x1,y0,y1):
    reg=a[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]
    lum=reg.sum(2); m=lum<lum.max()-90
    ys,xs=np.nonzero(m)
    return (x0+xs.min()/S, y0+ys.min()/S, x0+xs.max()/S, y0+ys.max()/S)

# 'C' of "Cidcar" on line 1, and 'S' of "System" on line 2
C=glyph_box(596.0, 601.8, 370.0, 384.0)
Sb=glyph_box(596.0, 601.8, 384.0, 398.0)
print('orig C  top %.2f bottom %.2f  cap %.2f' % (C[1], C[3], C[3]-C[1]))
print('orig S  top %.2f bottom %.2f  cap %.2f' % (Sb[1], Sb[3], Sb[3]-Sb[1]))

f=TTFont('fonts/Sora-Regular.ttf')
upem=f['head'].unitsPerEm
gs=f.getGlyphSet(); from fontTools.pens.boundsPen import BoundsPen
bp=BoundsPen(gs); gs['uni0043'].draw(bp)          # 'C'
capC=(bp.bounds[3]-bp.bounds[1])/upem
print('Sora C cap/em %.4f' % capC)
for name,box in (('C',C),('S',Sb)):
    print(f'  -> size implied by {name}: {(box[3]-box[1])/capC:.3f} pt')
