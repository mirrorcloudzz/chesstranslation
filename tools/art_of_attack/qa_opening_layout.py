import json
import re
from pathlib import Path
import pdfplumber
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[2]
PROJECT=ROOT/'translations/art_of_attack'
QA=ROOT/'tmp/pdfs/art_of_attack_opening'
manifest=json.loads((PROJECT/'translation/proof_manifest_v1.json').read_text(encoding='utf-8'))
items=json.loads((PROJECT/'translation/segments_v1.json').read_text(encoding='utf-8'))
reports=[]
for config in manifest:
    doc=pdfplumber.open(config['path'])
    pages=doc.pages
    prefix={'front_preface':'front','introduction':'intro','ch01':'ch01'}[config['section']]
    paths=sorted(QA.glob(prefix+'-*.png'))
    # Exclude manually enlarged scan-detail images, which use a different prefix.
    assert len(paths)==len(pages),(prefix,len(paths),len(pages))
    for offset in range(0,len(paths),9):
        group=paths[offset:offset+9]
        canvas=Image.new('RGB',(1200,1780),'#e3e7ea')
        draw=ImageDraw.Draw(canvas)
        for j,path in enumerate(group):
            im=Image.open(path).convert('RGB')
            im.thumbnail((380,548))
            x=10+(j%3)*400;y=30+(j//3)*590
            canvas.paste(im,(x,y))
            draw.text((x,y-20),f'{prefix} / page {offset+j+1}',fill='black')
        canvas.save(QA/f'{prefix}-contact-{offset+1:02}.jpg',quality=94)
    text_by_page=[p.extract_text() for p in pages]
    overflow=[]
    for n,p in enumerate(pages,1):
        for char in p.chars:
            x0,y0,x1,y1=char['x0'],char['top'],char['x1'],char['bottom']
            if x0<30 or x1>p.width-30 or y0<10 or y1>p.height-10:
                overflow.append({'page':n,'bbox':[x0,y0,x1,y1]})
    selected=[s for s in items if s['section']==config['section']]
    figs=[]
    for i,s in enumerate(selected):
        if not s.get('figure_id'):continue
        pfig=next(n for n,t in enumerate(text_by_page,1) if s['figure_id'] in t)
        panchor=next(n for n,t in enumerate(text_by_page,1) if s['segment_id']+' ·' in t)
        following=selected[i+1]['segment_id'] if i+1<len(selected) else s['segment_id']
        pnext=next(n for n,t in enumerate(text_by_page,1) if following+' ·' in t)
        figs.append({'figure':s['figure_id'],'page':pfig,'anchor_page':panchor,'next_segment_page':pnext,
                     'kept_with_context':pfig==panchor==pnext})
    r={'section':config['section'],'pages':len(pages),'overflow':overflow,'figures':figs,
       'images':sum(len(p.images) for p in pages)}
    reports.append(r)
(PROJECT/'translation/layout_validation_v1.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(reports,ensure_ascii=False,indent=2))
