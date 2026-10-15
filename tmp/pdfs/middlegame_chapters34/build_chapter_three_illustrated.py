import json
import re
from html import escape
from pathlib import Path
from PIL import Image as PILImage, ImageOps, ImageDraw
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, KeepTogether, PageBreak

ROOT = Path(__file__).resolve().parents[3]
WORK = Path(__file__).parent
TRANS = ROOT / 'translations/chess_middlegame_planning'
ASSETS = TRANS / 'chapter_three_figures'
ASSETS.mkdir(exist_ok=True)
OUT = ROOT / 'output/pdf/chess_middlegame_planning_chapter_three_a_file_illustrated_proof_v1.pdf'

# Crop coordinates refer to the visually checked 1304 x 1920 source previews.
# All ten boards are copied from the original scan; no pieces are reconstructed.
FIGURES = [
    (90, (137,77,530,466), 'CH3-7', '马尔科（白）对穆勒（黑），白方行棋', '片段；后文从33. Qa1开始'),
    (90, (759,1006,1152,1394), 'CH3-14–15', '拉斯克（白）对肖瓦尔特（黑），黑方行棋', '片段；原文说明白方第60步后，随后60... Rb1'),
    (91, (762,128,1155,518), 'CH3-24', '卡帕布兰卡（白）对特雷巴尔（黑），白方行棋', '片段；随后40. Ra1'),
    (92, (133,1093,529,1483), 'CH3-39', '卡帕布兰卡（白）对阿廖欣（黑），白方行棋', '片段；随后26. b5'),
    (94, (134,82,528,472), 'CH3-65–66', '白方走完13. Nd2后的局面', '前页末主线13. Nd2，白马在d2'),
    (95, (142,256,538,646), 'CH3-83', '黑方走完20... b5后的局面', '前页主线20. Raxc1 b5，黑兵在b5'),
    (96, (135,757,533,1148), 'CH3-103', '黑方走完33... Raa2后的局面', '图上方主线33... Raa2，黑车在a2和b2'),
    (97, (759,971,1154,1360), 'CH3-133–134', '黑方走完13... d5!后的局面', '图上方主线13... d5!，黑兵在d5和e4'),
    (99, (759,138,1155,529), 'CH3-156', '黑方走完24... a5!后的局面', '左栏主线24. Be1 a5!，黑兵在a5，白兵仍在g2'),
    (100,(773,79,1170,468), 'CH3-176', '白方走完38. Bh4后的局面', 'see next diagram指向38. Bh4；白象h4，黑车a1、a8'),
]

pdfmetrics.registerFont(TTFont('Deng', r'C:\Windows\Fonts\Deng.ttf'))
pdfmetrics.registerFont(TTFont('DengBold', r'C:\Windows\Fonts\Dengb.ttf'))
pdfmetrics.registerFontFamily('Deng', normal='Deng', bold='DengBold', italic='Deng', boldItalic='DengBold')
body = ParagraphStyle('Body', fontName='Deng', fontSize=10.5, leading=18,
    firstLineIndent=21, spaceAfter=6, alignment=TA_JUSTIFY, wordWrap='CJK', textColor=colors.HexColor('#202A31'))
moves = ParagraphStyle('Moves', parent=body, fontName='DengBold', firstLineIndent=0, leftIndent=10, spaceAfter=6)
heading = ParagraphStyle('Heading', parent=body, fontName='DengBold', fontSize=17, leading=26, firstLineIndent=0, spaceAfter=14)
game = ParagraphStyle('Game', parent=body, fontName='DengBold', firstLineIndent=0, spaceBefore=7, spaceAfter=4, keepWithNext=True)
metadata = ParagraphStyle('Meta', parent=body, firstLineIndent=0, spaceAfter=3, keepWithNext=True)
caption = ParagraphStyle('Caption', parent=body, firstLineIndent=0, fontSize=9, leading=14, alignment=TA_CENTER, spaceAfter=10)
cover = ParagraphStyle('Cover', parent=heading, alignment=TA_CENTER, fontSize=24, leading=35)
subtitle = ParagraphStyle('Subtitle', parent=caption, fontSize=12, leading=21)

def markup(text):
    return re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', escape(text)).replace('\n','<br/>')

def make_blocks():
    result=[]
    for seg in json.loads((TRANS/'13_chapter_three_reviewed.json').read_text(encoding='utf-8')):
        if seg['segment_id']=='CH3-1':
            continue
        for k, text in enumerate(seg['zh'].split('\n\n')):
            pure_moves = not re.search(r'[\u4e00-\u9fff]',text) and bool(re.match(r'(?:\*\*)?\d+\.',text))
            style = moves if pure_moves else game if seg['kind']=='heading' else metadata if seg['kind']=='metadata' else body
            result.append({'id':seg['segment_id'], 'text':text, 'style':style})
    return result

def board_card(index, spec):
    page, box, anchor, label, evidence = spec
    path = ASSETS/f'figure-{index:02d}.png'
    src = PILImage.open(WORK/'source'/f'page-{page:03d}.png').convert('L')
    sx, sy=src.width/1304,src.height/1920
    crop=src.crop((round((box[0]-3)*sx),round((box[1]-3)*sy),round((box[2]+3)*sx),round((box[3]+3)*sy)))
    crop=ImageOps.autocontrast(crop)
    crop.save(path)
    width=72*mm
    return [Spacer(1,3*mm), Image(str(path),width=width,height=width*crop.height/crop.width,hAlign='CENTER'),Spacer(1,1.5*mm),Paragraph(markup(label),caption)]

blocks=make_blocks()
positions={}
for i,b in enumerate(blocks):
    positions[b['id']]=i
insertions={positions[f[2]]:(n,f) for n,f in enumerate(FIGURES,1)}
story=[Spacer(1,45*mm),Paragraph('《国际象棋中局计划》',cover),Spacer(1,5*mm),Paragraph('第三章：a线上的战斗',cover),Spacer(1,8*mm),Paragraph('中文整章带图校样 · 版本 1',subtitle),Paragraph('原书印刷页 87-98',subtitle),PageBreak(),Paragraph('第三章　a线上的战斗',heading)]
i=0
while i<len(blocks):
    b=blocks[i]
    if i in insertions:
        n,spec=insertions[i]
        cluster=[Paragraph(markup(b['text']),b['style'])]+board_card(n,spec)
        if i+1<len(blocks):
            following=blocks[i+1]
            cluster.append(Paragraph(markup(following['text']),following['style']))
            i+=1
        # For the last board also keep the immediately preceding move sequence.
        if spec[2]=='CH3-176':
            cluster.insert(0,story.pop())
        story.append(KeepTogether(cluster))
    else:
        story.append(Paragraph(markup(b['text']),b['style']))
    i+=1

def furniture(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor('#64727B'))
    canvas.setFont('Deng',8)
    if doc.page>1:
        canvas.drawString(23*mm,A4[1]-11*mm,'彼得·罗曼诺夫斯基《国际象棋中局计划》｜第三章：a线上的战斗')
        canvas.setStrokeColor(colors.HexColor('#CDD5DB'))
        canvas.line(23*mm,A4[1]-14*mm,A4[0]-23*mm,A4[1]-14*mm)
    canvas.drawCentredString(A4[0]/2,9.5*mm,str(doc.page))
    canvas.restoreState()

doc=SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=23*mm,rightMargin=23*mm,topMargin=21*mm,bottomMargin=18*mm,title='国际象棋中局计划 第三章：a线上的战斗 中文整章带图校样',author='中文翻译校样')
doc.build(story,onFirstPage=furniture,onLaterPages=furniture)
manifest=[{'figure':n,'source_pdf_page':s[0],'source_print_page':s[0]-2,'anchor':s[2],'caption':s[3],'evidence':s[4],'image':f'figure-{n:02d}.png'} for n,s in enumerate(FIGURES,1)]
(ASSETS/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(OUT)
