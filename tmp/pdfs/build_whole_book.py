import ast, json, re, html, copy, shutil, sys
from pathlib import Path
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, KeepTogether, PageBreak
from reportlab.platypus.tableofcontents import TableOfContents

ROOT=Path(__file__).resolve().parents[2]
T=ROOT/'translations/chess_middlegame_planning'
TMP=ROOT/'tmp/pdfs'
EDITION='--edition' in sys.argv
QA=TMP/('whole_book_edition1' if EDITION else 'whole_book'); QA.mkdir(exist_ok=True)
OUT=ROOT/('output/pdf/chess_middlegame_planning_zh_first_edition.pdf' if EDITION else 'output/pdf/chess_middlegame_planning_complete_zh_proof_v1.pdf')

def load_config(file,names):
    tree=ast.parse(file.read_text(encoding='utf-8'))
    nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names or isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in names for t in n.targets)]
    ns={'re':re};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(file),'exec'),ns)
    return ns

pconfig=load_config(TMP/'middlegame_chapter/build_full_chapter_pdf.py',{'figure','read_blocks','DIAGRAM_SPECS','subsections'})
cconfig=load_config(TMP/'middlegame_chapters12/build_full_chapter_proofs.py',{'figure','read_blocks','CHAPTERS'})
chapters=[];hidden=[];figure_log=[];caption_changes=[]

def block(kind,text,**extra):
    return dict(kind=kind,text=text,figures=[],**extra)

def clean_blocks(blocks):
    out=[]
    for b in blocks:
        if b['text'].strip().startswith(('译注：','译者注：')):
            hidden.append(b['text']);continue
        if b['text'].strip():out.append(b)
    return out

def attach(b,path,label,ref):
    cleaned=re.sub(r'[!?！？‼⁇⁈⁉]','',label)
    if cleaned!=label:caption_changes.append(dict(before=label,after=cleaned))
    f=dict(path=str(path),caption=cleaned,reference=ref)
    assert path.exists(),path
    b['figures'].append(f);figure_log.append(f)

def md_sections():
    text=(T/'01_preface_introduction_zh.md').read_text(encoding='utf-8')
    for title,content in re.findall(r'^## ([^\n]+)\n(.*?)(?=^## |\Z)',text,re.M|re.S):
        content=re.sub(r'^### [A-Z]+-\d+\s*$','',content,flags=re.M)
        chapters.append((title,[block('body',p.strip()) for p in re.split(r'\n\s*\n',content) if p.strip()]))
md_sections()

planning=[];part=None
kindmap={'p':'body','move':'moves','heading':'heading','bullet':'bullet','h2':'heading','h3':'heading'}
for letter,name,section,file in pconfig['subsections']:
    if letter!=part:planning.append(block('part',letter+'　'+name));part=letter
    if section!=letter+'　'+name:planning.append(block('heading',section))
    rows=clean_blocks([block(kindmap[k],v) for k,v in pconfig['read_blocks'](T/file)])
    for spec in pconfig['DIAGRAM_SPECS'].get(file,[]):
        candidates=[b for b in rows if spec['anchor'] in b['text']]
        assert len(candidates)==1,(file,spec,candidates)
        attach(candidates[0],TMP/'middlegame_chapter/diagrams'/spec['name'],spec['caption'],file+': '+spec['anchor'])
    planning.extend(rows)
chapters.append(('计划',planning))

for conf in cconfig['CHAPTERS']:
    rows=clean_blocks([block(kindmap.get(k,k),v) for k,v in cconfig['read_blocks'](T/conf['source'])])
    for spec in conf['figures']:
        found=[(i,b) for i,b in enumerate(rows) if b['kind']==kindmap.get(spec['kind'],spec['kind']) and spec['anchor'] in b['text']]
        assert len(found)==1,(spec,found)
        i,b=found[0];end=b['text'].index(spec['anchor'])+len(spec['anchor'])
        before,after=b['text'][:end],b['text'][end:]
        if before.count('**')%2:before+='**';after='**'+after
        b['text']=before
        if after.strip():
            if spec['name']=='page-087-diagram-2.png' and after.strip()=='g5':after='29... g5'
            rows.insert(i+1,block(b['kind'],after.strip()))
        attach(b,TMP/'middlegame_chapters12/diagrams'/spec['name'],spec['caption'],conf['source']+': '+spec['anchor'])
    if rows[0]['kind']=='heading':rows.pop(0)
    chapters.append((conf['title'].replace('：','　'),rows))

for ch,word,filename,title in [(3,'three','13_chapter_three_reviewed.json','第三章　a线上的战斗'),(4,'four','14_chapter_four_reviewed.json','第四章　中心及其战略意义')]:
    rows=[]
    for s in json.loads((T/filename).read_text(encoding='utf-8')):
        if s['kind']=='title':continue
        for txt in s['zh'].split('\n\n'):
            pure=not re.search(r'[\u4e00-\u9fff]',txt) and bool(re.match(r'(?:\*\*)?\d+\.',txt))
            rows.append(block('moves' if pure else s['kind'] if s['kind'] in ('heading','metadata') else 'body',txt,id=s['segment_id'],page=s['page']))
    rows=clean_blocks(rows)
    assets=T/f'chapter_{word}_figures'
    figures=json.loads((assets/('manifest.json' if ch==3 else 'illustrated_proof_manifest.json')).read_text(encoding='utf-8'))
    for f in figures:
        if ch==3:
            at=max(i for i,b in enumerate(rows) if b['id']==f['anchor']);b=rows[at]
        else:
            marker=f['marker'];candidates=[]
            for i,b in enumerate(rows):
                pos=b['text'].rfind(marker)
                if pos>=0:candidates.append((abs(b['page']-f['source_pdf_page']),i,pos))
            assert candidates,f
            _,at,pos=min(candidates);b=rows[at];end=pos+len(marker)
            before,after=b['text'][:end],b['text'][end:]
            if after.startswith('**'):before+='**';after=after[2:]
            elif before.count('**')%2:before+='**';after='**'+after
            b['text']=before
            if after.strip():rows.insert(at+1,dict(b,text=after.strip(),figures=[]))
        attach(b,assets/f['image'],f['caption'],f.get('anchor',f.get('marker')))
    chapters.append((title,rows))

titles={5:'第五章　进一步谈兵的积极行动',6:'第六章　重子斗争',7:'第七章　调动与主动权',8:'第八章　双象'}
for ch,word in [(5,'five'),(6,'six'),(7,'seven'),(8,'eight')]:
    rows=json.loads((TMP/f'middlegame_final_four/ch{ch}_illustrated_blocks.json').read_text(encoding='utf-8'))
    for b in rows:b['figures']=[]
    for f in json.loads((T/f'chapter_{word}_figures/manifest.json').read_text(encoding='utf-8')):
        bs=[b for b in rows if b['last_key']==f['anchor']];assert len(bs)==1,f
        attach(bs[0],T/f'chapter_{word}_figures'/f['image'],f['caption'],f['anchor'])
    chapters.append((titles[ch],clean_blocks(rows)))
ep=json.loads((T/'19_epilogue_reviewed.json').read_text(encoding='utf-8'))
chapters.append(('代后记',[block('body',s['zh']) for s in ep]))
assert len(hidden)==2,hidden
assert len(figure_log)==183,len(figure_log)

pdfmetrics.registerFont(TTFont('Deng',r'C:\Windows\Fonts\Deng.ttf'))
pdfmetrics.registerFont(TTFont('DengBold',r'C:\Windows\Fonts\Dengb.ttf'))
pdfmetrics.registerFontFamily('Deng',normal='Deng',bold='DengBold',italic='Deng',boldItalic='DengBold')
body=ParagraphStyle('body',fontName='Deng',fontSize=10.5,leading=18,firstLineIndent=21,spaceAfter=7,alignment=TA_JUSTIFY,wordWrap='CJK',allowWidows=0,allowOrphans=0)
styles={'body':body}
styles['moves']=ParagraphStyle('moves',parent=body,fontName='DengBold',firstLineIndent=0,leftIndent=8,spaceBefore=4)
styles['heading']=ParagraphStyle('heading',parent=body,fontName='DengBold',fontSize=13,leading=21,firstLineIndent=0,spaceBefore=12,keepWithNext=True)
styles['part']=ParagraphStyle('part',parent=styles['heading'],fontSize=17,leading=26)
styles['metadata']=ParagraphStyle('metadata',parent=body,firstLineIndent=0,spaceAfter=3,keepWithNext=True)
styles['bullet']=ParagraphStyle('bullet',parent=body,firstLineIndent=0,leftIndent=12)
caption=ParagraphStyle('caption',parent=body,fontSize=9,leading=14,firstLineIndent=0,alignment=TA_CENTER,spaceAfter=10)
chapterstyle=ParagraphStyle('chapter',parent=styles['part'],fontSize=20,leading=30,spaceBefore=0,spaceAfter=18)
cover=ParagraphStyle('cover',parent=chapterstyle,fontSize=27,leading=42,alignment=TA_CENTER)

SAN=r'(?:O-O(?:-O)?|[KQRBN]?[a-h]?[1-8]?x?[a-h][1-8](?:=[QRBN])?[+#?!]*)'
TOKEN=re.compile(r'\*\*|\n|\d+\.(?:\.\.)?\s*'+SAN+r'|\.\.\.\s*'+SAN+r'|'+SAN+r'|[A-Za-z][A-Za-z0-9_.+\-]*|.')
def wrapped(text,style):
    text=text.replace('`','').replace('  \n','\n')
    units=[];bold=style.fontName=='DengBold'
    for token in TOKEN.findall(text):
        if token=='**':bold=not bold;continue
        if token in '，。；：！？、）〕》”' and units and units[-1][0]!='\n':
            units[-1]=(units[-1][0]+token,units[-1][1]);continue
        units.append((token,bold))
    width=A4[0]-46*mm-12-style.leftIndent-style.rightIndent-1
    limit=width-style.firstLineIndent;used=0;lines=[];line=[]
    for token,bold in units:
        w=pdfmetrics.stringWidth(token,'DengBold' if bold else 'Deng',style.fontSize)
        if token=='\n' or line and used+w>limit:
            lines.append(line);line=[];used=0;limit=width
            if token=='\n':continue
            token=token.lstrip();w=pdfmetrics.stringWidth(token,'DengBold' if bold else 'Deng',style.fontSize)
        line.append((token,bold));used+=w
    if line:lines.append(line)
    return '<br/>'.join(''.join(('<b>'+html.escape(t)+'</b>') if bold else html.escape(t) for t,bold in line) for line in lines)

def para(b):
    st=styles[b['kind']];return Paragraph(wrapped(b['text'],st),st)

def figure_card(f):
    with PILImage.open(f['path']) as im:w,h=im.size
    width=70*mm
    picture=Image(f['path'],width=width,height=width*h/w,hAlign='CENTER')
    picture.figure_id=figure_log.index(f)+1
    return [Spacer(1,3*mm),picture,Spacer(1,2*mm),Paragraph(html.escape(f['caption']),caption) if f['caption'] else Spacer(1,8*mm)]

class Book(SimpleDocTemplate):
    def afterFlowable(self,f):
        if hasattr(f,'chapter_key'):
            self.canv.bookmarkPage(f.chapter_key)
            self.canv.addOutlineEntry(f.getPlainText(),f.chapter_key,0,False)
            self.notify('TOCEntry',(0,f.getPlainText(),self.page,f.chapter_key))
            self.chapter_pages[f.getPlainText()]=self.page
        if hasattr(f,'figure_id'):self.figure_pages[f.figure_id]=self.page

def furniture(c,d):
    if d.page==1:return
    c.saveState();c.setFillColor(colors.HexColor('#64727B'));c.setFont('Deng',8)
    c.drawString(23*mm,A4[1]-11*mm,'彼得·罗曼诺夫斯基《国际象棋中局计划》'+('' if EDITION else '｜全书中文校样'))
    c.setStrokeColor(colors.HexColor('#CDD5DB'));c.line(23*mm,A4[1]-14*mm,A4[0]-23*mm,A4[1]-14*mm)
    c.drawCentredString(A4[0]/2,9.5*mm,str(d.page));c.restoreState()

story=[Spacer(1,44*mm),Paragraph('国际象棋中局计划',cover),Spacer(1,12*mm),Paragraph('彼得·罗曼诺夫斯基 著',caption),Spacer(1,7*mm),Paragraph('中文译本 · 第一版' if EDITION else '全书中文带图校样 · 版本1',caption),Paragraph('2026年9月28日',caption),PageBreak(),Paragraph('目录',chapterstyle)]
toc=TableOfContents();toc.levelStyles=[ParagraphStyle('toc',fontName='Deng',fontSize=11,leading=26,leftIndent=0,rightIndent=20,spaceBefore=2)];story.extend([toc,PageBreak()])
for n,(title,original) in enumerate(chapters):
    print('Preparing:',title,flush=True)
    if n:story.append(PageBreak())
    h=Paragraph(title,chapterstyle);h.chapter_key='chapter-'+str(n);story.append(h)
    rows=copy.deepcopy(original);i=0
    while i<len(rows):
        b=rows[i]
        if b['figures']:
            cluster=[para(b)]
            # CH3's final board follows an explanation referring back to 38. Bh4.
            if b.get('id')=='CH3-176' and story and isinstance(story[-1],Paragraph):cluster.insert(0,story.pop())
            for f in b['figures']:cluster.extend(figure_card(f))
            if i+1<len(rows) and rows[i+1]['kind'] in ('body','moves') and not rows[i+1]['figures']:
                nxt=rows[i+1]
                if len(nxt['text'])<=180:cluster.append(para(nxt));i+=1
                elif nxt['kind']=='body':
                    m=re.search('[。！？]',nxt['text'][40:150])
                    if m:
                        cut=41+m.start();cluster.append(para(dict(nxt,text=nxt['text'][:cut])));rows[i+1]=dict(nxt,text=nxt['text'][cut:])
            story.append(KeepTogether(cluster))
        else:story.append(para(b))
        i+=1
doc=Book(str(OUT),pagesize=A4,leftMargin=23*mm,rightMargin=23*mm,topMargin=21*mm,bottomMargin=18*mm,title='国际象棋中局计划 中文译本第一版' if EDITION else '国际象棋中局计划 全书中文带图校样',author='Peter Romanovsky' if EDITION else 'Peter Romanovsky / 中文翻译校样')
doc.chapter_pages={};doc.figure_pages={}
print('Typesetting',len(story),'items',flush=True)
doc.multiBuild(story,onFirstPage=furniture,onLaterPages=furniture)
report=dict(chapter_pages=doc.chapter_pages,figure_pages=doc.figure_pages,figures=figure_log,caption_changes=caption_changes,hidden_notes=hidden,source_counts={title:len(rows) for title,rows in chapters},output=str(OUT))
(QA/'manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(pages=doc.page,figures=len(figure_log),caption_changes=len(caption_changes),chapter_pages=doc.chapter_pages),ensure_ascii=False,indent=2))
