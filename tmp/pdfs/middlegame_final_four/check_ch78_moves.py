import sys,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];TMP=Path(__file__).parent
sys.path.insert(0,str(ROOT/'tmp/chessdeps'))
import chess
SAN=r'(?:O-O(?:-O)?|[KQRBN]?[a-h]?[1-8]?x?[a-h][1-8](?:=[QRBN])?[+#?!]*)'
TOKEN=re.compile(r'(?<![A-Za-z0-9])(?:(\d+)\.(\.\.)?\s*)?('+SAN+r')(?![A-Za-z0-9])')
starts7={'12.0':'r3r1k1/2q2ppp/pn1p1bn1/1pp1p3/3PP3/P1P1BNPP/1P2QP2/1B1RR1K1 w - - 0 22',
'30.0':'1r1q2k1/p1pbr1pp/3p1p1n/2p2P2/4P3/1NNQ3P/PPP3P1/4RRK1 w - - 0 17',
'75.0':chess.STARTING_FEN,'117.0':chess.STARTING_FEN,
'181.0':'2r5/r2n2k1/Pp1q4/1QpPp1p1/4Pp1p/2P2P1P/1R2KBP1/R7 w - - 0 40',
'215.0':chess.STARTING_FEN,'240.0':chess.STARTING_FEN,'274.0':chess.STARTING_FEN,'325.0':chess.STARTING_FEN}
b=chess.Board()
for s in 'e4 e5 Nf3 Nc6 Bc4 Bc5 b4 Bxb4 c3 Ba5 d4 d6 O-O Bb6 dxe5 dxe5 Qb3 Qf6 Bd5 Nge7 Bg5 Qg6 Bxe7 Kxe7 Bxc6 Qxc6 Nxe5 Qe6 Qa3+ c5'.split():b.push_san(s)
starts8={'19.0':b.fen(),'53.0':'2rrb1k1/1p2bppp/pqn1p3/8/1P1NB3/P3P3/1B2QPPP/2RR2K1 w - - 0 19',
'85.0':'2br1rk1/pp2ppbp/2p2np1/N2nB3/3P4/2N1PB2/PP3PPP/R4RK1 b - - 0 17','109.0':chess.STARTING_FEN}
for ch,starts in [(7,starts7),(8,starts8)]:
    rows=json.loads((TMP/f'ch{ch}_illustrated_blocks.json').read_text(encoding='utf-8'))
    history={};positions={};errors=[];plies=0;game=0;allhistory={}
    for r in rows:
        if r['key'] in starts:
            game+=1;board=chess.Board(starts[r['key']]);history={board.ply():board.copy()};allhistory[game]=history
        if r['kind']!='moves' or not re.match(r'\d',r['text']):continue
        for m in TOKEN.finditer(r['text']):
            n,d,s=m.groups()
            if n and (int(n)-1)*2+bool(d)!=board.ply():errors.append((r['key'],'number',m[0],board.fen()))
            try:board.push_san(s.strip('!?'));plies+=1;history[board.ply()]=board.copy()
            except ValueError as e:errors.append((r['key'],s,str(e)))
        positions[r['key']]=board.fen()
    checks=[]
    def v(game,move,black,sans):
        b=allhistory[game][(move-1)*2+black].copy()
        try:
            for s in sans.split():b.push_san(s)
            checks.append(dict(game=game,start=move,black=black,line=sans,status='legal'))
        except ValueError as e:
            checks.append(dict(game=game,start=move,black=black,line=sans,error=str(e)));print('VAR',ch,game,move,s,str(e))
    if ch==7:
        v(1,25,0,'Rh1 h5 Nh2 Nf6 Bg5')
        v(1,41,1,'a4 c4 b4 axb4 cxb4 fxe5 Rxe5 Ng4 Re8 e5')
        v(2,28,0,'Nf4 Nh6')
        v(2,31,1,'Nh6 Nxg7')
        v(2,31,1,'Nh6 Rxg7')
        v(2,31,1,'Ne5 Nxe5 dxe5')
        v(2,32,1,'Qe8 Qf4 Ne5 Rh4 Nf7')
        v(2,33,1,'Nh6 Rh4')
        v(2,38,1,'Ne5 Nf4 Nxf3+ Qxf3 Qxf3 Ng6#')
        v(2,38,1,'Ne5 Nf4 Bc8 Rxh7+')
        v(3,18,0,'f5 exf5 Bxf5 Rc7 Rag1 cxd4 cxd4 Kh8')
        v(3,33,1,'g5 fxg5 Nxg5 Ra3 Ne4+ Bxe4 fxe4')
        v(3,33,1,'g5 fxg5 Nxg5 Bb2 Ne4+ Bxe4 fxe4 Rg1+ Rg7 Rxg7+ Kxg7 Ke2')
        v(3,35,1,'Nd6 Ke2 Rf7 Bd2 Kf8 Kf2 Ke7 Kg3 Nf6 Raa1')
        v(3,47,0,'Ba2 Nc6 Rxc4 Nd6')
        v(3,57,0,'Rxf4 R6g2+ Ke3 Re1#')
        v(4,6,1,'h6 Bh4 Bxc3+ bxc3 d6')
        v(4,40,0,'Qxf6 Nd5')
        v(4,47,1,'Rgg8 f5 Nf8 Rxg8+ Kxg8 f6')
        v(4,47,1,'Reg8 f5 f6 Rxg6')
        v(4,48,0,'f5 Ne5 f6 Rg6 Qxf8+ Rxf8 Bxg6 fxg6')
        v(4,56,1,'Rxg2 Rxh7+ Kg8 Qd5+ Ne6 Qxg2+ Ng7 Qg6')
        v(4,57,0,'Rh6 Rxg2 Rxf6')
        v(5,46,0,'d6 Qxd6+ Ke2')
        v(5,61,1,'Rxa6 Rxa6 Rxa6 Ra3 Rxa3 Qxa3')
        v(5,82,1,'Rxa6 Ra3 Rba8 Rba1')
        v(5,82,1,'Kg6 Bxe5 Nxe5 Rxb6 Rxb6 Qxb6 Rxa6')
        v(6,6,0,'d4 exd4 Qxd4 Qxd4 Nxd4')
        v(6,21,0,'Nxf5 Bxf5 Ne2 e4 dxe4 Bxe4 Bf4 Bb7 Rfd1 Qe6 Bxd6 Rxd6 Rxd6 cxd6')
        v(7,11,0,'d4 dxe4 Nxe4 Qxd4 Rd1 Qb6 Rd7 Bf6 c3')
        v(7,18,0,'Nc3 Nec7 Nb1 Rfc8 Nd2 b4 Nb3 Nb5 Be3 Rxc1 Rxc1 Rc8 Rxc8+ Qxc8 d4 Qc6 Bf1 Nac7 h5')
        v(7,19,0,'a3 Nc6 Qd3 Na5')
        v(8,6,1,'g6 Nxc6 bxc6 e5 dxe5 Bxf7+')
        v(8,16,0,'g4 d5 e5 Ne4 Nxe4 dxe4 Be3')
        v(8,17,0,'e5 Nd5 Nxd5 Bxd5 Nf5 exf5 Rxd5 Qe6 Rfd1 f6')
        v(8,18,0,'Rxc3 Nxe4 Rc2 Bd8 Nf3 Nxf2 Qxf2 Bd5')
        v(8,37,1,'h5 h4 Rg4')
        v(9,6,0,'Bg5 h6 Bxf6 Qxf6 e3 O-O Nf3')
        v(9,9,0,'g3 b6 Bg2 Bb7 O-O O-O Rad1')
        v(9,11,0,'g4 Ne4 gxf5 exf5 Rg1 Nxc3 Qxc3 Qf6 Qxf6 Rxf6 O-O-O')
        v(9,12,0,'Bb2 b6 g4 Nxf2 Kxf2 fxg4 Rg1 Qh4+ Ke3 Qh6+ Kd3 gxf3 Rxg7+ Qxg7 Bxg7 Kxg7 exf3 Rxf3+ Ke4 d5+')
        v(9,18,0,'Nd4 e5 Nb5 Qg6 f3')
        v(9,31,0,'Qd2 Bxf3 Nxf3 Nxf3+ Rxf3 Rxf3 Qxg5 Rxf1+ Rxf1 Rxf1+ Kxf1 hxg5 Ke2 Kf7 Kf3 Ke6 Ke4 b5')
    else:
        v(1,19,1,'Rxd5 exd5')
        v(1,19,1,'Ke8 Rab1 Bd7 Qg3 Qg6 Qh4 Qf7 fxe5')
        v(1,19,1,'Ke8 Rab1 Bd7 Qg3 Qg6 Qh4 Kf8 fxe5')
        v(1,20,1,'Rb8 f5 Qh6 f6 Rxd5 exd5 gxf6 Rxb6 axb6 Qa7 Qe3+ Kh1 Qe2 Rc1 Qd2 Rg1')
        v(1,20,1,'Rb8 f5 Qd6 f6 g6 Qe3')
        v(1,22,1,'Kg8 Rh3 Qg5 Rg3 Qh6 f6 g6 Qc3 Be6 f7+ Bxf7 Ne7+')
        v(1,22,1,'Kg8 Rh3 Qg5 Rg3 Qh6 f6 g6 Qc3 Be6 f7+ Bxf7 Nf6 Kf8 Rgf3')
        v(1,22,1,'Kg8 Rh3 Qg5 Rg3 Qh6 f6 g6 Qc3 Be6 f7+ Bxf7 Nf6 Kf8 h3')
        v(1,22,1,'Kg8 Rh3 Qg5 Rg3 Qh6 f6 g6 Qc3 Qh5 f7+ Kh8 Nf6 Qh6 Nxd7 Rxd7 Qxe5+')
        v(1,22,1,'Kg8 Rh3 Qg5 Rg3 Qh6 f6 g6 Qc3 Qh5 f7+ Kf8 Nf6 Qh6 Qxe5 Bc6 Rh3')
        v(1,22,1,'Qd2 Rd3 Qe2 f6 g6 Qc1 Qh5 Nxb6 axb6 Qd2 Ke8 Rd1')
        v(1,22,1,'Qd2 Rd3 Qa5 Qc1')
        v(2,24,0,'Rxc8 Rxc8 Rc1 Rxc1+ Bxc1 e5 Nf5 Qc6 Bd2 Qc2 Be1 Qb1')
        v(2,28,0,'Nf3 Rxc1 Rxc1 Bd1')
        v(2,31,0,'Qg3 Qd7 Nf3')
        v(2,35,0,'Qh5 g6')
        v(2,35,0,'Qf5 Be4')
        v(2,35,0,'Qg3 Bh4 Qh2 f6')
        v(2,36,1,'exf4 Nxf4 Rc1')
        v(2,41,1,'Rg5 Nf4')
        v(3,22,1,'Ne4 Rfc1')
        v(3,24,1,'Bb7 Ne5 Bxe5 Bxe5 Ba6 Rfc1')
        v(3,25,1,'Bxf1 Nxd7 Rd8 Nxb6 Bxg2 Kxg2 axb6 Bc7')
        v(4,7,0,'Qb3 c4 Qxb6 axb6 Be2 b5')
        v(4,8,0,'Ngf3 Be7 O-O O-O Ne5')
        v(4,10,0,'Ngf3 Ng4 Qe2 f5')
        v(4,19,0,'g5 e4 Qg2 Nh5 Bc2 cxd4 cxd4 Nb4')
        v(4,19,1,'Bxe5 g5')
        v(4,21,0,'e4 dxe4 Bxe4 Re7 O-O')
        v(4,24,0,'Ng3 Nd3+')
        v(4,25,0,'Nxd5 Qa6')
        v(4,35,0,'gxf6 Qxf6 Qg3 Bd6 Qf3')
    report=dict(chapter=ch,halfmoves=plies,games=game,errors=errors,positions=positions,analysis_checks=checks)
    print(ch,plies,game,'errors',len(errors))
    for e in errors:print(e)
    (TMP/f'ch{ch}_move_check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
