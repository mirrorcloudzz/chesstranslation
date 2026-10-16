import json,re,subprocess
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from project_paths import find_pdftoppm
import pdfplumber
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[3]
WORK=Path(__file__).parent/'qa_illustrated'
WORK.mkdir(exist_ok=True)
pdf=ROOT/'output/pdf/chess_middlegame_planning_chapter_three_a_file_illustrated_proof_v1.pdf'
pages=pdfplumber.open(pdf).pages
norm=lambda s:re.sub(r'\s|\*\*','',s)
text=''.join(norm(p.crop((0,45,p.width,p.height-40)).extract_text() or '') for p in pages)
data=json.loads((ROOT/'translations/chess_middlegame_planning/13_chapter_three_reviewed.json').read_text(encoding='utf-8'))
for s in data:
    assert norm(s['zh']) in text,s['segment_id']
assert sum(len(p.images) for p in pages)==10
for p in pages:
    for c in p.chars:
        assert c['x0']>=0 and c['x1']<=p.width+1 and c['top']>=0 and c['bottom']<=p.height
manifest=json.loads((ROOT/'translations/chess_middlegame_planning/chapter_three_figures/manifest.json').read_text(encoding='utf-8'))
for f in manifest:
    matches=[p for p in pages if norm(f['caption']) in norm(p.extract_text() or '')]
    assert len(matches)==1 and len(matches[0].images)>=1,f
    print(f"Figure {f['figure']}: page {matches[0].page_number}: {f['caption']}")
print(f'{len(pages)} pages; all 154 segments present; 10 images and captions verified')
poppler=Path(find_pdftoppm())
subprocess.run([str(poppler),'-scale-to','1500','-png',str(pdf),str(WORK/'page')],check=True,stderr=subprocess.DEVNULL)
pngs=sorted(WORK.glob('page-*.png'))
for start in range(0,len(pngs),6):
    sheet=Image.new('RGB',(1200,1740),'#cccccc')
    draw=ImageDraw.Draw(sheet)
    for k,p in enumerate(pngs[start:start+6]):
        im=Image.open(p).convert('RGB'); im.thumbnail((580,820))
        x,y=(k%2)*600,(k//2)*580
        im.thumbnail((390,550))
        x,y=(k%3)*400,(k//3)*870
        im=Image.open(p).convert('RGB'); im.thumbnail((395,820))
        sheet.paste(im,(x,y+25)); draw.text((x+5,y+5),p.stem,fill='black')
    sheet.save(WORK/f'contact-{start//6+1}.png')
