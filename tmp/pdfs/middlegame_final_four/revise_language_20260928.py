"""Apply explicit editorial corrections; synchronize manuscripts, never rebuild PDFs."""
import argparse
import copy
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TMP = Path(__file__).resolve().parent
TRANS = ROOT / 'translations' / 'chess_middlegame_planning'
PREFIX = {5:'15_chapter_five_active_pawns',6:'16_chapter_six_heavy_pieces',7:'17_chapter_seven_manoeuvring_initiative',8:'18_chapter_eight_two_bishops'}
TITLE = {5:'第五章：进一步谈兵的积极行动',6:'第六章：重子斗争',7:'第七章：调动与主动权',8:'第八章：双象'}
BACKUP = TRANS / 'archive' / '20260928_before_language_review'
SAN = r'(?:O-O(?:-O)?|[KQRBN]?[a-h]?[1-8]?x?[a-h][1-8](?:=[QRBN])?[+#?!]*)'

def normalize(s):
    s = re.sub(r'(?<![A-Za-z])(?:[O0]-[O0]-[O0])', 'O-O-O', s)
    s = re.sub(r'(?<![A-Za-z])(?:[O0]-[O0])', 'O-O', s)
    # Unambiguous OCR letter l for rank 1, confined to chess tokens.
    s = re.sub(r'(?<![A-Za-z])([KQRBN][a-h]?x?[a-h])l(?=[+#?!.,\s，。;；)）]|$)', r'\g<1>1', s)
    s = re.sub(r'(?<![A-Za-z])([a-h][18])([QRBN])(?=[+#?!.,\s，。;；)）]|$)', r'\1=\2', s)
    # Remove spurious full stops after a move before the opponent's move.
    s = re.sub(r'('+SAN+r')[.。]\s*(?='+SAN+r'(?![A-Za-z]))', r'\1 ', s)
    # Restore missing spacing/period between move number and SAN, not rank numbers.
    s = re.sub(r'(?<![A-Za-z0-9.])(\d{1,3})[。.]?\s*('+SAN+r')(?![A-Za-z])', r'\1. \2', s)
    s = re.sub(r'(?<!\d)(\d{1,3})\s*\.{2,}\s*', r'\1... ', s)
    s = re.sub(r'\.{4,}', '...', s)
    s = s.replace('……', '...')
    return re.sub(r'\s+', ' ', s).strip()

def pure_moves(s):
    t = re.sub(SAN, '', s)
    return not re.search(r'[A-Za-z\u4e00-\u9fff]', t)

def mixed_moves(s):
    # Only complete English connector words/phrases; all complex prose is hand-edited.
    for a,b in [('and wins','并获胜'),('If','若'),('if','若'),('then','则'),('Or','或'),('or','或'),('and','，'),('followed by','随后'),('with','，'),('mate','将杀')]:
        s = re.sub(r'\b'+re.escape(a)+r'\b',b,s)
    return s

def main():
    apply = argparse.ArgumentParser()
    apply.add_argument('--apply', action='store_true')
    args=apply.parse_args()
    src = BACKUP / 'reviewed_segments.json'
    if not src.exists():
        src = TMP / 'reviewed_segments.json'
    original=json.loads(src.read_text(encoding='utf-8'))
    rows=copy.deepcopy(original)
    fixes={}
    for file in sorted(TMP.glob('corrections_*.json')):
        fixes.update(json.loads(file.read_text(encoding='utf-8')))
    ids={x['segment_id'] for x in rows}
    assert set(fixes).issubset(ids),set(fixes)-ids
    enf = TMP / 'english_verified_20260928.json'
    english=json.loads(enf.read_text(encoding='utf-8')) if enf.exists() else {}
    for row in rows:
        sid=row['segment_id']
        en=normalize(english.get(sid,row['text']))
        row['text']=en
        if sid in fixes:
            zh=fixes[sid]
        elif pure_moves(en):
            zh=en
        elif row['kind']=='moves':
            zh=mixed_moves(en)
        else:
            zh=row['zh']
        for a,b in {'通兵':'通路兵','二步杀':'两步杀','王的位置置':'王的位置','兵攻势':'兵的攻击','兵攻击':'兵的攻击','空位 h线':'开放的h线'}.items():
            zh=zh.replace(a,b)
        row['zh']=normalize(zh)
        row['review_status']='language_review_2026-09-28'
    (TMP/'language_review_candidate.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    changed=Counter()
    log=[]
    for old,new in zip(original,rows):
        if old['zh']!=new['zh'] or old['text']!=new['text']:
            changed[new['chapter']]+=1
            log.append({'segment_id':new['segment_id'],'page':new['page'],'zh_before':old['zh'],'zh_after':new['zh'],'en_before':old['text'],'en_after':new['text'],'explicit_rewrite':new['segment_id'] in fixes})
    print('Explicit editorial entries:',len(fixes),'changed:',dict(changed))
    # Show unrevised prose, and any residual source words in Chinese.
    for r in rows:
        residue=re.sub(SAN,'',r['zh'])
        words=re.findall(r'[A-Za-z]{3,}',residue)
        if words:
            print('RESIDUE',r['segment_id'],words,r['zh'])
    print('UNREWRITTEN PROSE:')
    for r in rows:
        if r['segment_id'] not in fixes and r['kind']!='moves' and re.search(r'[\u4e00-\u9fff]{4}',r['zh']):
            print(r['segment_id'],r['text'],'|',r['zh'])
    if not args.apply:
        return
    BACKUP.mkdir(parents=True,exist_ok=True)
    if not (BACKUP/'reviewed_segments.json').exists():
        (BACKUP/'reviewed_segments.json').write_text(json.dumps(original,ensure_ascii=False,indent=2),encoding='utf-8')
    (TRANS/'15-18_language_review_changes_20260928.json').write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf-8')
    (TMP/'reviewed_segments.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    for ch in range(5,9):
        selected=[r for r in rows if r['chapter']==ch]
        for suffix in ['_reviewed.json','_zh.md','_en_ocr.md']:
            p=TRANS/(PREFIX[ch]+suffix)
            if p.exists() and not (BACKUP/p.name).exists():
                (BACKUP/p.name).write_bytes(p.read_bytes())
        (TRANS/(PREFIX[ch]+'_reviewed.json')).write_text(json.dumps(selected,ensure_ascii=False,indent=2),encoding='utf-8')
        for lang,field,desc in [('zh','zh','中文修订稿'),('en_ocr','text','英文OCR校对稿')]:
            parts=[f'# {TITLE[ch]}（{desc}）','', '修订日期：2026-09-28。保留原校对编号；分段之间的续文应连读。','']
            for r in selected:
                parts.extend([f"## {r['segment_id']}",'',r[field],''])
            (TRANS/(PREFIX[ch]+'_'+lang+'.md')).write_text('\n'.join(parts),encoding='utf-8')
    assert [r['segment_id'] for r in original]==[r['segment_id'] for r in rows]
    assert len(rows)==1468 and all(r['zh'].strip() for r in rows)
    print('SAVED; 1468 original IDs preserved; PDFs untouched.')

if __name__=='__main__':
    main()
