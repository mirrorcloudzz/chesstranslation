import json,re
from pathlib import Path
from html import escape
from PIL import Image as PILImage,ImageOps
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER,TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate,Paragraph,Image,Spacer,KeepTogether,PageBreak

ROOT=Path(__file__).resolve().parents[3]
TMP=Path(__file__).parent
TRANS=ROOT/'translations/chess_middlegame_planning'
ASSETS=TRANS/'chapter_six_figures'
ASSETS.mkdir(exist_ok=True)
OUT=ROOT/'output/pdf/chess_middlegame_planning_chapter_six_heavy_pieces_illustrated_proof_v1.pdf'
blocks=json.loads((TMP/'ch6_illustrated_blocks.json').read_text(encoding='utf-8'))
figures=json.loads((TMP/'ch6_figures.json').read_text(encoding='utf-8'))
pdfmetrics.registerFont(TTFont('Deng',r'C:\Windows\Fonts\Deng.ttf'))
pdfmetrics.registerFont(TTFont('DengBold',r'C:\Windows\Fonts\Dengb.ttf'))
pdfmetrics.registerFontFamily('Deng',normal='Deng',bold='DengBold',italic='Deng',boldItalic='DengBold')
body=ParagraphStyle('body',fontName='Deng',fontSize=10.5,leading=18,firstLineIndent=21,spaceAfter=7,alignment=TA_JUSTIFY,wordWrap='CJK')
moves=ParagraphStyle('moves',parent=body,fontName='DengBold',firstLineIndent=0,leftIndent=8,spaceBefore=4,spaceAfter=7)
heading=ParagraphStyle('heading',parent=body,fontName='DengBold',firstLineIndent=0,fontSize=13,leading=21,spaceBefore=12,keepWithNext=True)
meta=ParagraphStyle('meta',parent=body,firstLineIndent=0,spaceAfter=3,keepWithNext=True)
caption=ParagraphStyle('caption',parent=body,fontSize=9,leading=14,firstLineIndent=0,alignment=TA_CENTER,spaceAfter=9)
title=ParagraphStyle('title',parent=heading,fontSize=22,leading=34,alignment=TA_CENTER,keepWithNext=False)
styles={'body':body,'moves':moves,'heading':heading,'metadata':meta}
SAN=r'(?:O-O(?:-O)?|[KQRBN]?[a-h]?[1-8]?x?[a-h][1-8](?:=[QRBN])?[+#?!]*)'
def markup(text):
    s=escape(text)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',s)
    return re.sub(r'(?<![A-Za-z0-9])\d+\.(?:\.\.)?\s*'+SAN,lambda m:'<nobr>'+m[0]+'</nobr>',s)
def wrapped_markup(text,style):
    # CJK automatic wrapping ignores ReportLab's nobr spans. Pre-wrap measured
    # units so a move number stays with its move and SAN is never split.
    pattern=r'\d+\.(?:\.\.)?\s*'+SAN+r'|\.\.\.\s*'+SAN+r'|'+SAN+r'|[A-Za-z][A-Za-z0-9_.+\-]*|.'
    tokens=re.findall(pattern,text)
    units=[]
    for token in tokens:
        if token in '，。；：！？、）〕》”' and units:units[-1]+=token
        elif units and units[-1] in '（〔《“':units[-1]+=token
        else:units.append(token)
    width=A4[0]-46*mm-12-style.leftIndent-style.rightIndent-1
    lines=[];line='';used=0;limit=width-style.firstLineIndent
    for unit in units:
        w=pdfmetrics.stringWidth(unit,style.fontName,style.fontSize)
        if line and used+w>limit:
            lines.append(line.rstrip());line='';used=0;limit=width
            unit=unit.lstrip();w=pdfmetrics.stringWidth(unit,style.fontName,style.fontSize)
        line+=unit;used+=w
    if line:lines.append(line.rstrip())
    return '<br/>'.join(markup(s) for s in lines)
def para(b):
    st=styles[b['kind']]
    return Paragraph(wrapped_markup(b['text'],st),st)
manifest=[]
cards={}
for n,(page,box,anchor,label) in enumerate(figures,1):
    src=PILImage.open(TMP/'source'/f'page-{page}.png').convert('L')
    sx=src.width/1304;sy=src.height/1920
    crop=ImageOps.autocontrast(src.crop((int((box[0]-3)*sx),int((box[1]-3)*sy),int((box[2]+3)*sx),int((box[3]+3)*sy))))
    dest=ASSETS/f'figure-{n:02}.png';crop.save(dest)
    w=72*mm
    cards[anchor]=[Spacer(1,3*mm),Image(str(dest),width=w,height=w*crop.height/crop.width,hAlign='CENTER'),Spacer(1,2*mm),Paragraph(markup(label),caption) if label else Spacer(1,8*mm)]
    manifest.append({'figure':n,'source_pdf_page':page,'source_print_page':page-2,'crop_reference_1304x1920':box,'anchor':anchor,'caption':label,'image':dest.name,'status':'caption_pending_source_position_conflict' if not label else 'checked_against_source'})
story=[Spacer(1,42*mm),Paragraph('《国际象棋中局计划》',title),Spacer(1,6*mm),Paragraph('第六章：重子斗争',title),Spacer(1,9*mm),Paragraph('中文整章带图校样 · 版本1',caption),Paragraph('2026-09-28 · 原书印刷页175-193',caption),PageBreak(),Paragraph('第六章　重子斗争',heading)]
i=0
while i<len(blocks):
    b=blocks[i]; key=b['last_key']
    if key in cards:
        cluster=[para(b)]+cards[key]
        if i+1<len(blocks) and blocks[i+1]['kind']=='body' and blocks[i+1]['last_key'] not in cards:
            nxt=blocks[i+1]
            # Keep the start of the adjacent explanation with the board, without
            # forcing a long multi-paragraph comment onto an overfull page.
            if len(nxt['text'])<=180:
                cluster.append(para(nxt));i+=1
            else:
                m=re.search('[。！？]',nxt['text'][50:150])
                cut=51+m.start() if m else 0
                if cut:
                    cluster.append(para(dict(nxt,text=nxt['text'][:cut])))
                    blocks[i+1]=dict(nxt,text=nxt['text'][cut:])
        story.append(KeepTogether(cluster))
    else: story.append(para(b))
    i+=1
def furniture(c,d):
    c.saveState();c.setFillColor(colors.HexColor('#64727B'));c.setFont('Deng',8)
    if d.page>1:
        c.drawString(23*mm,A4[1]-11*mm,'彼得·罗曼诺夫斯基《国际象棋中局计划》｜第六章：重子斗争')
        c.setStrokeColor(colors.HexColor('#CDD5DB'));c.line(23*mm,A4[1]-14*mm,A4[0]-23*mm,A4[1]-14*mm)
    c.drawCentredString(A4[0]/2,9.5*mm,str(d.page));c.restoreState()
doc=SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=23*mm,rightMargin=23*mm,topMargin=21*mm,bottomMargin=18*mm,title='国际象棋中局计划 第六章 中文整章带图校样',author='中文翻译校样')
doc.build(story,onFirstPage=furniture,onLaterPages=furniture)
(ASSETS/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(OUT)
