"""Legality and SAN checks, not engine evaluation of the author's claims."""
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tmp/chessdeps'))
import chess
from build_opening_proofs import parse_file,PROJECT
items=[s for c in ['ch02','ch03','ch04','ch05'] for s in parse_file(c)]
byid={s['segment_id']:s for s in items}
reports=[]
def tokens(t):
    t=re.sub(r'\d+\.(?:\.\.)?|\(D\)|[!?¹²³⁴*]|1-0|0-1|½-½',' ',t)
    return re.findall(r'O-O-O[+#]?|O-O[+#]?|[KQRBN]?[a-h]?[1-8]?x?[a-h][1-8](?:=[QRBN])?[+#]?',t)
def check(name,t,fen=None):
    b=chess.Board(fen) if fen else chess.Board()
    r={'name':name,'plies':0,'errors':[],'san_differences':[]}
    for token in tokens(t):
        try:m=b.parse_san(token)
        except ValueError as e:
            r['errors'].append({'token':token,'fen':b.fen(),'message':str(e)});break
        actual=b.san(m)
        if actual!=token:r['san_differences'].append({'source':token,'canonical':actual,'fen':b.fen()})
        b.push(m);r['plies']+=1
    r['final_fen']=b.fen();reports.append(r)
    return b
def game(ch,name,ids,extra=''):
    text=' '.join(byid[f'CH{ch}-{i}']['text'] for i in ids)+' '+extra
    return check(name,text)
game(2,'波将金—阿廖欣',[7,9,11,13],'16... Nxd4! 17. gxf5 Nxf5+')
game(2,'克莱门斯—艾森施密特',[17,18,21,23,25,27,29])
game(2,'斯梅斯洛夫—弗洛里安',[45,46,48,50,54,56,58,60])
smyslov=game(2,'斯梅斯洛夫编者注分支起点',[45,46,48],'18... Rh8 19. Qxf7+ Kxg5 20. Qg7! Kf4')
check('斯梅斯洛夫编者注：23. c4+为冲兵',byid['CH2-63']['text'],smyslov.fen())
game(2,'别拉韦涅茨—奇斯佳科夫',[65,67,69,71,74,76,77,79])
game(2,'齐果林—卡罗',[105,108,110,112,113,115,117,119,121,123,126,128,130,132,140,141,143,145,147,149])
game(2,'汉佩—迈特纳',[153,155,157,159,160,163,165,168,170,174,176,178,180])
game(2,'墨菲—巴恩斯',[184,186,188,190,192,194,196,198,200,202,204,206,208,210,213,216,219,221,223])
game(2,'米舍莱—基塞里茨基',[227,229,231,233,234,236,238,240,242])
game(3,'过早短易位示例',[30,32,34,36])
game(3,'塔拉什体系易位示例',[50,52])
game(3,'斯拉夫防御示例',[55,57])
game(3,'格雷科进攻示例',[93,95,98,99,102,104,106,109],'15... Bxd4+ 16. Kxd4 Qxf2+ 17. Kc3 Qe3+ 18. Bd3 Qxe5+')
check('莱加尔杀','1.e4 e5 2.Nf3 d6 3.Bc4 Bg4 4.Nc3 g6 5.Nxe5 Bxd1 6.Bxf7+ Ke7 7.Nd5#')
check('列蒂—塔塔科维尔','1.e4 c6 2.d4 d5 3.Nc3 dxe4 4.Nxe4 Nf6 5.Qd3 e5 6.dxe5 Qa5+ 7.Bd2 Qxe5 8.O-O-O Nxe4 9.Qd8+ Kxd8 10.Bg5+ Kc7 11.Bd8#')
check('安德森—马克斯·朗格',byid['CH4-71']['text'].split('**')[1]+' 10... Bc5+ 11.Kh1 Ng3+ 12.hxg3 Qg5 13.Rf5 h5 14.gxh5 Qxf5 15.g4 Qf2')
game(5,'维戈德奇科夫—阿廖欣',[34,36,38,40,42,43,46,48,50,51,54,56,58,60,61,63])
game(5,'阿廖欣—拉斯克',[65,67,69,70,72,74,76,78,80,83,85])
base=game(5,'默勒尔进攻共同主干',[117,119,121,123])
for label,ids in [('A',[127,129,131,132,134,136,138]),('B',[139,141,143]),('C',[146,148,150]),('D',[152,153,156,159,161,163])]:
    check('默勒尔进攻分支'+label,' '.join(byid[f'CH5-{i}']['text'].split('**')[1] if byid[f'CH5-{i}']['kind']=='paragraph' else byid[f'CH5-{i}']['text'] for i in ids),base.fen())
prefix=byid['CH5-168']['text'].split('**')[1]
check('泰勒—科尔塔诺夫斯基',prefix+' '+' '.join(byid[f'CH5-{i}']['text'] for i in [170,172,174])+' 13... Nd5 14. dxe7 Rxe7 15. Nxd5')
game(5,'雅诺夫斯基咨询棋',[207,209,211,213,215,217,218,220,222])
game(5,'皮尔尼克—纳伊多夫',[384,386,388,391,393,394,396,398,400,403,404,408,410,417,419,421,423,425,427,429,431,433])
fragments=[
 ('g7焦点',[11],'r3r1k1/2p1bppp/pq1pb3/1p5N/4P3/P2Q3P/1PP2PP1/R1BR2K1 w - - 0 1'),
 ('科里亚—卡帕布兰卡',[16,18],'r1br2k1/ppp2pp1/5q1p/4p3/2N1Pn2/2PB4/P1PQ1PPP/R4RK1 b - - 0 1'),
 ('菲尔德—滕纳',[20],'r4rk1/ppp2pp1/7p/2NP3n/2P1p1q1/5bB1/PPP2PPP/RN2QRK1 b - - 0 1'),
 ('波列斯拉夫斯基—乌菲姆采夫',[24,26,28,30],'2k4r/pb3p1p/1q1bpp2/2n5/2P3r1/4BN2/1P1Q1PPP/R2B1RK1 b - - 0 1'),
 ('萨博—科托夫',[97,99],'r1b2rk1/1p2qpp1/p1n1pn1p/6N1/1PB5/P1N1P3/1BQ2PPb/R4R1K w - - 0 1'),
 ('h7弃象示例',[102],'r2q1rk1/1pp3pp/p1nbpp2/3p2P1/3P3P/P1NBP3/1PP1QP2/2KR3R w - - 0 1'),
 ('h2焦点示例',[104,107,109,111,113],'r3k1nr/pppb1Nb1/2np3p/8/1PB1PRpq/2P5/P2P2P1/RNBQ2K1 b kq - 0 1'),
 ('伯恩—E.科恩',[178,180,182],'r3r1k1/1bq1bppp/p3nn2/1p2N1B1/2pP4/2N1P3/PPB1Q1PP/3R1RK1 w - - 0 1'),
 ('卡帕布兰卡—R.伊利亚',[186,189,191,193,195],'b2q1rk1/5ppp/4pnn1/3p2N1/1b3PN1/1P1BP3/1B2Q1PP/5R1K w - - 0 1'),
 ('纳伊多夫—伊夫科夫',[200,202,204],'r1b1r1k1/1p1n2bp/1qpp2p1/p4p2/2PNP1n1/1P5P/P3NPP1/1RBQRBK1 b - - 0 16'),
 ('g7转f7',[233,236,238,241],'r4rk1/pbq2p1p/1p1pp1p1/5P2/2P3P1/PP6/R2Q2P1/1B3R1K w - - 0 1'),
 ('复合焦点Rh1',[244,246,249,251,253,256],'1qr4k/1p3p1p/5p1Q/pP1pbP2/P7/3BP1P1/5KP1/5R2 w - - 0 1'),
 ('萨博—范谢尔廷加',[260,262,264],'r1bn1r1k/1pp2ppp/p7/1n2P3/1qB5/3QNN1P/P4PP1/2R1R1K1 w - - 0 1'),
 ('武科维奇—恩泽林斯',[267,269,272,275,277],'1br2rk1/pb3pp1/1pq1pn1B/8/3P4/P1NB2PP/1P1Q1P2/2RR2K1 w - - 0 1'),
 ('h7/f7示例',[282,290,292,295,297],'r1n2rk1/1b2qpp1/p6p/1p2P3/1P1p4/3B4/1P2QPPP/R1B1R1K1 w - - 0 1'),
 ('弱格网络A',[307,309],'r1r3k1/pp1q1p1p/2n1pBp1/3pP3/2pP4/2P5/PP3PPP/R2QR1K1 b - - 0 1'),
 ('弱格网络B',[311,313,315,317,319],'r1r3k1/pp1q1p1p/2n1pBp1/3pP3/2pP4/2P5/PP3PPP/R2QR1K1 b - - 0 1'),
 ('弱格网络D',[324,326,328],'r1r3k1/pp1q1p1p/2n1pBp1/3pP3/2pP4/2P5/PP3PPP/R2QR1K1 b - - 0 1'),
 ('弱格网络E',[331,333,335,337],'r1r3k1/pp1q1p1p/2n1pBp1/3pP3/2pP4/2P5/PP3PPP/R2QR1K1 b - - 0 1'),
 ('弱格网络h4',[342,344,346,348,350,351,353,355],'r1r3k1/pp1q1p1p/2n1pBp1/3pP3/2pP3P/2P5/PP3PP1/R2QR1K1 b - - 0 1'),
 ('尤伟—弗洛尔',[361,363,365,367,369,371,373,375,376,379,381],'r3rbk1/pp1b1p1p/2p1pBp1/q7/3PP3/5Q2/PP2BPPP/2RR2K1 w - - 0 1'),
]
for name,ids,fen in fragments:
    text=' '.join(byid[f'CH5-{i}']['text'] for i in ids)
    if name=='武科维奇—恩泽林斯':text=text.replace('5. Qh4+','5. Qh4+ Kg8')
    final=check(name,text,fen)
    if name=='尤伟—弗洛尔':
        check('尤伟—弗洛尔末尾回合号校勘','18... Bxh3 19.Rxh3 b5 20.Rc3 b4 21.Rxc6 b3 22.Rb6',final.fen())
result={'scope':'Complete main lines and selected diagram variations; no engine evaluation. All source pages visually reviewed separately.',
        'checks':len(reports),'plies':sum(r['plies'] for r in reports),
        'errors':sum(len(r['errors']) for r in reports),'reports':reports}
(PROJECT/'translation/chess_validation_ch02_05_v1.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({**{k:v for k,v in result.items() if k!='reports'},'issues':[r for r in reports if r['errors'] or r['san_differences']]},ensure_ascii=False,indent=2))
