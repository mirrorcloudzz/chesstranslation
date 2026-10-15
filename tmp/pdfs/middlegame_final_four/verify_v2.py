import json
import re
import subprocess
from pathlib import Path
import pdfplumber
from PIL import Image, ImageOps, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'output/pdf'
QA = Path(__file__).resolve().parent / 'qa_v2'
QA.mkdir(exist_ok=True)
POPPLER = r'C:\Users\12059\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe'
rows = json.loads((QA.parent/'reviewed_segments.json').read_text(encoding='utf-8'))
names = ['five_active_pawns', 'six_heavy_pieces', 'seven_manoeuvring_initiative', 'eight_two_bishops']
for ch, name in zip(range(5,9), names):
    pdf = OUT / f'chess_middlegame_planning_chapter_{name}_bilingual_proof_v2.pdf'
    doc = pdfplumber.open(pdf).pages
    text = '\n'.join(p.extract_text() or '' for p in doc)
    expected = {r['segment_id'] for r in rows if r['chapter']==ch}
    actual = set(re.findall(r'CH\d-\d+',text))
    assert expected == actual, (ch, expected-actual, actual-expected)
    assert '\ufffd' not in text
    for page in doc:
        for char in page.chars:
            assert char['x0']>=0 and char['top']>=0 and char['x1']<=page.width+1 and char['bottom']<=page.height+1
    sample = sorted(set([1,2,len(doc)//2,len(doc)]))
    sheet=Image.new('RGB',(1240,1800),'#d9dfe4')
    draw=ImageDraw.Draw(sheet)
    for i, num in enumerate(sample):
        prefix=QA/f'ch{ch}-p{num}'
        subprocess.run([POPPLER,'-f',str(num),'-l',str(num),'-singlefile','-scale-to','1200','-png',str(pdf),str(prefix)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
        im=Image.open(str(prefix)+'.png').convert('RGB')
        im.thumbnail((600,855))
        x=(i%2)*620+10; y=(i//2)*900+30
        sheet.paste(im,(x,y)); draw.text((x,y-20),f'Chapter {ch} / page {num}',fill='black')
    sheet.save(QA/f'ch{ch}-overview.png')
    print(f'Chapter {ch}: {len(doc)} pages, {len(expected)} segment IDs verified; bounds checked; samples rendered.')
