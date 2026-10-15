import json,re,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
TMP=Path(__file__).parent
TRANS=ROOT/'translations/chess_middlegame_planning'
SRC=TRANS/'15_chapter_five_active_pawns_reviewed.json'
backup=TRANS/'archive/20260928_before_ch5_illustrated'
backup.mkdir(parents=True,exist_ok=True)
for file in [SRC,TRANS/'15_chapter_five_active_pawns_zh.md',TMP/'reviewed_segments.json']:
    if not (backup/file.name).exists(): (backup/file.name).write_bytes(file.read_bytes())
rows=json.loads((backup/SRC.name).read_text(encoding='utf-8'))
edits=json.loads((TMP/'ch5_layout_edits.json').read_text(encoding='utf-8'))
main_spec='11-12 15 22-23 28 35 37 41 43 45 47 49 51-52 54 56 63 65 67 71 75 77 81 83 87 89 95 97 99 104 106-107 109 111 117 124 129 131 136 140 144 146 150 152 154 156 160 164 166 168 170 172 174 180 182 186 195 197 200 202 205 208 211 213 217 221 223 225 227 233-234 238 240-241 245 247 251 253 255 257 262 266 268 270 272 274 276 278 285 287-288 294 297 299 301 308 310 319 321 323 327 331 334 342 344 347 351 353 355 358 362 364 366 368 374 377 381 383 386 388 394 402 409 411 413 415 417 425 428 430 434 436 440 442 444 446 450 452 454 462 466 468 470 477 479 481 483 485 487-488 490 492 498 505 508 510 512 517 527 529 532 534 536 538 542 544 549 554 556 558 560 570 572 574 576 578 580 582 584 588 590 597 605 608 612 616 620 625 627'
main=set()
for spec in main_spec.split():
    ab=list(map(int,spec.split('-'))); main.update(range(ab[0],ab[-1]+1))
main.discard(358)
headings={59,91,120,191,281,358,398,473,523,566}
metadata=set()
for start in headings: metadata.update(range(start+1,start+4))
figure_specs=json.loads((TMP/'ch5_figures.json').read_text(encoding='utf-8'))
anchors={f[2] for f in figure_specs}
parts=[]
for row in rows:
    n=int(row['segment_id'].split('-')[1])
    text=edits.get(str(n),row['zh'])
    text=re.sub('布雷耶(?!尔)','布雷耶尔',text)
    if n==370: text='**12. Qe2**\n\n**12... f5 13. Nb3 f4 14. Bc5 e4 15. Nfd4 f3!**'
    row['zh']=text
    row['review_status']='source_and_layout_review_2026-09-28'
    if n in [1,5,606]: continue
    for k,part in enumerate(text.split('\n\n')):
        kind='moves' if part.startswith('**') and part.endswith('**') or n in main else 'heading' if n in headings else 'metadata' if n in metadata else 'body'
        parts.append({'key':f'{n}.{k}','ids':[row['segment_id']],'page':row['page'],'kind':kind,'text':part.strip('*')})

def join(a,b):
    return a+(' ' if re.search(r'[A-Za-z0-9+#!?.]$',a) and re.match(r'[A-Za-z0-9]',b) else '')+b

blocks=[]
for part in parts:
    if blocks:
        prev=blocks[-1]
        terminal=bool(re.search(r'[。！？：）”]$',prev['text']))
        # Colons introducing an analysis line do not create a separate paragraph.
        terminal=terminal and not prev['text'].endswith('：')
        merge=(part['kind']==prev['kind']=='moves' or part['kind']==prev['kind']=='body' and not terminal)
        if merge and prev['last_key'] not in anchors:
            prev['text']=join(prev['text'],part['text'])
            prev['ids']+=part['ids'];prev['last_key']=part['key']
            continue
    blocks.append(dict(part,last_key=part['key']))
for b in blocks:
    s=b['text']
    s=re.sub(r'(?<!\d)(\d{1,2})\.\s+(?=[KQRBNabcdefghO])',r'\1. ',s)
    s=re.sub(r'\.{2,}\s*','... ',s)
    s=re.sub(r'([a-h][1-8])\s+([+#])',r'\1\2',s)
    b['text']=s
(TMP/'ch5_illustrated_blocks.json').write_text(json.dumps(blocks,ensure_ascii=False,indent=2),encoding='utf-8')
exportrows=[]
group_ranges={348:350,356:357}
skip=set()
for row in rows:
    n=int(row['segment_id'].split('-')[1])
    if n in skip: continue
    if n in group_ranges:
        last=group_ranges[n];members=rows[n-1:last]
        row=copy.deepcopy(row)
        row['source_ids']=[m['segment_id'] for m in members]
        row['segment_id']=f'CH5-{n}–{last}'
        row['zh']=''.join(m['zh'] for m in members)
        row['text']=' '.join(m['text'] for m in members)
        skip.update(range(n+1,last+1))
    exportrows.append(row)
SRC.write_text(json.dumps(exportrows,ensure_ascii=False,indent=2),encoding='utf-8')
combined=json.loads((TMP/'reviewed_segments.json').read_text(encoding='utf-8'))
combined=exportrows+[r for r in combined if r['chapter']!=5]
(TMP/'reviewed_segments.json').write_text(json.dumps(combined,ensure_ascii=False,indent=2),encoding='utf-8')
md=['# 第五章：进一步谈兵的积极行动（中文修订稿）','','2026-09-28：对照原书复核棋谱及段落；原校对编号保留。','']
for r in exportrows: md.extend(['## '+r['segment_id'],'',r['zh'],''])
(TRANS/'15_chapter_five_active_pawns_zh.md').write_text('\n'.join(md),encoding='utf-8')
layout=['# 第五章：进一步谈兵的积极行动（整章排版底稿）','']
for b in blocks: layout.extend(['<!-- '+','.join(dict.fromkeys(b['ids']))+' -->','',('**'+b['text']+'**') if b['kind']=='moves' else b['text'],''])
(TRANS/'15_chapter_five_active_pawns_illustrated_zh.md').write_text('\n'.join(layout),encoding='utf-8')
en=['# 第五章：进一步谈兵的积极行动（英文OCR校对稿）','','2026-09-28：CH5-348–350、CH5-356–357合并误断段落；其余编号保留。','']
for r in exportrows: en.extend(['## '+r['segment_id'],'',r['text'],''])
(TRANS/'15_chapter_five_active_pawns_en_ocr.md').write_text('\n'.join(en),encoding='utf-8')
print(len(blocks),'layout blocks;',len(exportrows),'manuscript units; 629 original IDs covered')
