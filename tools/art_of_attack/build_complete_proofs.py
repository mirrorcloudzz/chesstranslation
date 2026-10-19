"""Build all 16 bilingual proofs together from current paired Markdown."""
import argparse
import hashlib
import json
from pathlib import Path
import re

from build_opening_proofs import ROOT, PROJECT, build, parse_file, provenance

DEST=ROOT/'output/pdf/art_of_attack_bilingual_complete'
NAMES=[
 ('front_preface','开篇材料与编者序',1,5),('introduction','导言',6,13),
 ('ch01','第一章：攻击尚未易位的王',14,27),('ch02','第二章：攻击失去易位权利的王',28,50),
 ('ch03','第三章：易位与攻击王城的一般问题',51,65),('ch04','第四章：将杀模式',66,79),
 ('ch05','第五章：杀王焦点',80,120),('ch06','第六章：古典弃象',121,141),
 ('ch07','第七章：攻击易位王时的横线、直线与斜线',142,182),
 ('ch08','第八章：攻击易位王时的棋子与兵',183,230),
 ('ch09','第九章：攻击侧翼出象与长易位的局面',231,246),
 ('ch10','第十章：抵御针对易位王的进攻',247,292),('ch11','第十一章：攻击易位王的各个阶段',293,333),
 ('ch12','第十二章：杀王进攻作为对局整体的一部分',334,349),
 ('players','棋手索引',350,352),('openings','开局索引',352,352),
]


def load_and_check(stem, start, end, figures):
    items=parse_file(stem)
    assert items and len({s['segment_id'] for s in items})==len(items),stem
    if stem.startswith('ch'):
        chapter=int(stem[2:])
        assert [s['segment_id'] for s in items]==[f'CH{chapter}-{i}' for i in range(1,len(items)+1)],stem
    covered={p for s in items for p in range(s['page'],s['page_end']+1)}
    assert covered==set(range(start,end+1)),(stem,'source page coverage',set(range(start,end+1))-covered)
    expected={f['id'] for f in figures.values() if f['section']==stem or (stem=='front_preface' and f['pdf_page']<=5)}
    found=[s['figure_id'] for s in items if s.get('figure_id')]
    assert len(found)==len(set(found)),(stem,'duplicate figure')
    assert expected==set(found),(stem,expected-set(found),set(found)-expected)
    for s in items:
        assert s['text'].strip() and s['zh'].strip(),s['segment_id']
        assert not re.search(r'[\u4e00-\u9fff♔-♟Ω②臭皇]',s['text']),('OCR glyph noise',s['segment_id'])
        if s.get('caption_zh'):assert not re.search('[!?！？]',s['caption_zh']),s['segment_id']
    provenance(items)
    return items


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sections',nargs='+',help='Optional selected sections for incremental generation')
    parser.add_argument('--check-only',action='store_true',help='Validate source and figure coverage without writing')
    parser.add_argument('--version',choices=['v2','v3'],default='v2')
    parser.add_argument('--date',default='2026-10-16')
    args=parser.parse_args()
    figures={f['id']:f for f in json.loads((PROJECT/'figures/manifest.json').read_text(encoding='utf-8'))}
    selected=[c for c in NAMES if not args.sections or c[0] in args.sections]
    if args.sections and set(args.sections)-{c[0] for c in NAMES}:parser.error('Unknown section')
    all_items=[];manifest=[]
    for number,(stem,title,start,end) in enumerate(NAMES):
        if (stem,title,start,end) not in selected:continue
        items=load_and_check(stem,start,end,figures)
        all_items.extend(items)
        print(f'{stem}: {len(items)} segments validated',flush=True)
        if args.check_only:continue
        config=(stem,title,f'原书第{start}—{end}页',f'{number:02d}_{stem}_bilingual_proof_{args.version}.pdf')
        result=build(config,items,figures,output_dir=DEST,version=args.version,date=args.date,
                     zh_label='中文语言校订稿' if args.version=='v3' else '中文初译稿')
        original=Path(result['path']);numbered=DEST/config[-1]
        original.replace(numbered)
        result['path']=numbered.relative_to(ROOT).as_posix()
        result['sha256']=hashlib.sha256(numbered.read_bytes()).hexdigest()
        manifest.append(result)
        print(f'{stem}: {result["pages"]} PDF pages',flush=True)
    if args.check_only:return
    data=PROJECT/'translation'
    suffix=f'complete_{args.version}' if not args.sections else '_'.join(args.sections)+'_'+args.version
    (data/f'segments_{suffix}.json').write_text(json.dumps(all_items,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (data/f'figure_anchors_{suffix}.json').write_text(json.dumps([
        {'figure_id':s['figure_id'],'anchor_segment':s['segment_id'],'caption':s['caption_zh'],'status':s['caption_status']}
        for s in all_items if s.get('figure_id')],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (data/f'proof_manifest_{suffix}.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if not args.sections:
        assert len(manifest)==16
        (DEST/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        rows=['# 国际象棋进攻的艺术全书中英对照校样','',
              f'{args.date} · {args.version}。英文校订稿在左，中文语言校订稿在右。已完成全书语言复核并保留此前确认的订正，供用户继续校对。' if args.version=='v3' else f'{args.date} · {args.version}。英文校订稿在左，中文初译稿在右。包含此前确认的术语与逐段订正，供用户继续校对。',
              '段号保持稳定；索引页码沿用英文原书页码，便于扫描溯源。','',
              '| 部分 | 校样页数 | 对照单元 | 棋图 | 文件 |','| --- | ---: | ---: | ---: | --- |']
        for m in manifest:rows.append(f'| {m["title"]} | {m["pages"]} | {m["segments"]} | {m["figures"]} | [{Path(m["path"]).name}]({Path(m["path"]).name}) |')
        rows+=['',f'生成及核验记录见仓库 `translations/art_of_attack/translation/` 下的 complete_{args.version} 数据与校订记录。',
               '文字、棋谱合法性与版面检查各自记录实际覆盖范围；本校样不是引擎重注本。','']
        if args.version=='v3':rows+=['旧版16份`*_v2.pdf`留在本文件夹原位作为2026-10-16历史校样；上表只列本次有效v3。','']
        (DEST/'README.md').write_text('\n'.join(rows),encoding='utf-8')


if __name__=='__main__':main()
