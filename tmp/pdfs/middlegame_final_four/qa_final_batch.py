import json,re,subprocess,sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import pdfplumber
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[3];TMP=Path(__file__).parent
names={5:('five','active_pawns',2),6:('six','heavy_pieces',2),7:('seven','manoeuvring_initiative',1),8:('eight','two_bishops',1)}
poppler=r'C:\Users\12059\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe'
norm=lambda s:re.sub(r'\s|\*\*','',s)
def work(ch):
    QA=TMP/f'qa_final_ch{ch}';QA.mkdir(exist_ok=True)
    if ch==9:pdf=ROOT/'output/pdf/chess_middlegame_planning_epilogue_bilingual_proof_v1.pdf'
    else:
        word,slug,version=names[ch];pdf=ROOT/f'output/pdf/chess_middlegame_planning_chapter_{word}_{slug}_illustrated_proof_v{version}.pdf'
    with pdfplumber.open(pdf) as doc:
        pages=doc.pages
        texts=[norm(p.crop((0,45,p.width,p.height-40)).extract_text() or '') for p in pages]
        if ch!=9:
            blocks=json.loads((TMP/f'ch{ch}_illustrated_blocks.json').read_text(encoding='utf-8'))
            figures=json.loads((TMP/f'ch{ch}_figures.json').read_text(encoding='utf-8'))
            for b in blocks:assert norm(b['text']) in ''.join(texts),(ch,b['key'],b['text'])
            assert sum(len(p.images) for p in pages)==len(figures)
            for _,_,anchor,cap in figures:
                b=next(x for x in blocks if x['last_key']==anchor)
                hits=[i for i,t in enumerate(texts) if norm(cap) in t and norm(b['text']) in t] if cap else [i for i,t in enumerate(texts) if norm(b['text']) in t and pages[i].images]
                assert hits,(ch,anchor,cap)
            boards=[Image.open(p) for p in sorted((ROOT/f'translations/chess_middlegame_planning/chapter_{word}_figures').glob('figure-*.png'))]
            sheet=Image.new('RGB',(1500,((len(boards)+4)//5)*310),'#dddddd');draw=ImageDraw.Draw(sheet)
            for k,im in enumerate(boards):
                im=im.convert('RGB');im.thumbnail((280,280));x=k%5*300+8;y=k//5*310+24
                sheet.paste(im,(x,y));draw.text((x,y-20),str(k+1),fill='black')
            sheet.save(QA/'boards.png')
        for p in pages:
            for c in p.chars:assert c['x0']>=0 and c['x1']<=p.width+1 and c['top']>=0 and c['bottom']<=p.height
        print(ch,len(pages),'pages; content, diagrams, anchors, bounds checked.',flush=True)
    subprocess.run([poppler,'-scale-to','1600','-png',str(pdf),str(QA/'page')],check=True,stderr=subprocess.DEVNULL)
    pngs=sorted(QA.glob('page-*.png'))
    for start in range(0,len(pngs),6):
        sheet=Image.new('RGB',(1500,1460),'#d5d5d5');draw=ImageDraw.Draw(sheet)
        for k,p in enumerate(pngs[start:start+6]):
            im=Image.open(p).convert('RGB');im.thumbnail((485,690));x=(k%3)*500+5;y=(k//3)*730+25
            sheet.paste(im,(x,y));draw.text((x,y-20),p.stem,fill='black')
        sheet.save(QA/f'contact-{start//6+1}.png')
    return ch
with ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(work,[int(x) for x in sys.argv[1:]] or [5,6,7,8,9]))
