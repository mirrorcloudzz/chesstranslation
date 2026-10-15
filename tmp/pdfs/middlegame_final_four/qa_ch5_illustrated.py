import json,re,subprocess
from pathlib import Path
import pdfplumber
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[3];TMP=Path(__file__).parent
QA=TMP/'qa_ch5_illustrated';QA.mkdir(exist_ok=True)
pdf=ROOT/'output/pdf/chess_middlegame_planning_chapter_five_active_pawns_illustrated_proof_v1.pdf'
pages=pdfplumber.open(pdf).pages
norm=lambda s:re.sub(r'\s|\*\*','',s)
text=''.join(norm(p.crop((0,45,p.width,p.height-40)).extract_text() or '') for p in pages)
blocks=json.loads((TMP/'ch5_illustrated_blocks.json').read_text(encoding='utf-8'))
for b in blocks:
    assert norm(b['text']) in text,(b['key'],b['text'])
assert sum(len(p.images) for p in pages)==30
for p in pages:
    for c in p.chars: assert c['x0']>=0 and c['x1']<=p.width+1 and c['top']>=0 and c['bottom']<=p.height
figs=json.loads((ROOT/'translations/chess_middlegame_planning/chapter_five_figures/manifest.json').read_text(encoding='utf-8'))
for f in figs:
    if f['caption']:
        matches=[p for p in pages if norm(f['caption']) in norm(p.extract_text() or '')]
        assert matches and all(p.images for p in matches),f
print(len(pages),'pages; all',len(blocks),'blocks present; 30 boards present; text bounds checked.')
poppler=r'C:\Users\12059\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe'
subprocess.run([poppler,'-scale-to','1400','-png',str(pdf),str(QA/'page')],check=True,stderr=subprocess.DEVNULL)
pngs=sorted(QA.glob('page-*.png'))
for start in range(0,len(pngs),6):
    sheet=Image.new('RGB',(1500,1460),'#d5d5d5');draw=ImageDraw.Draw(sheet)
    for k,p in enumerate(pngs[start:start+6]):
        im=Image.open(p).convert('RGB');im.thumbnail((485,690))
        x=(k%3)*500+5;y=(k//3)*730+25
        sheet.paste(im,(x,y));draw.text((x,y-20),p.stem,fill='black')
    sheet.save(QA/f'contact-{start//6+1}.png')
sheet=Image.new('RGB',(1500,1800),'#dddddd');draw=ImageDraw.Draw(sheet)
for k,f in enumerate(figs):
    im=Image.open(ROOT/'translations/chess_middlegame_planning/chapter_five_figures'/f['image']).convert('RGB');im.thumbnail((280,280))
    x=k%5*300+5;y=k//5*300+20;sheet.paste(im,(x,y));draw.text((x,y-16),str(k+1),fill='black')
sheet.save(QA/'boards.png')
