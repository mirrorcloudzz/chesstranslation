"""Chapter Four source-scan review; retain all legacy proofreading IDs."""
import importlib
import json
import re
from pathlib import Path
from ch4_review_english import REPLACE, EXACT

ROOT = Path(str(Path(__file__).resolve().parents[3]))
TRANS = ROOT / 'translations/chess_middlegame_planning'
TMP = Path(__file__).parent
SOURCE = TMP / 'chapter_four_before_review.json'
if not SOURCE.exists():
    data = json.loads((TMP / 'translated_segments_clean.json').read_text(encoding='utf-8'))
    data = [s for s in data if 101 <= s['page'] <= 144 and s['kind'] != 'chapter']
    assert len(data) == 714
    SOURCE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
source = json.loads(SOURCE.read_text(encoding='utf-8'))
merges, zh, en = {}, {}, {}
for n in range(1, 6):
    mod = importlib.import_module(f'ch4_review_{n}')
    merges.update(mod.MERGES)
    zh.update(mod.ZH)
    en.update(mod.EN)
merges[135] = 136

def clean_english(s):
    for a, b in {
        'athe ': 'at the ', 'Athe ': 'At the ', 'thethe ': 'the ',
        'broughthe':'brought the', 'buthe':'but the', 'abouthe':'about the',
        'againsthe':'against the', 'atthe':'at the', 'tothe':'to the',
        'intohe':'into the', 'ofthe':'of the',
        'takethe':'take the', 'exploithe':'exploit the', 'preventhe':'prevent the',
        'carry outhe':'carry out the', 'retreathe':'retreat the',
        'broughtabout':'brought about', 'holdingthe':'holding the',
        'thatthe':'that the', 'thenthe':'then the', 'supporthe':'support the',
        'Withouthe':'Without the', 'withouthe':'without the',
        'interrupthe':'interrupt the', 'accounthe':'account the',
        '1l...':'11...', 'Racl':'Rac1', 'Rxcl':'Rxc1',
        'Bfl':'Bf1', 'Nel':'Ne1', 'Kxhl':'Kxh1', 'diagona1':'diagonal',
        'piecearmy':'piece army', 'pieceforces':'piece forces',
        'returnmatch':'return match', 'wellfortified':'well-fortified',
        'doubleedged':'double-edged', 'wellcomposed':'well-composed',
        'opponnent':'opponent', 'standin ':'standing ', 'decidin ':'deciding ',
        'Relyin ':'Relying ', 'relyin ':'relying ', 'takin ':'taking ',
        'doublin ':'doubling ', 'f2s':'f2', 'ad- vance':'advance',
        'varia- tion':'variation', 'threa- tening':'threatening',
        'threa- tened':'threatened', 'posi- tion':'position', 'or- ganises':'organises',
        'dra on':'drag on',
        'averthe':'avert the', 'accepthe':'accept the', 'cuthe':'cut the',
        'carry outhe':'carry out the', 'prevent- ing':'preventing',
        'back- ward':'backward',
    }.items():
        s = s.replace(a, b)
    s = re.sub(r'\bnothe\b', 'not the', s)
    s = re.sub(r'\bRel\b', 'Re1', s)
    s = re.sub(r'([A-Za-z])- ([A-Z])', r'\1-\2', s)
    s = re.sub(r'\b([a-h](?:x[a-h])?[18])\(?([QRBN])\)?(?=[+#!?\s]|$)', r'\1=\2', s)
    s = re.sub(r'(?<!\.)\.{2}(?!\.)', '...', s)
    s = re.sub(r'(\d+)\.(?!\.)(?=[KQRBNOa-h])', r'\1. ', s)
    s = re.sub(r'(?<![A-Za-z0-9.])(\d+)\s+(?=[KQRBNOa-h][a-h1-8x=+#?!-]*(?:\s|$))', r'\1. ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

result, pending = [], []
i = 1
while i <= 714:
    end = merges.get(i, i)
    item = dict(source[i-1])
    text = clean_english(' '.join(source[j-1]['text'] for j in range(i, end+1)))
    text = en.get(i, text)
    for old, new in REPLACE.get(i, {}).items():
        text = text.replace(old, new)
    text = EXACT.get(i, text)
    text = re.sub(r'\.{4,}', '...', text)
    text = re.sub(r'(\d+)\s+\.{3}', r'\1...', text)
    translated = zh.get(i)
    if translated is None:
        # Only pure score lines may be carried forward without a prose rewrite.
        residual = re.sub(r'\b(?:[KQRBN]?[a-h]?[1-8]?x?[a-h][1-8](?:=[QRBN])?|O-O(?:-O)?)\b[+#!?]*', '', text)
        residual = re.sub(r'[\d\s.?!+:#=\-()/½]+', '', residual)
        if residual:
            pending.append((i, text))
            translated = item['zh']
        else:
            translated = '**' + text + '**'
    item.update(text=text, zh=translated, page_end=source[end-1].get('page_end', source[end-1]['page']),
                segment_id=f'CH4-{i}' if i == end else f'CH4-{i}–{end}',
                legacy_ids=[f'CH4-{j}' for j in range(i,end+1)], review_status='source_scan_reviewed')
    result.append(item)
    i = end + 1
if pending:
    for i,t in pending:
        print(f'UNREVIEWED {i}: {t}')
    raise SystemExit(f'{len(pending)} segments require manual review')

# Source bold move sequences are represented in both language versions.
for item in result:
    if item['zh'].startswith('**') and item['zh'].endswith('**') and item['zh'].count('**') == 2:
        if item['zh'][2:-2] == item['text']:
            item['text'] = item['zh']
    for score in re.findall(r'\*\*(.*?)\*\*', item['zh'], flags=re.S):
        if score in item['text'] and '**' + score + '**' not in item['text']:
            left, right = item['text'].rsplit(score, 1)
            item['text'] = left + '**' + score + '**' + right

assert [id for s in result for id in s['legacy_ids']] == [f'CH4-{i}' for i in range(1,715)]
(TRANS / '14_chapter_four_reviewed.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Reviewed {len(result)} segments; original IDs 1–714 preserved; {len(merges)} merged groups.')
