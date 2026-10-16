"""Merge parallel chapter parts and standardize SAN typography in active drafts."""
import json
from pathlib import Path
import re

FOLDER=Path(__file__).resolve().parents[2]/'translations/art_of_attack/translation'


def merge(stem):
    parts=[FOLDER/f'{stem}_part{i}_v1.md' for i in (1,2)]
    blocks=[];mapping={}
    chapter=int(stem[2:])
    for path in parts:
        chunks=re.split(r'(?m)(?=^## )',path.read_text(encoding='utf-8'))
        for block in chunks:
            if not block.startswith('## '):continue
            old=block[3:].split('|',1)[0].strip()
            new=f'CH{chapter}-{len(blocks)+1}'
            mapping[old]=new
            blocks.append(re.sub(r'^## [^|]+',f'## {new} ',block))
    text=f'# 《国际象棋进攻的艺术》第{chapter}章\n\n'+''.join(blocks)
    for old,new in mapping.items():text=re.sub(r'(?m)^REF: '+re.escape(old)+r'$',f'REF: {new}',text)
    (FOLDER/f'{stem}_v1.md').write_text(text,encoding='utf-8')
    (FOLDER/f'{stem}_assembly_map.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(stem,len(blocks),'segments merged')


def normalize():
    changes=[]
    san=r'(?:O-O-O|O-O|[KQRBN]?[a-h]?[1-8]?x?[a-h][1-8](?:=[QRBN])?)[+#]?[!?]*(?=[\s.,;:!?()（）。，；：\u4e00-\u9fff]|$)'
    for path in [FOLDER/f'{s}_v1.md' for s in ['front_preface','introduction',*[f'ch{i:02}' for i in range(1,13)],'players','openings']]:
        if not path.exists():continue
        raw=path.read_bytes()
        ending='\r\n' if b'\r\n' in raw else '\n'
        lines=raw.decode('utf-8').replace('\r\n','\n').splitlines(keepends=True)
        for index,line in enumerate(lines):
            if not line.startswith(('EN: ','ZH: ','FIG: ')):continue
            before=line
            line=line.replace('0-0-0','O-O-O').replace('0-0','O-O')
            line=re.sub(r'(?<![a-zA-Z0-9_.])(\d{1,3})\s+(?='+san+')',r'\1. ',line)
            line=re.sub(r'(?<![a-zA-Z0-9_.])(\d{1,3})(\.{1,3})[ \t]*(?='+san+')',
                        lambda m:m[1]+('. ' if len(m[2])==1 else '... '),line)
            if before!=line:changes.append({'file':path.name,'line':index+1,'before':before.strip(),'after':line.strip()})
            lines[index]=line
        if any(c['file']==path.name for c in changes):path.write_bytes(''.join(lines).replace('\n',ending).encode('utf-8'))
    if changes:
        path=FOLDER/'san_typography_changes_20261016.json'
        previous=json.loads(path.read_text(encoding='utf-8')) if path.exists() else []
        path.write_text(json.dumps(previous+changes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('SAN typography fields changed:',len(changes))


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--merge',choices=['ch08','ch11'],nargs='*',default=[])
    parser.add_argument('--normalize',action='store_true')
    args=parser.parse_args()
    for stem in args.merge:merge(stem)
    if args.normalize:normalize()
