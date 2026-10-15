"""Render all four chapter proofs and verify text, bounds and diagram anchors."""
import json,re,subprocess,concurrent.futures,sys
from pathlib import Path
import pdfplumber
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
PROJECT=ROOT/'translations/art_of_attack'
QA=ROOT/'tmp/pdfs/art_of_attack_ch02_05'
QA.mkdir(parents=True,exist_ok=True)
manifest=json.loads((PROJECT/'translation/proof_manifest_ch02_05_v1.json').read_text(encoding='utf-8'))
items=json.loads((PROJECT/'translation/segments_ch02_05_v1.json').read_text(encoding='utf-8'))
poppler='C:/Users/12059/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.exe'
def render(c):
    subprocess.run([poppler,'-r','100','-png',c['path'],str(QA/c['section'])],check=True,capture_output=True)
    print('Rendered '+c['section'],flush=True)
if '--skip-render' not in sys.argv:
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(render,manifest))
def normalize(t):return re.sub(r'\s+|\*\*','',t)
reports=[]
for c in manifest:
    prefix=c['section']
    paths=sorted(QA.glob(prefix+'-[0-9]*.png'))
    with pdfplumber.open(c['path']) as doc:
        pages=doc.pages
        assert len(paths)==len(pages)
        for offset in range(0,len(paths),9):
            canvas=Image.new('RGB',(1500,2200),'#e3e7ea');draw=ImageDraw.Draw(canvas)
            for j,path in enumerate(paths[offset:offset+9]):
                im=Image.open(path).convert('RGB');im.thumbnail((480,686))
                x=10+(j%3)*500;y=30+(j//3)*730
                canvas.paste(im,(x,y));draw.text((x,y-20),f'{prefix} / page {offset+j+1}',fill='black')
            canvas.save(QA/f'{prefix}-contact-{offset+1:02}.jpg',quality=95)
        texts=[p.extract_text(layout=False) or '' for p in pages]
        overflow=[]
        for n,p in enumerate(pages,1):
            for char in p.chars:
                if char['x0']<30 or char['x1']>p.width-30 or char['top']<10 or char['bottom']>p.height-10:
                    overflow.append({'page':n,'bbox':[char['x0'],char['top'],char['x1'],char['bottom']]})
        selected=[s for s in items if s['section']==prefix]
        figs=[];text_mismatches=[]
        for i,s in enumerate(selected):
            panchor=next(n for n,t in enumerate(texts,1) if s['segment_id']+' · 原书' in t)
            # Extract each bilingual column separately; interleaved table extraction is not reliable.
            p=pages[panchor-1]
            for key,x0,x1 in [('text',36,281),('zh',281,559)]:
                col=p.crop((x0,0,x1,p.height)).extract_text() or ''
                if normalize(s[key]) not in normalize(col):text_mismatches.append({'segment':s['segment_id'],'language':key,'page':panchor})
            if not s.get('figure_id'):continue
            pf=next(n for n,t in enumerate(texts,1) if s['figure_id'] in t)
            nextid=selected[i+1]['segment_id'] if i+1<len(selected) else s['segment_id']
            pn=next(n for n,t in enumerate(texts,1) if nextid+' · 原书' in t)
            figs.append({'figure':s['figure_id'],'page':pf,'anchor_page':panchor,'next_segment_page':pn,'kept_with_context':pf==panchor==pn})
        reports.append({'section':prefix,'pages':len(pages),'overflow':overflow,'text_mismatches':text_mismatches,
                        'figures':figs,'images':sum(len(p.images) for p in pages),'rendered_pages':len(paths)})
(PROJECT/'translation/layout_validation_ch02_05_v1.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps([{'section':r['section'],'pages':r['pages'],'images':r['images'],'overflow':len(r['overflow']),
    'text_mismatches':r['text_mismatches'],'split_figures':[f for f in r['figures'] if not f['kept_with_context']]} for r in reports],ensure_ascii=False,indent=2))
