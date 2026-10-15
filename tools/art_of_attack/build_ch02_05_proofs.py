"""Build the second batch without touching the three existing opening PDFs."""
import argparse
import json
import re
from pathlib import Path
from build_opening_proofs import PROJECT, OUT, parse_file, provenance, build

CONFIGS = [
 ('ch02','第二章：攻击失去易位权利的王','原书第28—50页','03_第二章_攻击失去易位权利的王_中英对照分段校样_v1.pdf'),
 ('ch03','第三章：易位与攻击王城的一般问题','原书第51—65页','04_第三章_易位与攻击王城的一般问题_中英对照分段校样_v1.pdf'),
 ('ch04','第四章：将杀模式','原书第66—79页','05_第四章_将杀模式_中英对照分段校样_v1.pdf'),
 ('ch05','第五章：杀王焦点','原书第80—120页','06_第五章_杀王焦点_中英对照分段校样_v1.pdf'),
]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--chapters', nargs='+', default=[c[0] for c in CONFIGS])
    args=parser.parse_args()
    configs=[c for c in CONFIGS if c[0] in args.chapters]
    items=[]
    for c in configs:
        # Mechanical formatting: ensure stable numerical IDs, not patch insertion order.
        path=PROJECT/'translation'/f'{c[0]}_v1.md'
        parts=re.split(r'(?m)^## ',path.read_text(encoding='utf-8'))
        blocks=sorted(parts[1:],key=lambda b:int(b.split('|',1)[0].strip().split('-')[-1]))
        path.write_text(parts[0]+''.join('## '+b for b in blocks),encoding='utf-8')
        selected=parse_file(c[0])
        assert [s['segment_id'] for s in selected]==[f'CH{int(c[0][-2:])}-{i}' for i in range(1,len(selected)+1)]
        items.extend(selected)
    assert len({s['segment_id'] for s in items})==len(items)
    for s in items:
        assert '棋步' not in s['zh'] and '......' not in s['zh'],s['segment_id']
        assert not re.search(r'[!?]',s.get('caption_zh','')),s['segment_id']
    provenance(items)
    figures={f['id']:f for f in json.loads((PROJECT/'figures/manifest.json').read_text(encoding='utf-8'))}
    expected={f['id'] for f in figures.values() if f['section'] in args.chapters}
    actual=[s['figure_id'] for s in items if s.get('figure_id')]
    assert len(actual)==len(set(actual)), 'Duplicate diagram'
    assert expected==set(actual),(expected-set(actual),set(actual)-expected)
    OUT.mkdir(parents=True,exist_ok=True)
    output=[build(c,items,figures) for c in configs]
    suffix='ch02_05' if len(configs)==4 else '_'.join(c[0] for c in configs)
    folder=PROJECT/'translation'
    (folder/f'segments_{suffix}_v1.json').write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf-8')
    (folder/f'proof_manifest_{suffix}_v1.json').write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf-8')
    (folder/f'figure_anchors_{suffix}_v1.json').write_text(json.dumps([
        {'figure_id':s['figure_id'],'anchor_segment':s['segment_id'],'caption':s['caption_zh'],'status':s['caption_status']}
        for s in items if s.get('figure_id')],ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(output,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
