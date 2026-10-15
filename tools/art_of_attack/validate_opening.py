"""Legal-move and provenance QA; never substitutes engine analysis for the book."""
import json
import re
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tmp/chessdeps'))
import chess

PROJECT=ROOT/'translations/art_of_attack'
items=json.loads((PROJECT/'translation/segments_v1.json').read_text(encoding='utf-8'))
segments={s['segment_id']:s for s in items}
checks=[]

def san_tokens(value):
    value=re.sub(r'\*\*|\(D\)|\d+\.(?:\.\.)?|[!?]|1-0|0-1|½-½',' ',value)
    return value.split()

def seq(ids):
    return ' '.join(segments[f'CH1-{n}']['text'] for n in ids)

def check(name,text,fen=None):
    board=chess.Board(fen) if fen else chess.Board()
    errors=[]
    annotations=[]
    count=0
    for token in san_tokens(text):
        try:
            move=board.parse_san(token)
            canonical=board.san(move)
            if canonical!=token:annotations.append({'source':token,'canonical_SAN':canonical,'ply':count+1})
            board.push(move);count+=1
        except ValueError as e:
            errors.append({'token':token,'ply':count+1,'error':str(e)})
            break
    checks.append({'name':name,'plies':count,'errors':errors,'SAN_annotation_differences':annotations,'final_fen':board.fen()})
    return board

HANSEN='2kr1b1r/ppp2ppp/2n5/8/3PqBb1/2P2N2/PP1QB1PP/R3K2R b KQ - 0 1'
ANON='r1nqk2r/ppp1bp2/3p2p1/6Bp/3P4/5N2/PPP2PPP/R2QR1K1 w kq - 0 1'
RAVINSKY='2r1kb1r/q2n1ppp/p3p3/1p2n3/5N2/6P1/1PP1QPBP/2BR1RK1 w - - 0 1'
VAREIN='rnb1k2r/pppp1ppp/8/8/1bBPPp2/2N5/PPP1Q1Pq/R1B2KN1 w kq - 0 1'
ASGEIRSSON='r1b1r1k1/1p2qpp1/p1p4p/2Ppn3/1P4n1/P1N1PN2/2Q1BPPP/R3K2R b KQ - 0 1'

check('Meesen–Müller main',seq([10,12,14,16]))
check('Meesen–Müller final mate',seq([10,12,14,16])+' 14. cxd5 Qxe2#')
check('Chigorin–Burn main',seq([20,22])+' 10. Bg5 '+seq([25]))
check('Chigorin–Burn accepting sacrifice',seq([20,22])+' 10. exf5 e4 11. Kd1 exf3 12. Qxf3 Ne5')
check('Hansen–Lundin fragment',seq([28,30])+' 4. Kf2 Bxd2 5. Bxg4+ f5 6. Bxd2 fxg4 7. Rhe1 Qxd4+ 8. Be3 Qxb2+ 9. Kf1 Re8',HANSEN)
check('Unnamed e-file main',seq([34,36,38])+' 4. Re1 Qe6 5. Qb5+ c6 6. Qxb7',ANON)
check('Unnamed e-file castling variation','1. Bf6 O-O 2. Rxe7 Nxe7 3. Qe2 Re8 4. Qd2 Kh7 5. Ng5+ Kg8 6. Ne6 fxe6 7. Qh6 Nf5 8. Qxg6+',ANON)
check('Unnamed e-file king variation','1. Bf6 Rf8 2. Rxe7+ Nxe7 3. Qe2 Kd7 4. Re1 Re8 5. Qb5+ Kc8 6. Qc4 d5 7. Qe2 Kd7 8. Ne5+',ANON)
check('Nunn footnote 1 alternative','1. Bf6 Rf8 2. Qd3 Kd7 3. Qb5+',ANON)
check('Nunn footnote 1 main-line objection','1. Bf6 Rf8 2. Rxe7+ Nxe7 3. Qe2 Qd7 4. Re1 O-O-O 5. Bxe7 Rde8',ANON)
check('Ravinsky–Panov main',seq([43,45,47,49,51,53,55]),RAVINSKY)
check('Ravinsky–Panov alternative mate','1. Rxd7 Nxd7 2. Nxe6 fxe6 3. Qxe6+ Kd8 4. Bg5+ Kc7 5. Qc6+ Kb8 6. Bf4+ Rc7 7. Bxc7+ Qxc7 8. Qa8#',RAVINSKY)
check('Ravinsky–Panov shorter finish',seq([43,45,47,49])+' 7... Kxe7 8. Bg5+ Kd6 9. Qd1+ Kc7 10. Bf4+ Kb6 11. Qd6+ Ka7 12. Qe7+ Rc7 13. Be3+ Kb8 14. Qd8+ Rc8 15. Qb6#',RAVINSKY)
check('Steinitz–Bardeleben main and intended finish',seq([59,61,63,65,66,69,71,72,74,76,78,80]))
check('Steinitz–Bardeleben accepting sacrifice',seq([59,61,63,65,66,69,71])+' 22. Rxe7+ Kxe7 23. Re1+ Kd6 24. Qb4+ Kc7 25. Ne6+ Kb8 26. Qf4+')
check('Steinitz–Bardeleben rook alternative',seq([59,61,63,65,66,69,71])+' 22. Rxe7+ Kxe7 23. Re1+ Kd6 24. Qb4+ Rc5 25. Re6+')
check('Philidor example',seq([85,87,89,91])+' 7... f5 8. Bxb7 e4 9. Qb3 Qxg2 10. Rf1')
check('Keres–Kotov quoted game',seq([95,97])+' 11... Kd8 12. Bg4 Qe5 13. f4 Qxe4 14. Bxd7 Bxd7 15. Nxf6')
check('Keres–Kotov author variation',seq([95,97])+' 11... Nxd5 12. exd5 Qf5 13. Re1+ Ne5 14. f4 g6 15. fxe5 dxe5 16. Qe2 f6')
check('Keres–Kotov Nunn footnote',seq([95,97])+' 11... Nxd5 12. exd5 Qf5 13. Qe1+ Ne5 14. f4 h6 15. fxe5 Qxg5 16. exd6+')
check('Keres–Winter main',seq([103,105,107,109]))
check('Keres–Winter king retreat',seq([103,105])+' 14... Kf8 15. Rfe1 Bd7 16. Qf3+ Kg8 17. Be7 Bxe7 18. Rxe7')
check('Keres–Winter final mate',seq([103,105,107,109])+' 19... Ke8 20. Qe6+ Kf8 21. Bh6#')
check('Varein fragment',seq([112,114]),VAREIN)
check('Asgeirsson–Raud fragment',seq([116,118]),ASGEIRSSON)
check('Réti–Wolf main',seq([122,124,126,128,130,132,134,136]))
check('Réti–Wolf critical variation',seq([122,124,126])+' 15... Nxf2 16. Kxf2 Ng4+ 17. Ke1 Qxe3+ 18. Ne2 Bf5 19. Bxf5 Qf2+ 20. Kd2 Rxe2+ 21. Kc3 Qxc5+')
check('Euwe–Rubinstein main',seq([139,141,143,145,147,149,151,153,155,157,159]))

INTRO7='r1bq1rk1/p2n1ppp/4p3/2pp4/8/PPB1PN2/3P1PPP/R2Q1RK1 w - - 0 1'
INTRO8='r2qr1k1/1b1n1ppp/p1p1p3/1p6/3P4/2P2N2/PPQB1PPP/R3R1K1 w - - 0 1'
INTRO9='8/1K1Q4/6pB/4kB2/3b1n1P/5p2/8/8 b - - 0 1'
INTRO11='8/p5K1/1p2p3/4kp2/1Q6/2PpbP2/1R2n1B1/q7 w - - 0 1'
check('Introduction latent attack','1. d4 Bb7 2. dxc5 Nxc5 3. Qd4',INTRO7)
check('Introduction h7 attack g6','1. Ng5 g6 2. Ne4',INTRO8)
check('Introduction h7 attack Nf6','1. Ng5 Nf6 2. Bf4',INTRO8)
check('Introduction mating pattern Kf6','1... Kf6 2. Bg7#',INTRO9)
check('Introduction mating pattern Ne2','1... Ne2 2. Qe6#',INTRO9)
check('Introduction mating pattern gxf5','1... gxf5 2. Bg7+ Ke4 3. Qxd4#',INTRO9)
check('Introduction focal-point clearance','1. Rxe2 dxe2 2. f4+ Bxf4 3. Qd4#',INTRO11)

report={'checks':checks,'total_checks':len(checks),'total_plies':sum(c['plies'] for c in checks),
        'failed_checks':[c for c in checks if c['errors']],
        'segments':len(items),'figure_count':sum(bool(s.get('figure_id')) for s in items),
        'editor_footnotes':sum(s['kind']=='footnote' for s in items),
        'raw_OCR_unmodified':True,'validation_scope':'Legal moves and scan transcription; no engine evaluation'}
(PROJECT/'translation/chess_validation_v1.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'checks':report['total_checks'],'plies':report['total_plies'],
                  'errors':report['failed_checks'],
                  'annotation_differences':[c for c in checks if c['SAN_annotation_differences']]},ensure_ascii=False,indent=2))
