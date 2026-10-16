"""Check current bilingual PDFs and render every page for visual inspection."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import unicodedata

import pdfplumber
from PIL import Image, ImageDraw
from pypdf import PdfReader
from build_complete_proofs import DEST,NAMES
from build_opening_proofs import PROJECT,ROOT,parse_file
sys.path.insert(0,str(ROOT/'tools'))
from project_paths import find_pdftoppm

QA=ROOT/'tmp/pdfs/art_of_attack_complete_v2'


def norm(value):
    return re.sub(r'\s+|\*\*','',unicodedata.normalize('NFKC',value))


def clean_column(value):
    value=re.sub(r'(?:CH\d+|FM|PF|IN|PI|OI)-\d+ · 原书\d+(?:—\d+)?页(?: · 纳恩编者注)?','',value)
    value=re.sub(r'(?:FM|PF)-\d+ · 原版封[面底]','',value)
    return value.replace('英文校订稿','').replace('中文初译稿','')


def check(config):
    number,(stem,title,start,end)=config
    path=DEST/f'{number:02d}_{stem}_bilingual_proof_v2.pdf'
    items=parse_file(stem)
    result={'section':stem,'file':path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'overflow':[],'missing_text':[],'figure_checks':[]}
    with pdfplumber.open(path) as pdf:
        result['pages']=len(pdf.pages)
        result['images']=sum(len(p.images) for p in pdf.pages)
        texts=[p.extract_text() or '' for p in pdf.pages]
        columns={}
        for key,x0,x1 in [('text',36,281),('zh',281,559)]:
            columns[key]=norm(''.join(clean_column(p.crop((x0,53,x1,p.height-35)).extract_text() or '') for p in pdf.pages))
        raw_text=norm(''.join(p.extract_text() or '' for p in PdfReader(path).pages))
        result['column_extraction_fallbacks']=[]
        for item in items:
            for key in columns:
                if norm(item[key]) not in columns[key]:
                    # pdfplumber may sort overlapping punctuation glyph boxes
                    # as "16Q.e2". Verify the complete source string against the
                    # PDF content stream before calling this a missing passage.
                    if norm(item[key]) in raw_text:
                        result['column_extraction_fallbacks'].append({'segment':item['segment_id'],'language':key})
                    else:result['missing_text'].append({'segment':item['segment_id'],'language':key})
        for n,page in enumerate(pdf.pages,1):
            for char in page.chars:
                if char['x0']<30 or char['x1']>page.width-30 or char['top']<10 or char['bottom']>page.height-10:
                    result['overflow'].append({'page':n,'text':char['text'],'bounds':[char['x0'],char['top'],char['x1'],char['bottom']]})
        for i,item in enumerate(items):
            if not item.get('figure_id'):continue
            figure=item['figure_id']
            fp=[n for n,t in enumerate(texts,1) if figure in t]
            ap=[n for n,t in enumerate(texts,1) if re.search(re.escape(item['segment_id'])+r' · 原',t)]
            following=items[min(i+1,len(items)-1)]['segment_id']
            np=[n for n,t in enumerate(texts,1) if re.search(re.escape(following)+r' · 原',t)]
            result['figure_checks'].append({'figure':figure,'figure_pages':fp,'anchor_pages':ap,'next_pages':np,
                                           'kept_with_context':len(fp)==1 and fp==ap==np})
        result['ok']=(not result['overflow'] and not result['missing_text'] and
                      all(f['kept_with_context'] for f in result['figure_checks']) and
                      result['images']==len(result['figure_checks']))
    return result


def render(result):
    folder=QA/'render'/result['section']
    folder.mkdir(parents=True,exist_ok=True)
    subprocess.run([find_pdftoppm(),'-r','85','-png',str(ROOT/result['file']),str(folder/'page')],check=True,capture_output=True)
    images=sorted(folder.glob('page-*.png'))
    assert len(images)==result['pages'],(result['section'],len(images),result['pages'])
    contacts=QA/'contacts'
    contacts.mkdir(parents=True,exist_ok=True)
    for offset in range(0,len(images),12):
        canvas=Image.new('RGB',(1500,2160),'#d9dfe2');draw=ImageDraw.Draw(canvas)
        for j,path in enumerate(images[offset:offset+12]):
            with Image.open(path) as image:
                image.thumbnail((485,505));x=8+(j%3)*500;y=28+(j//3)*540
                canvas.paste(image,(x+(485-image.width)//2,y))
            draw.text((x,y-20),f'{result["section"]} / {offset+j+1}',fill='black')
        canvas.save(contacts/f'{result["section"]}-{offset+1:03}.jpg',quality=90)
    result['rendered_pages']=len(images)
    print(f'{result["section"]}: rendered {len(images)} pages',flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sections',nargs='+')
    parser.add_argument('--skip-render',action='store_true')
    args=parser.parse_args()
    QA.mkdir(parents=True,exist_ok=True)
    configs=[(n,c) for n,c in enumerate(NAMES) if not args.sections or c[0] in args.sections]
    with ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(check,configs))
    for r in results:print(json.dumps({k:r[k] for k in ['section','pages','images','ok','missing_text']},ensure_ascii=False),flush=True)
    if not args.skip_render:
        with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(render,results))
    report=PROJECT/'translation/layout_validation_complete_v2.json'
    old=json.loads(report.read_text(encoding='utf-8')) if report.exists() else {'sections':[]}
    combined={r['section']:r for r in old['sections']}
    combined.update({r['section']:r for r in results})
    report.write_text(json.dumps({'method':'Per-column full segment text coverage, page bounds, image counts, diagram/anchor/next-block page equality; rendered pages require separate visual review.',
                                 'sections':[combined[c[0]] for c in NAMES if c[0] in combined]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return 0 if all(r['ok'] for r in results) else 1


if __name__=='__main__':sys.exit(main())
