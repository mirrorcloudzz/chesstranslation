import json, re
from html import escape
from pathlib import Path
from PIL import Image as PILImage, ImageOps
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, KeepTogether, PageBreak

ROOT=Path(__file__).resolve().parents[3]
WORK=Path(__file__).parent
TRANS=ROOT/'translations/chess_middlegame_planning'
ASSETS=TRANS/'chapter_four_figures'
OUT=ROOT/'output/pdf/chess_middlegame_planning_chapter_four_centre_illustrated_proof_v4.pdf'
DATA=json.loads((TRANS/'14_chapter_four_reviewed.json').read_text(encoding='utf-8'))

# Visually checked automatic source-board crops. Where the position/move cannot
# be established unambiguously from the source context, deliberately omit a caption.
FIGURES=[
 (102,1,165,1557,'白方走完14. Ne5后的局面'),
 (103,1,165,507,'黑方走完11... c5 12. Qf3后的局面'),
 (105,1,169,1621,''),(106,1,160,1360,''),(106,2,908,1496,''),(108,1,170,91,''),(108,2,909,1562,''),(110,1,904,798,''),(111,1,906,1392,''),(112,1,912,1621,''),(114,1,160,208,''),(115,1,904,306,''),(117,1,908,1242,''),(118,1,918,95,''),(121,1,941,664,''),
 (124,1,174,200,''),(125,1,165,1302,'白方走完21. Rh6后的局面'),(126,1,910,1634,'白方走完13. exd4后的局面'),(127,1,944,254,''),(128,1,184,262,''),(128,2,912,820,''),(129,1,186,1634,''),(130,1,900,1351,''),(130,2,177,1504,''),(131,1,911,994,''),(132,1,178,1594,''),(133,1,177,1205,''),(134,1,174,1049,''),(136,1,175,276,''),(137,1,913,1593,''),(138,1,910,1154,'白方走完12. Be2后的局面'),(139,1,225,1107,''),(140,1,221,707,''),(140,2,984,708,''),(141,1,906,260,''),(142,1,977,264,''),(143,1,906,412,'白方走完21. e4后的局面')
]

# Captions and their precise insertion markers.  The marker is the move or
# sentence immediately above the diagram in the original.  A marker may fall
# on the preceding source page when the diagram begins the next page.
CAPTION_MARKERS={
 (102,1):('白方走完14. Ne5后的局面','14. Ne5'),
 (103,1):('白方走完12. Qf3后的局面','12. Qf3'),
 (105,1):('黑方走完18... Rac8后的局面','18. Qxc4 Rac8?'),
 (106,1):('白方走完20. Ng1后的局面','白方刚走完20. Ng1。'),
 (106,2):('米泽斯（白）对比耶卡尔（黑），白方走棋','在米泽斯对比耶卡尔一局中（奥斯坦德，1907年），出现了类似的局面。'),
 (108,1):('黑方走完6... Nc6后的局面','6... Nc6'),
 (108,2):('黑方走完21... Nb4后的局面','21. Nc3 Nb4'),
 (110,1):('黑方走完22... Rfc8后的局面','22... Rfc8'),
 (111,1):('黑方走完9... O-O后的局面','9... O-O?'),
 (112,1):('黑方走完20... Nxg7后的局面','20. Bxg7 Nxg7'),
 (114,1):('白方走完28. bxa4后的局面','28. bxa4'),
 (115,1):('白方走完6. fxe5后的局面','6. fxe5'),
 (117,1):('白方走完12. e4后的局面','12. e4'),
 (118,1):('黑方走完3... Nf6后的局面','3. Nc3 Nf6'),
 (121,1):('黑方走完6... d5后的局面','6. cxb5 d5'),
 (124,1):('白方走完6. Bg5后的局面','6. Bg5'),
 (125,1):('白方走完21. Rh6后的局面','21. Rh6'),
 (126,1):('白方走完13. exd4后的局面','13. exd4'),
 (127,1):('黑方走完18... Rc7后的局面','18... Rc7'),
 (128,1):('索科尔斯基（白）对鲍特维尼克（黑），白方走棋','下例是索科尔斯基对鲍特维尼克一局'),
 (128,2):('塔拉什（白）对齐果林（黑），白方走棋','图示局面出自1893年塔拉什对齐果林对抗赛第19局。'),
 (129,1):('拉文斯基（白）对罗曼诺夫斯基（黑），白方走棋','在拉文斯基对罗曼诺夫斯基一局中（列宁格勒，1926年）'),
 (130,1):('黑方走完31... e5后的局面','31... e5'),
 (130,2):('肖瓦尔特（白）对布莱克本（黑），白方走棋','肖瓦尔特对布莱克本一局（纽伦堡，1896年）'),
 (131,1):('黑方走完11... c5后的局面','11. O-O c5'),
 (132,1):('白方走完17. g4后的局面','17. g4'),
 (133,1):('白方走完11. Be3后的局面','11. Be3'),
 (134,1):('黑方走完24... Qc6后的局面','24. e3 Qc6'),
 (136,1):('白方走完12. Bf1后的局面','12. Bf1'),
 (137,1):('黑方走完26... c4后的局面','26... c4'),
 (138,1):('白方走完12. Be2后的局面','12. Be2'),
 (139,1):('黑方走完24... a5后的局面','24. Rd4 a5'),
 (140,1):('白方走完12. e4后的局面','12. e4'),
 (140,2):('黑方走完15... Rad8后的局面','15. Rad1 Rad8'),
 (141,1):('白方走完22. b4后的局面','22. b4?'),
 (142,1):('黑方走完10... exd5后的局面','10. cxd5 exd5'),
 (143,1):('白方走完21. e4后的局面','21. e4'),
}
MANUAL_CROPS={
    (137,1):(899,1584,1407,2095),
    (121,1):(900,655,1392,1135),
    (127,1):(900,245,1402,728),
    (139,1):(162,1098,658,1580),
    (140,1):(162,698,657,1178),
    (140,2):(899,699,1406,1179),
    (142,1):(899,255,1399,736),
}
# Keep the previous proof's image-card heights so that correcting the crop does
# not disturb the user's established page references.  The extra height is
# neutral white padding; the complete board itself is not stretched.
LEGACY_ASPECTS={
    (137,1):480/479,
    (121,1):480/451,
    (127,1):480/463,
    (139,1):480/439,
    (140,1):480/442,
    (140,2):478/431,
    (142,1):479/426,
}
LEGACY_MANUAL={(102,1),(103,1),(125,1),(126,1),(138,1),(143,1)}
for pg,n,x,y,label in FIGURES:
    if (pg,n) in MANUAL_CROPS or (pg,n) in LEGACY_MANUAL:
        src=PILImage.open(WORK/'source'/f'page-{pg:03d}.png').convert('L')
        box=MANUAL_CROPS.get((pg,n),(x-5,y-5,x+480,y+465))
        crop=ImageOps.autocontrast(src.crop(box))
        if (pg,n) in LEGACY_ASPECTS:
            target_h=round(crop.width*LEGACY_ASPECTS[(pg,n)])
            extra=max(0,target_h-crop.height)
            crop=ImageOps.expand(crop,border=(0,extra//2,0,extra-extra//2),fill=255)
        crop.save(ASSETS/f'page-{pg:03d}-diagram-{n}.png')
    assert (ASSETS/f'page-{pg:03d}-diagram-{n}.png').exists(),(pg,n)

pdfmetrics.registerFont(TTFont('Deng',r'C:\Windows\Fonts\Deng.ttf'))
pdfmetrics.registerFont(TTFont('DengBold',r'C:\Windows\Fonts\Dengb.ttf'))
pdfmetrics.registerFontFamily('Deng',normal='Deng',bold='DengBold',italic='Deng',boldItalic='DengBold')
body=ParagraphStyle('Body',fontName='Deng',fontSize=10.5,leading=18,firstLineIndent=21,spaceAfter=6,alignment=TA_JUSTIFY,wordWrap='CJK',textColor=colors.HexColor('#202A31'))
moves=ParagraphStyle('Moves',parent=body,fontName='DengBold',firstLineIndent=0,leftIndent=10,spaceAfter=6)
heading=ParagraphStyle('Heading',parent=body,fontName='DengBold',fontSize=17,leading=26,firstLineIndent=0,spaceBefore=10,spaceAfter=12,keepWithNext=True)
game=ParagraphStyle('Game',parent=body,fontName='DengBold',firstLineIndent=0,spaceBefore=7,spaceAfter=4,keepWithNext=True)
metadata=ParagraphStyle('Meta',parent=body,firstLineIndent=0,spaceAfter=3,keepWithNext=True)
caption=ParagraphStyle('Caption',parent=body,firstLineIndent=0,fontSize=9,leading=14,alignment=TA_CENTER,spaceAfter=10)
cover=ParagraphStyle('Cover',parent=heading,alignment=TA_CENTER,fontSize=24,leading=35,spaceBefore=0,spaceAfter=0)
subtitle=ParagraphStyle('Subtitle',parent=caption,fontSize=12,leading=21)
def markup(s): return re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',escape(s)).replace('\n','<br/>')

blocks=[]
for seg in DATA:
    if seg['segment_id']=='CH4-1': continue
    for txt in seg['zh'].split('\n\n'):
        if not txt.strip(): continue
        pure=not re.search(r'[\u4e00-\u9fff]',txt) and bool(re.match(r'(?:\*\*)?\d+\.',txt))
        sty=moves if pure else game if seg['kind']=='heading' else metadata if seg['kind']=='metadata' else body
        blocks.append({'id':seg['segment_id'],'page':seg['page'],'side':seg.get('side','left'),'text':txt,'style':sty})

# Locate each diagram by its exact source marker, splitting a move sequence when
# the original places the diagram between two moves in the same OCR segment.
fig_after={}
for seq,(pg,n,x,y,_old_label) in enumerate(FIGURES,1):
    label,marker=CAPTION_MARKERS[(pg,n)]
    path=ASSETS/f'page-{pg:03d}-diagram-{n}.png'
    src=PILImage.open(path)
    width=68*mm
    card=[Spacer(1,2*mm),Image(str(path),width=width,height=width*src.height/src.width,hAlign='CENTER'),Spacer(1,1.2*mm),Paragraph(markup(label),caption)]
    candidates=[]
    for i,b in enumerate(blocks):
        pos=b['text'].rfind(marker)
        if pos>=0:
            candidates.append((abs(b['page']-pg),i,pos))
    if not candidates:
        raise ValueError(f'No insertion marker for figure {seq}: {marker!r}')
    _,at,pos=min(candidates)
    b=blocks[at]
    end=pos+len(marker)
    before,after=b['text'][:end],b['text'][end:]
    if after.startswith('**'):
        before+='**'; after=after[2:]
    elif before.count('**')%2:
        before+='**'; after='**'+after
    b['text']=before
    if after.strip():
        blocks.insert(at+1,{**b,'text':after.lstrip()})
        fig_after={i+(1 if i>at else 0):v for i,v in fig_after.items()}
    fig_after.setdefault(at,[]).append(card)

story=[Spacer(1,43*mm),Paragraph('《国际象棋中局计划》',cover),Spacer(1,5*mm),Paragraph('第四章：中心及其战略意义',cover),Spacer(1,8*mm),Paragraph('中文整章带图校样 · 版本 4',subtitle),Paragraph('原书印刷页 99–142',subtitle),PageBreak(),Paragraph('第四章　中心及其战略意义',heading)]
for i,b in enumerate(blocks):
    paragraph=Paragraph(markup(b['text']),b['style'])
    if i in fig_after:
        cluster=[paragraph]
        for card in fig_after[i]:
            cluster.extend(card)
        story.append(KeepTogether(cluster))
    else:
        story.append(paragraph)

def furniture(canvas,doc):
    canvas.saveState(); canvas.setFillColor(colors.HexColor('#64727B')); canvas.setFont('Deng',8)
    if doc.page>1:
        canvas.drawString(23*mm,A4[1]-11*mm,'彼得·罗曼诺夫斯基《国际象棋中局计划》｜第四章：中心及其战略意义')
        canvas.setStrokeColor(colors.HexColor('#CDD5DB')); canvas.line(23*mm,A4[1]-14*mm,A4[0]-23*mm,A4[1]-14*mm)
    canvas.drawCentredString(A4[0]/2,9.5*mm,str(doc.page)); canvas.restoreState()
doc=SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=23*mm,rightMargin=23*mm,topMargin=21*mm,bottomMargin=18*mm,title='国际象棋中局计划 第四章：中心及其战略意义 中文整章带图校样',author='中文翻译校样')
doc.build(story,onFirstPage=furniture,onLaterPages=furniture)
manifest=[{'figure':i,'source_pdf_page':pg,'source_print_page':pg-2,'caption':CAPTION_MARKERS[(pg,n)][0],'marker':CAPTION_MARKERS[(pg,n)][1],'image':f'page-{pg:03d}-diagram-{n}.png'} for i,(pg,n,x,y,label) in enumerate(FIGURES,1)]
(ASSETS/'illustrated_proof_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(OUT)
