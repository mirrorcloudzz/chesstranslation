import json, re, subprocess
from pathlib import Path
import pdfplumber
from PIL import Image, ImageOps, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
TMP = Path(__file__).parent / 'qa_v2'
TMP.mkdir(exist_ok=True)
POPPLER = Path(r'C:\Users\12059\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe')
for chapter, stem, manuscript in [(3,'three_a_file','13_chapter_three_reviewed.json'),(4,'four_centre','14_chapter_four_reviewed.json')]:
    pdf = ROOT / 'output/pdf' / f'chess_middlegame_planning_chapter_{stem}_bilingual_proof_v2.pdf'
    doc = pdfplumber.open(pdf).pages
    full = '\n'.join(p.extract_text() for p in doc)
    segments = json.loads((ROOT/'translations/chess_middlegame_planning'/manuscript).read_text(encoding='utf-8'))
    missing = [s['segment_id'] for s in segments if s['kind'] != 'chapter' and s['segment_id'] not in full]
    assert not missing, missing
    assert '\ufffd' not in full
    for p in doc:
        for block in p.chars:
            x0,y0,x1,y1 = block['x0'],block['top'],block['x1'],block['bottom']
            assert x0 >= 0 and y0 >= 0 and x1 <= p.width+1 and y1 <= p.height+1
    print(f'CH{chapter}: {len(doc)} pages; {len(segments)} segments; all IDs present, bounds valid')
    subprocess.run([str(POPPLER),'-scale-to','500','-png',str(pdf),str(TMP/f'ch{chapter}')],check=True)
    pages = sorted(TMP.glob(f'ch{chapter}-*.png'))
    for batch in range(0,len(pages),16):
        canvas = Image.new('RGB',(1440,2120),'#cccccc')
        draw = ImageDraw.Draw(canvas)
        for k,path in enumerate(pages[batch:batch+16]):
            im = Image.open(path).convert('RGB')
            x,y = (k%4)*360, (k//4)*530
            canvas.paste(im,(x,y+22))
            draw.text((x+8,y+4),path.stem,fill='black')
        canvas.save(TMP/f'contact_ch{chapter}_{batch//16+1}.png')
    for page in [2,len(doc)//2,len(doc)]:
        subprocess.run([str(POPPLER),'-f',str(page),'-l',str(page),'-scale-to','1600','-singlefile','-png',str(pdf),str(TMP/f'detail_ch{chapter}_p{page}')],check=True)
