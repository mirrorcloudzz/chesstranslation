"""Check explicit move blocks from known positions; report every untested block."""
import argparse
import json
import re
from pathlib import Path
import chess

from build_opening_proofs import PROJECT, parse_file

SAN=re.compile(r'(?:O-O-O|O-O|[KQRBN]?[a-h]?[1-8]?x?[a-h][1-8](?:=[QRBN])?)[+#]?[!?]*')


def check_section(stem,seeds):
    states={};known=False;current_game=None
    checked=[];unverified=[];differences=[]
    for item in parse_file(stem):
        if item['kind']=='metadata':
            current_game=item['segment_id'];states={(1,True):[chess.Board()]};known=True
        if item['kind']!='moves':continue
        sid=item['segment_id'];text=item['text']
        clean=re.sub(r'\*\*|\(D\)|1-0|0-1|½-½|¹|²|³|⁴',' ',text).replace('0-0-0','O-O-O').replace('0-0','O-O')
        clean=re.sub(r'(?<![\w.])(\d+)\s+(?=[KQRBN]?[a-h][1-8]|O-O)',r'\1. ',clean)
        start=re.search(r'(\d+)\.(\.\.)?',clean)
        if not start:continue
        key=(int(start[1]),not bool(start[2]))
        if key[0]==1 and sid not in seeds and any(n>1 for n,_ in states):
            # A book diagram often restarts its numbering at 1. It cannot inherit
            # a prior game's initial board merely because an isolated move fits.
            known=False
        if sid in seeds:
            board=chess.Board(seeds[sid]);states={key:[board]};known=True
        tokens=SAN.findall(re.sub(r'\d+\.(?:\.\.)?',' ',clean))
        if not tokens:continue
        candidates=states.get(key,[]) if known else []
        best_error=None;success=None
        for initial in reversed(candidates):
            board=initial.copy();history=[];changes=[]
            try:
                for token in tokens:
                    plain=re.sub('[!?]','',token)
                    move=board.parse_san(plain)
                    canonical=board.san(move)
                    if canonical!=plain:changes.append({'input':plain,'canonical':canonical,'fen':board.fen()})
                    board.push(move);history.append(board.copy())
            except ValueError as exc:
                best_error={'token':token,'fen':board.fen(),'error':str(exc)}
                continue
            success=(history,changes);break
        if success is None:
            unverified.append({'segment':sid,'game':current_game,'text':text,
                               'reason':'no matching legal sequence from available snapshots' if candidates else 'starting position not supplied',
                               'last_error':best_error})
            # Do not silently treat a later partial continuation as independently verified.
            known=False
        else:
            history,changes=success
            for board in history:states.setdefault((board.fullmove_number,board.turn),[]).append(board)
            checked.append({'segment':sid,'plies':len(tokens),'start_fen':initial.fen(),'end_fen':history[-1].fen()})
            if changes:differences.append({'segment':sid,'differences':changes})
    return {'section':stem,'checked_blocks':checked,'unverified_blocks':unverified,'san_differences':differences,
            'plies':sum(c['plies'] for c in checked)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sections',nargs='+',default=[f'ch{i:02}' for i in range(1,13)])
    args=parser.parse_args()
    seeds={}
    for file in (PROJECT/'translation').glob('chess_seeds*.json'):
        data=json.loads(file.read_text(encoding='utf-8'))
        for key,value in data.items():
            if isinstance(value,str):seeds[key]=value
    results=[check_section(stem,seeds) for stem in args.sections]
    result={'scope':'Explicit moves blocks from standard initial positions or manually supplied FEN; prose variations are not exhaustively parsed; no engine evaluation.',
            'sections':results,'plies':sum(r['plies'] for r in results),
            'unverified_blocks':sum(len(r['unverified_blocks']) for r in results),
            'san_differences':sum(len(r['san_differences']) for r in results)}
    suffix='complete_v2' if len(args.sections)==12 else '_'.join(args.sections)+'_v2'
    (PROJECT/'translation'/f'chess_validation_{suffix}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({r['section']:{'blocks':len(r['checked_blocks']),'plies':r['plies'],'unverified':len(r['unverified_blocks']),
                     'san_differences':r['san_differences']} for r in results},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
