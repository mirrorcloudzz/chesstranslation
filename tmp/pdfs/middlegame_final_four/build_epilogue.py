import json
from pathlib import Path
from html import escape
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,KeepTogether
ROOT=Path(__file__).resolve().parents[3];TRANS=ROOT/'translations/chess_middlegame_planning'
rows=[{'segment_id':'EP-1','page':228,'text':'In the chess struggle, enterprise and foresight, boldness and composure, daring and persistence, ingenuity in imagination and accuracy of calculation, allow the scientific process of the chess game to become creative. In other words, with the production of creative forms, chess can be placed alongside works of art.','zh':'在国际象棋的斗争中，进取与远见、大胆与沉着、勇气与毅力，以及想象的巧思和计算的准确，使讲究科学方法的对弈过程具有创造性。换言之，正是这些创造性的表现，使国际象棋足以与艺术作品相提并论。'},
{'segment_id':'EP-2','page':228,'text':'The present book calls upon chessplayers to strive for creativity. In addition, it calls for a deep respect and study of chess theory and endeavours to do everything in its power to help chess enthusiasts achieve these important objectives.','zh':'本书呼吁棋手追求创造性，同时倡导尊重并深入研究国际象棋理论，并力求尽其所能，帮助国际象棋爱好者实现这些重要目标。'}]
(TRANS/'19_epilogue_reviewed.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
(TRANS/'19_epilogue_zh.md').write_text('# 代后记\n\n'+'\n\n'.join('## '+r['segment_id']+'\n\n'+r['zh'] for r in rows),encoding='utf-8')
(TRANS/'19_epilogue_en_ocr.md').write_text('# Instead of an Epilogue\n\n'+'\n\n'.join('## '+r['segment_id']+'\n\n'+r['text'] for r in rows),encoding='utf-8')
pdfmetrics.registerFont(TTFont('Deng',r'C:\Windows\Fonts\Deng.ttf'));pdfmetrics.registerFont(TTFont('DengBold',r'C:\Windows\Fonts\Dengb.ttf'))
head=ParagraphStyle('head',fontName='DengBold',fontSize=20,leading=30,spaceAfter=12)
sub=ParagraphStyle('sub',fontName='Deng',fontSize=10,leading=16,textColor=colors.HexColor('#64727B'),spaceAfter=14)
label=ParagraphStyle('id',fontName='DengBold',fontSize=10,leading=16,spaceAfter=6)
en=ParagraphStyle('en',fontName='Helvetica',fontSize=10.5,leading=16,spaceAfter=10)
zh=ParagraphStyle('zh',fontName='Deng',fontSize=11,leading=20,spaceAfter=18,wordWrap='CJK')
story=[Paragraph('代后记',head),Paragraph('Instead of an Epilogue',en),Paragraph('中英对照校样 · 版本1 · 原书印刷页226',sub)]
for r in rows:story.append(KeepTogether([Paragraph(r['segment_id'],label),Paragraph(escape(r['text']),en),Paragraph(r['zh'],zh)]))
out=ROOT/'output/pdf/chess_middlegame_planning_epilogue_bilingual_proof_v1.pdf'
def footer(c,d):
    c.setFont('Deng',8);c.setFillColor(colors.HexColor('#64727B'));c.drawCentredString(A4[0]/2,11*mm,str(d.page))
SimpleDocTemplate(str(out),pagesize=A4,leftMargin=24*mm,rightMargin=24*mm,topMargin=24*mm,bottomMargin=22*mm,title='国际象棋中局计划 代后记 中英对照校样').build(story,onFirstPage=footer,onLaterPages=footer)
print(out)
