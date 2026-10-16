"""Build the editable bilingual proofs for front matter, introduction and ch01.

Input is human-reviewed paired Markdown, not unreviewed OCR. Figure anchors
are explicit. OCR IDs are recovered with a page-scoped sequence alignment;
the scan/page references remain authoritative if an OCR token is missing.
"""
import difflib
import html
import json
import re
import unicodedata
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, LongTable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from PIL import Image as PILImage
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / 'translations/art_of_attack'
OUT = ROOT / 'output/pdf'
QA = ROOT / 'tmp/pdfs/art_of_attack_opening'
CONFIGS = [
    ('front_preface', '开篇材料与编者序', '原书封面、封底及第3—5页', '00_开篇材料与编者序_中英对照分段校样_v1.pdf'),
    ('introduction', '导言', '原书第6—13页', '01_导言_中英对照分段校样_v1.pdf'),
    ('ch01', '第一章：攻击尚未易位的王', '原书第14—27页', '02_第一章_攻击尚未易位的王_中英对照分段校样_v1.pdf'),
]

def parse_file(stem):
    text = (PROJECT / 'translation' / f'{stem}_v1.md').read_text(encoding='utf-8')
    result = []
    for block in re.split(r'(?m)^## ', text)[1:]:
        head, body = block.split('\n', 1)
        sid, pages, kind = (x.strip() for x in head.split('|'))
        start, _, end = pages.partition('-')
        item = {'segment_id': sid, 'section': stem, 'page': int(start),
                'page_end': int(end or start), 'kind': kind,
                'status': 'draft_v1_for_user_review', 'scan_checked': True}
        fields = dict(re.findall(r'(?m)^(EN|ZH|FIG|REF): (.*)$', body))
        item['text'] = fields['EN'].replace('\\n', '\n')
        item['zh'] = (fields['EN'] if fields['ZH'] == '=' else fields['ZH']).replace('\\n', '\n')
        if 'REF' in fields:item['note_anchor']=fields['REF'].strip()
        if 'FIG' in fields:
            fid, _, caption = fields['FIG'].partition('|')
            item['figure_id'] = fid.strip()
            item['caption_zh'] = caption.strip()
            item['caption_status'] = 'context_verified' if caption.strip() else 'blank_no_game_context'
        result.append(item)
    return result

def tokens(s):
    s = unicodedata.normalize('NFKD', s.lower())
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.findall(r'[a-z]+|\d+', s)

def provenance(items):
    """Align all reviewed tokens to OCR per page; retain real line IDs only."""
    for item in items:
        item['source_ids'] = []
        item['source_scan_paths'] = [f'source_pages/page-{p:03}.png' for p in range(item['page'], item['page_end']+1)]
    needed_pages = sorted({p for s in items for p in range(s['page'], s['page_end'] + 1)})
    source_files = list((PROJECT / 'ocr/chapters').glob('*.json'))
    page_lines = {}
    for file in source_files:
        src = json.loads(file.read_text(encoding='utf-8'))
        for page in src.get('pages', []):
            if page['pdf_page'] in needed_pages:
                page_lines.setdefault(page['pdf_page'], []).extend(page['lines'])
    for p in needed_pages:
        lines = []
        lines = page_lines.get(p, [])
        if not lines:
            continue
        a, owners_a, b, owners_b = [], [], [], []
        for line in lines:
            ts = tokens(line['text'])
            a.extend(ts); owners_a.extend([line['id']]*len(ts))
        relevant = [s for s in items if s['page'] <= p <= s['page_end']]
        for item in relevant:
            ts = tokens(item['text'])
            b.extend(ts); owners_b.extend([item]*len(ts))
        for match in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
            for j in range(match.size):
                sid = owners_a[match.a+j]
                item = owners_b[match.b+j]
                if sid not in item['source_ids']:
                    item['source_ids'].append(sid)
        for item in relevant:
            # Chess glyph-only lines can lack matching text; page anchor is explicit.
            if not item['source_ids']:
                item['source_mapping_precision'] = 'scan_page_only'
    for item in items:
        item.setdefault('source_mapping_precision', 'OCR_token_alignment_scan_verified')

pdfmetrics.registerFont(TTFont('Deng', 'C:/Windows/Fonts/Deng.ttf'))
pdfmetrics.registerFont(TTFont('DengBold', 'C:/Windows/Fonts/Dengb.ttf'))
pdfmetrics.registerFontFamily('Deng', normal='Deng', bold='DengBold', italic='Deng', boldItalic='DengBold')
pdfmetrics.registerFont(TTFont('BookEnglish', 'C:/Windows/Fonts/times.ttf'))
pdfmetrics.registerFont(TTFont('BookEnglishBold', 'C:/Windows/Fonts/timesbd.ttf'))
pdfmetrics.registerFont(TTFont('BookEnglishItalic', 'C:/Windows/Fonts/timesi.ttf'))
pdfmetrics.registerFontFamily('BookEnglish',normal='BookEnglish',bold='BookEnglishBold',italic='BookEnglishItalic',boldItalic='BookEnglishBold')
NAVY = colors.HexColor('#18354C')
RULE = colors.HexColor('#CDD5DB')
PALE = colors.HexColor('#F5F7F8')
MUTED = colors.HexColor('#64727B')
EN = ParagraphStyle('English', fontName='BookEnglish', fontSize=8.1, leading=11.7, spaceAfter=0)
ZH = ParagraphStyle('Chinese', fontName='Deng', fontSize=9, leading=14.2, wordWrap='CJK', spaceAfter=0)
TITLE = ParagraphStyle('Title', fontName='DengBold', fontSize=19, leading=27, textColor=NAVY)
SUB = ParagraphStyle('Sub', fontName='Deng', fontSize=9, leading=15, textColor=MUTED, wordWrap='CJK')
HEAD = ParagraphStyle('Head', fontName='DengBold', fontSize=9, leading=13, textColor=colors.white, alignment=TA_CENTER)
CAP = ParagraphStyle('Caption', fontName='Deng', fontSize=8.7, leading=13, alignment=TA_CENTER, wordWrap='CJK')

def markup(value):
    value = html.escape(value)
    value = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', value)
    # Keep a move number with its following SAN token in this editable proof.
    value = re.sub(r'(\d+\.(?:\.\.)?) ([KQRBN]?[a-hO][a-zA-Z0-9x=+#?!-]*)', lambda m:m[1]+'\u00a0'+m[2], value)
    return value.replace('\n', '<br/>')

def cell(item, language):
    value = item['text' if language == 'en' else 'zh']
    style = EN if language == 'en' else ZH
    if item['kind'] in {'title', 'heading', 'metadata', 'moves'}:
        value = '**'+value+'**' if '**' not in value else value
    pages = str(item['page']) if item['page_end'] == item['page'] else f"{item['page']}—{item['page_end']}"
    label = f"{item['segment_id']} · 原书{pages}页"
    if item['page'] <= 2:
        label = f"{item['segment_id']} · 原版{'封面' if item['page']==1 else '封底'}"
    if item['kind'] == 'footnote':
        label += ' · 纳恩编者注'
    return Paragraph(f'<font name="DengBold" size="7.2" color="#3B6885">{label}</font><br/>{markup(value)}', style)

def build(config, items, figures, *, output_dir=None, version='v1', date='2026-10-01'):
    stem, title, scope, filename = config
    selected = [s for s in items if s['section'] == stem]
    # Preserve stable source IDs while placing cross-example notes at their
    # actual reference rather than the bottom-of-scan-page reading position.
    attached={s['note_anchor']:s for s in selected if s.get('note_anchor')}
    if attached:
        arranged=[]
        for item in selected:
            if item.get('note_anchor'):continue
            arranged.append(item)
            if item['segment_id'] in attached:arranged.append(attached[item['segment_id']])
        if len(arranged)!=len(selected):raise ValueError('Missing or duplicate footnote anchor')
        selected=arranged
    destination = Path(output_dir) if output_dir is not None else OUT
    destination.mkdir(parents=True, exist_ok=True)
    filename_out = destination / f'art_of_attack_{stem}_bilingual_proof_{version}.pdf'
    doc = SimpleDocTemplate(str(filename_out), pagesize=A4, leftMargin=13*mm, rightMargin=13*mm,
                            topMargin=19*mm, bottomMargin=16*mm,
                            title=f'Art of Attack in Chess | {title} | Bilingual proof {version}',
                            author='Vladimir Vuković; bilingual translation proof')
    data = [[Paragraph('英文校订稿', HEAD), Paragraph('中文初译稿', HEAD)]]
    commands = [('BACKGROUND',(0,0),(-1,0),NAVY),('VALIGN',(0,0),(-1,-1),'TOP'),
                ('LEFTPADDING',(0,0),(-1,-1),6.5),('RIGHTPADDING',(0,0),(-1,-1),6.5),
                ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]
    keep_ranges = []
    for i, item in enumerate(selected):
        row = len(data)
        data.append([cell(item,'en'), cell(item,'zh')])
        commands.extend([('BACKGROUND',(0,row),(-1,row),colors.white if row%2 else PALE),
                         ('LINEBELOW',(0,row),(-1,row),0.3,RULE)])
        if item.get('figure_id'):
            fig = figures[item['figure_id']]
            path = PROJECT / fig['image']
            with PILImage.open(path) as im:
                w,h = im.size
            graphic = Image(str(path),width=80*mm,height=80*mm*h/w)
            graphic.hAlign = 'CENTER'
            contents = [graphic]
            if item['caption_zh']:
                contents += [Spacer(1,3*mm),Paragraph(markup(item['caption_zh']),CAP)]
            contents += [Paragraph(f"{item['figure_id']} · 原书{fig['pdf_page']}页",SUB)]
            frow = len(data)
            data.append([contents,''])
            commands.extend([('SPAN',(0,frow),(-1,frow)),('BACKGROUND',(0,frow),(-1,frow),colors.white),
                             ('ALIGN',(0,frow),(-1,frow),'CENTER')])
            # Anchor, diagram and its immediate commentary travel together.
            keep_ranges.append((row, min(frow+1, frow+1 if i+1<len(selected) else frow)))
        elif item['kind'] in {'title','heading','metadata'}:
            keep_ranges.append((row,row+1))
    for first,last in keep_ranges:
        last=min(last,len(data)-1)
        commands.append(('NOSPLIT',(0,first),(-1,last)))
    # Consecutive heading/diagram ranges can overlap. Fit the entire connected
    # group, including the repeated table header, rather than splitting its text.
    merged=[]
    for first,last in keep_ranges:
        last=min(last,len(data)-1)
        if merged and first<=merged[-1][1]:
            merged[-1]=(merged[-1][0],max(last,merged[-1][1]))
        else:merged.append((first,last))
    def group_height(rows):
        probe=Table(rows,colWidths=[86*mm,98*mm])
        probe.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),
            ('LEFTPADDING',(0,0),(-1,-1),6.5),('RIGHTPADDING',(0,0),(-1,-1),6.5),
            ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
            *[('SPAN',(0,i),(-1,i)) for i,row in enumerate(rows) if isinstance(row[0],list)]]))
        return probe.wrap(184*mm,100000)[1]
    limit=A4[1]-35*mm-12-group_height(data[:1])-3
    for first,last in merged:
        rows=data[first:last+1]
        height=group_height(rows)
        if height<=limit:continue
        graphics=[flow for row in rows for value in row if isinstance(value,list) for flow in value if isinstance(flow,Image)]
        if not graphics:raise ValueError(f'Unbreakable text group exceeds a page: {selected[0]["section"]}, row {first}')
        available=sum(g.drawHeight for g in graphics)
        factor=(available-(height-limit)-4)/available
        if factor<0.65:raise ValueError(f'Diagram group needs source paragraph splitting: {selected[0]["section"]}, row {first}')
        for graphic in graphics:
            graphic.drawWidth*=factor;graphic.drawHeight*=factor
        if group_height(rows)>limit:raise ValueError('Diagram group still exceeds the page')
    table=LongTable(data,colWidths=[86*mm,98*mm],repeatRows=1,splitByRow=1,splitInRow=0,hAlign='CENTER')
    table.setStyle(TableStyle(commands))
    def furniture(canvas, d):
        canvas.saveState()
        canvas.setFillColor(MUTED);canvas.setFont('Deng',7.7)
        canvas.drawString(13*mm,A4[1]-11*mm,f'《国际象棋进攻的艺术》｜{title}｜中英对照')
        canvas.setStrokeColor(RULE);canvas.line(13*mm,A4[1]-14*mm,A4[0]-13*mm,A4[1]-14*mm)
        canvas.drawCentredString(A4[0]/2,9*mm,str(d.page))
        canvas.restoreState()
    story=[Paragraph(title,TITLE),Spacer(1,3*mm),
           Paragraph(f'{scope} · {selected[0]["segment_id"]}—{selected[-1]["segment_id"]} · {version} · {date}',SUB),
           Spacer(1,5*mm),table]
    doc.build(story,onFirstPage=furniture,onLaterPages=furniture)
    pdf=PdfReader(str(filename_out))
    extracted='\n'.join(p.extract_text() or '' for p in pdf.pages)
    missing=[s['segment_id'] for s in selected if s['segment_id'] not in extracted]
    if missing: raise ValueError(f'Missing segments: {missing}')
    return {'section':stem,'title':title,'path':str(filename_out),'desktop_filename':filename,
            'pages':len(pdf.pages),'segments':len(selected),
            'figures':sum(bool(s.get('figure_id')) for s in selected),'missing_segments':missing}

def main():
    OUT.mkdir(parents=True,exist_ok=True);QA.mkdir(parents=True,exist_ok=True)
    items=[]
    for c in CONFIGS:items.extend(parse_file(c[0]))
    assert len({s['segment_id'] for s in items})==len(items)
    for s in items:
        if '棋步' in s['zh'] or '......' in s['zh']:raise ValueError(s['segment_id'])
        if s.get('caption_zh') and re.search(r'[!?]',s['caption_zh']):raise ValueError('Caption annotations')
    provenance(items)
    (PROJECT/'translation/segments_v1.json').write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf-8')
    figures={s['id']:s for s in json.loads((PROJECT/'figures/manifest.json').read_text(encoding='utf-8'))}
    expected={s['id'] for s in figures.values() if s['pdf_page']<=27}
    actual={s['figure_id'] for s in items if s.get('figure_id')}
    assert expected==actual,(expected-actual,actual-expected)
    output=[build(c,items,figures) for c in CONFIGS]
    (PROJECT/'translation/proof_manifest_v1.json').write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf-8')
    (PROJECT/'translation/figure_anchors_v1.json').write_text(json.dumps([
        {'figure_id':s['figure_id'],'anchor_segment':s['segment_id'],'caption':s['caption_zh'],
         'status':s['caption_status']} for s in items if s.get('figure_id')],ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(output,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
