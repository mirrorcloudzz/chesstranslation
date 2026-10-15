"""Synchronize the user's explicit terminology and historical corrections."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[3]
TRANS = ROOT / 'translations/chess_middlegame_planning'
TMP = Path(__file__).resolve().parent
old = 'Qf7+，1-0。阿罗宁对弗洛尔一局（原书记作1954年第18届苏联锦标赛），也展示了白方以e、f兵阵突破后，向对方阵地发动的决定性进攻。〔校勘注：原书年份与届次疑不相符，暂照录。〕'
new = 'Qf7+，1-0。1950年第18届苏联锦标赛中阿罗宁对弗洛尔一局，也展示了白方以e、f兵阵突破后，向对方阵地发动的决定性进攻。〔校勘注：原书误作1954年，依用户校对更正为1950年。阿罗宁未参加1954年该项锦标赛，而在1950年的比赛中确曾战胜弗洛尔。〕'
files = list(TRANS.glob('*_zh.md')) + list(TRANS.glob('*reviewed.json'))
files += list(TMP.glob('corrections_*.json'))
files += [TMP/'reviewed_segments.json', TMP/'language_review_candidate.json']
count = 0
for p in files:
    text = p.read_text(encoding='utf-8')
    updated = text.replace('兵潮', '兵风暴').replace(old,new)
    if updated != text:
        if p.suffix=='.json':
            json.loads(updated)
        p.write_text(updated,encoding='utf-8')
        count += 1
        print(p.relative_to(ROOT))
print('Updated',count,'files; historical backups and PDFs unchanged.')
