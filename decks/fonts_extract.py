"""Rebuild usable Sora / Space Mono TTFs from the subsets embedded in the Skizze PDF.

Every page carries its own subset of the original font. The subsets keep the
original glyph IDs, so the union across pages gives a font that covers all text
used anywhere in the deck. Glyphs are re-drawn through a pen (rather than copied
as glyf records) so composites like the umlauts come out as plain contours.
"""
import pypdf, os, re
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.fontBuilder import FontBuilder

SK='/root/.claude/uploads/db740190-8188-5d74-b382-8c526618dace/d87cc5cc-20260723__AthenaRun_Loesungsskizze_DE4.pdf'
os.makedirs('fonts',exist_ok=True)

def tounicode(o):
    m={}
    if '/ToUnicode' not in o: return m
    data=o['/ToUnicode'].get_object().get_data().decode('latin-1')
    for blk in re.findall(r'beginbfchar(.*?)endbfchar', data, re.S):
        for src,dst in re.findall(r'<([0-9a-fA-F]+)>\s*<([0-9a-fA-F]+)>', blk):
            m[int(src,16)]=''.join(chr(int(dst[i:i+4],16)) for i in range(0,len(dst),4))
    for blk in re.findall(r'beginbfrange(.*?)endbfrange', data, re.S):
        for lo,hi,dst in re.findall(r'<([0-9a-fA-F]+)>\s*<([0-9a-fA-F]+)>\s*<([0-9a-fA-F]+)>', blk):
            lo,hi,d=int(lo,16),int(hi,16),int(dst,16)
            for k in range(lo,hi+1): m[k]=chr(d+k-lo)
    return m

def collect():
    r=pypdf.PdfReader(SK); fams={}
    for i,p in enumerate(r.pages):
        fo=p['/Resources'].get('/Font')
        if not fo: continue
        for k,v in fo.items():
            o=v.get_object(); base=str(o['/BaseFont']).split('+')[-1]
            fd=o['/DescendantFonts'][0].get_object()['/FontDescriptor'].get_object()
            path=f'fonts/_{base}_p{i+1}.ttf'
            open(path,'wb').write(fd['/FontFile2'].get_object().get_data())
            fams.setdefault(base,[]).append((path, tounicode(o)))
    return fams

def build(base, lst, out):
    glyphs={'.notdef': TTGlyphPen(None).glyph()}
    widths={'.notdef': 0}
    cmap={}
    upem=None
    for path,tu in lst:
        f=TTFont(path)
        upem=upem or f['head'].unitsPerEm
        order=f.getGlyphOrder(); gs=f.getGlyphSet(); hm=f['hmtx']
        for gid,s in tu.items():
            if len(s)!=1 or gid>=len(order): continue
            u=ord(s)
            if u in cmap: continue
            gname=order[gid]
            if f['glyf'][gname].numberOfContours==0: continue
            rec=DecomposingRecordingPen(gs)
            try: gs[gname].draw(rec)
            except Exception: continue   # composite whose parts this subset lacks
            pen=TTGlyphPen(None); rec.replay(pen)
            nm=f'uni{u:04X}'
            glyphs[nm]=pen.glyph(); widths[nm]=hm[gname][0]; cmap[u]=nm
    fb=FontBuilder(upem, isTTF=True)
    order=['.notdef']+[cmap[u] for u in sorted(cmap)]
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics({g:(widths[g],0) for g in order})
    fb.setupHorizontalHeader(ascent=int(upem*0.8), descent=-int(upem*0.2))
    fb.setupNameTable({'familyName':base,'styleName':'Regular','fullName':base,'psName':base.replace(' ','')})
    fb.setupOS2(sTypoAscender=int(upem*0.8), sTypoDescender=-int(upem*0.2))
    fb.setupPost()
    fb.save(out)
    return set(cmap)

if __name__=='__main__':
    for base,lst in collect().items():
        chars=build(base,lst,f'fonts/{base}.ttf')
        print(f'{base:20s} {len(chars):3d} -> {"".join(sorted(chr(c) for c in chars))}')
