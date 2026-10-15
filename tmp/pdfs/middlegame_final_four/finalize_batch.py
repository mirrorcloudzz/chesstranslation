import json,hashlib
from pathlib import Path
import pdfplumber
ROOT=Path(__file__).resolve().parents[3];TMP=Path(__file__).parent;TRANS=ROOT/'translations/chess_middlegame_planning'
combined=json.loads((TMP/'reviewed_segments.json').read_text(encoding='utf-8'))
combined=[r for r in combined if r['chapter'] not in (7,8)]
for name in ['17_chapter_seven_manoeuvring_initiative','18_chapter_eight_two_bishops']:
    combined.extend(json.loads((TRANS/(name+'_reviewed.json')).read_text(encoding='utf-8')))
(TMP/'reviewed_segments.json').write_text(json.dumps(combined,ensure_ascii=False,indent=2),encoding='utf-8')
files=[('chapter_five_active_pawns_illustrated_proof_v2',5),('chapter_six_heavy_pieces_illustrated_proof_v2',6),('chapter_seven_manoeuvring_initiative_illustrated_proof_v1',7),('chapter_eight_two_bishops_illustrated_proof_v1',8),('epilogue_bilingual_proof_v1',9)]
report=[]
for slug,ch in files:
    p=ROOT/'output/pdf'/('chess_middlegame_planning_'+slug+'.pdf')
    with pdfplumber.open(p) as d:
        text='\n'.join(x.extract_text() or '' for x in d.pages)
        assert '\ufffd' not in text
        assert '......' not in text
        if ch==5:assert '22... gxf6' in text and '30... g4' in text and '143-174' in text
        if ch==6:assert '53... Qc2+' in text and '黑斯廷斯' in text
        if ch==7:assert '尼姆佐-印度防御' in text and '20. exf3' in text and '9. a3' in text
        if ch==8:assert '17. h3' in text and '26. Qf3 b5' in text and '10. Ngf3' in text
        report.append(dict(chapter=ch,file=str(p),pages=len(d.pages),diagrams=sum(len(x.images) for x in d.pages),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
(TMP/'final_batch_manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
