import json,re,sys
from pathlib import Path
import pdfplumber
from pypdf import PdfReader
from PIL import Image,ImageOps,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
EDITION='--edition' in sys.argv
QA=ROOT/('tmp/pdfs/whole_book_edition1' if EDITION else 'tmp/pdfs/whole_book')
pdf=ROOT/('output/pdf/chess_middlegame_planning_zh_first_edition.pdf' if EDITION else 'output/pdf/chess_middlegame_planning_complete_zh_proof_v1.pdf')
doc=pdfplumber.open(pdf).pages;m=json.loads((QA/'manifest.json').read_text(encoding='utf-8'))
text='\n'.join(p.extract_text() or '' for p in doc)
compact=re.sub(r'\s+','',text)
if EDITION:
    assert '全书中文校样' not in text
    assert '中文译本·第一版' in compact
    page7=re.sub(r'\s+','',doc[6].extract_text())
    assert '1.c4、1.d4、1.Nf3还是1.e4' in page7
assert '译注：' not in compact and '译者注：' not in compact
assert '28.Nf6Kf829.Rgf3或29.h3' in compact
assert '原文此处的28.f6应为28.Nf6' in compact
assert '此处保留原书这一分支的记录，待校' not in compact
assert '53...Qc2+' in compact
reader=PdfReader(pdf)
assert len(reader.outline)==12,len(reader.outline)
issues=[];images=0;caption_pages=[]
for pi,p in enumerate(doc,1):
    images+=len(p.images)
    for s in p.chars:
        x0,y0,x1,y1=s['x0'],s['top'],s['x1'],s['bottom']
        if x0<60 or x1>p.width-60 or y0<16 or y1>p.height-15:issues.append((pi,s['text'],(x0,y0,x1,y1)))
        if abs(s['size']-9)<0.1:assert s['text'] not in '!?！？',(pi,s['text'])
    if any(abs(s['size']-9)<0.1 for s in p.chars):caption_pages.append(pi)
assert images==183,images
assert not issues,issues[:10]
ns={'__file__':str(ROOT/'tmp/pdfs/build_whole_book.py')}
source=(ROOT/'tmp/pdfs/build_whole_book.py').read_text(encoding='utf-8').split("pdfmetrics.registerFont(TTFont('Deng'")[0]
exec(compile(source,'source_inventory','exec'),ns)
content=[]
for p in doc:
    filtered=p.filter(lambda obj:obj.get('object_type')=='char' and obj['top']>50 and obj['bottom']<800 and abs(obj['size']-9)>0.1)
    content.append(filtered.extract_text() or '')
def norm(s):return re.sub(r'[\s*`]','',s)
bodytext=norm(''.join(content));missing=[]
for title,rows in ns['chapters']:
    for b in rows:
        expected=norm(b['text'])
        if expected not in bodytext:missing.append(dict(chapter=title,text=b['text']))
(QA/'text_coverage_issues.json').write_text(json.dumps(missing,ensure_ascii=False,indent=2),encoding='utf-8')
print('Text coverage differences:',len(missing))
report=dict(pages=len(doc),images=images,bookmarks=[(s.title,reader.get_destination_page_number(s)+1) for s in reader.outline],bounds_issues=issues,caption_pages=caption_pages)
(QA/'qa_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
if '--contacts' in sys.argv:
    pages=sorted((QA/'render').glob('page-*.png'))
    assert len(pages)==len(doc),(len(pages),len(doc))
    for start in range(0,len(pages),20):
        sheet=Image.new('RGB',(1100,1665),'#d9dfe2');draw=ImageDraw.Draw(sheet)
        for j,path in enumerate(pages[start:start+20]):
            im=Image.open(path).convert('RGB');im.thumbnail((263,308))
            x=(j%4)*275+(275-im.width)//2;y=(j//4)*333+22
            sheet.paste(im,(x,y));draw.text(((j%4)*275+12,(j//4)*333+5),str(start+j+1),fill='black')
        sheet.save(QA/f'contact-{start+1:03}.jpg',quality=90)
