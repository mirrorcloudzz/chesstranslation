import sys,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'tmp/chessdeps'))
import chess
TMP=Path(__file__).parent
rows=json.loads((TMP/'ch5_illustrated_blocks.json').read_text(encoding='utf-8'))
SAN=r'(?:O-O(?:-O)?|[KQRBN]?[a-h]?[1-8]?x?[a-h][1-8](?:=[QRBN])?[+#?!]*)'
TOKEN=re.compile(r'(?<![A-Za-z0-9])(?:(\d+)\.(\.\.)?\s*)?('+SAN+r')(?![A-Za-z0-9])')
starts={
'262.0':'rnbqr1k1/1pppbppp/p7/3P4/B4B2/2P2N2/P1P2PPP/R2Q1RK1 b - - 0 12',
'334.0':'4n1k1/p1pqbppp/8/4PP2/2Pp1B2/3P4/PrP1Q1NP/5RK1 w - - 0 27',
'347.0':'r4rk1/4bpp1/p4n2/qp6/3BPP1p/3Q3P/P3B1P1/3R1RK1 w - - 0 24',
'462.0':'r1br2k1/qp2npp1/p3pb1p/3n4/1PBPN3/P2QBN2/5PPP/2RR2K1 w - - 0 18'}
board=None;history={};main_errors=[];analysis_issues=[];plies=0;games=0;figure_positions={}
for row in rows:
    text=row['text'];key=row['key']
    if row['kind']=='moves':
        if key=='238.0':continue  # Repeated opening move cited in explanatory text.
        if re.match(r'1\. ',text): board=chess.Board();history={0:board.copy()};games+=1
        if key in starts:board=chess.Board(starts[key]);history={board.ply():board.copy()};games+=1
        if board is None:continue
        for match in TOKEN.finditer(text):
            num,dots,san=match.groups()
            if num:
                ply=(int(num)-1)*2+bool(dots)
                if ply!=board.ply():main_errors.append((key,'number',num,dots,board.fullmove_number,board.turn))
            try:board.push_san(san.strip('!?'));plies+=1;history[board.ply()]=board.copy()
            except ValueError as e:main_errors.append((key,san,str(e)));board=None;break
        if board:figure_positions[row['last_key']]=board.fen()
    elif row['kind']=='body' and board:
        # Diagnostic only: prose sometimes names threats rather than full lines.
        local={k:v.copy() for k,v in history.items()};candidate=None;count=0
        for match in TOKEN.finditer(text):
            num,dots,san=match.groups()
            if num:
                ply=(int(num)-1)*2+bool(dots)
                if candidate is None or candidate.ply()!=ply:
                    candidate=local.get(ply,history.get(ply));candidate=candidate.copy() if candidate else None;count=0
            if candidate is None:continue
            try:candidate.push_san(san.strip('!?'));count+=1;local[candidate.ply()]=candidate.copy()
            except ValueError:
                if count>=2:analysis_issues.append((key,san,count,text))
                candidate=None;count=0
print('Mainline plies',plies,'games/fragments',games,'errors',len(main_errors))
for e in main_errors:print('MAIN',e)
for e in analysis_issues:print('ANALYSIS',e)
(TMP/'ch5_move_check.json').write_text(json.dumps({'plies':plies,'games_and_fragments':games,'main_errors':main_errors,'analysis_diagnostics':analysis_issues,'positions':figure_positions},ensure_ascii=False,indent=2),encoding='utf-8')
