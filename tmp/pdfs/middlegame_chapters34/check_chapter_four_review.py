import json, re
from collections import Counter
from pathlib import Path
root = Path(str(Path(__file__).resolve().parents[3]))
items = json.loads((root/'translations/chess_middlegame_planning/14_chapter_four_reviewed.json').read_text(encoding='utf-8'))
pat = r'(?<![A-Za-z])(?:[KQRBN][a-h1-8]?x?[a-h][1-8]|[a-h]x[a-h][1-8](?:=[QRBN])?|O-O(?:-O)?)(?![A-Za-z0-9])'
for s in items:
    a = Counter(re.findall(pat, s['text']))
    b = Counter(re.findall(pat, s['zh']))
    if a-b or b-a:
        print(s['segment_id'], 'EN_ONLY', dict(a-b), 'ZH_ONLY', dict(b-a))
print('TERMINOLOGY')
for s in items:
    bad = re.findall(r'棋步|方格|王位|物质优势|材料优势|收回一兵|兵攻|推进到|配偶|……\s*[KQRBNOa-h]|\.{4,}', s['zh'])
    if bad: print(s['segment_id'], bad)
print('ODD ENGLISH')
for s in items:
    bad = re.findall(r'(?<![\w\x27’])\b[b-hj-z]\s+[a-z]{3,}|[（]|\b[a-z]{2,}the\b|\b[0-9]+[A-Za-z]{3,}|\b[A-Za-z]+[0-9][A-Za-z]{2}|\w+- \w+', s['text'])
    if bad: print(s['segment_id'], bad)
    bold_en = re.findall(r'\*\*(.*?)\*\*', s['text'])
    bold_zh = re.findall(r'\*\*(.*?)\*\*', s['zh'])
    if bold_en != bold_zh: print('BOLD_DIFF', s['segment_id'], bold_en, bold_zh)
