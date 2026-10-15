"""Assemble OCR preparation artifacts. Does not translate or repair chess moves."""
import json,re,html,hashlib
from collections import Counter
from pathlib import Path
from prepare_art_of_attack import BASE,ROOT,SECTIONS,save,ARCHIVE

def main():
    figures=json.loads((BASE/'figures/manifest.json').read_text(encoding='utf-8'))
    pages={};review=[];excluded=[]
    for file in sorted((BASE/'ocr/raw').glob('page-*.json')):
        p=json.loads(file.read_text(encoding='utf-8')); n=p['pdf_page']; rows=[]
        fs=[f for f in figures if f['pdf_page']==n]
        for i,line in enumerate(p['lines'],1):
            row=dict(line,id=f'AA-p{n:03}-l{i:03}',pdf_page=n)
            x,y,r,b=row['bbox'];cx=(x+r)/2;cy=(y+b)/2
            reason=None
            if n>=3 and cy<200:reason='running_header_or_page_number'
            if any(f['crop_bbox'][0]<=cx<=f['crop_bbox'][2] and f['crop_bbox'][1]<=cy<=f['crop_bbox'][3] for f in fs):reason='inside_figure'
            if reason:
                excluded.append(dict(row,reason=reason));continue
            flags=[]
            if row['confidence'] is not None and row['confidence']<.92:flags.append('low_confidence')
            if re.search(r'[\u4e00-\u9fff]',row['text']):flags.append('unexpected_CJK_likely_figurine_error')
            if re.search(r'\b[a-h][1-8]\b|\d[.．]|[♔-♟]|(?:^|\s)\d{1,3}\s+\S|[O0]-[O0]',row['text']):flags.append('chess_notation_review')
            if re.search(r'\b[a-h]l\b',row['text']):flags.append('possible_file_square_1_l_confusion')
            row['review_flags']=flags
            if flags:review.append(row)
            rows.append(row)
        pages[n]=dict(p,lines=rows)
    sections=[]
    for k,t,a,b in SECTIONS:
        if k=='front':t='Front and back covers'
        if k=='players':b=352
        sections.append(dict(id=k,title=t,pdf_start=a,pdf_end=b,print_start=a if a>=3 else None,print_end=b if a>=3 else None))
    sections[-2]['last_page_region']='y < 1380 in native 1725 x 2475 bitmap'
    sections[-1]['first_page_region']='y >= 1380 in native 1725 x 2475 bitmap'
    save(BASE/'contents.json',sections)
    source_manifest=json.loads((BASE/'source_manifest.json').read_text(encoding='utf-8'))
    source_manifest['note']='Original embedded page bitmaps preserved without resampling, with PDF rotation applied. TOC section starts checked against page images. Pages 1–2 are front/back covers; from page 3, PDF and printed page numbers agree. Page 352 contains both indexes.'
    source_manifest['pages'][-1]['sections']=['players','openings']
    save(BASE/'source_manifest.json',source_manifest)
    toc=['# Art of Attack in Chess — OCR 目录','', '英文原稿准备；未翻译，未逐句校订。保留原始 OCR 行，不自动猜测棋子图标或拼接跨页句子。','', '| 部分 | 原书/PDF页 | 英文OCR | 棋图数 |','| --- | --- | --- | ---: |']
    stats=[]
    for sec in sections:
        k,t,a,b=sec['id'],sec['title'],sec['pdf_start'],sec['pdf_end']
        text=[f'# {t}','', '> 原始英文 OCR 整理稿。换行是扫描行，不是已确认的段落边界；棋谱、脚注及专名须对照页图复核。','']
        plain=[t,''];structured=[]
        for n in range(a,b+1):
            if n not in pages:continue
            rows=pages[n]['lines']
            if n==352:
                rows=[r for r in rows if (r['bbox'][1]<1380 if k=='players' else r['bbox'][1]>=1380)]
            # Index pages have two columns; headings precede column content.
            if n>=350:
                headings=[r for r in rows if 'Index of' in r['text']]
                rest=[r for r in rows if r not in headings]
                rows=headings+sorted(rest,key=lambda r:(r['bbox'][0]>950,r['bbox'][1],r['bbox'][0]))
            else:rows=sorted(rows,key=lambda r:(round(r['bbox'][1]/15),r['bbox'][0]))
            fs=[f for f in figures if f['pdf_page']==n]
            text += [f'## PDF page {n}', '',f'[原页图](../../source_pages/page-{n:03}.png) · [原始OCR坐标](../raw/page-{n:03}.json)','']
            plain += [f'\n[PDF page {n}]']
            events=[(r['bbox'][1],'line',r) for r in rows]+[(f['board_bbox'][1],'figure',f) for f in fs]
            if n<350:events.sort(key=lambda e:e[0])
            for _,kind,r in events:
                if kind=='line':
                    text += [f'<!-- {r["id"]} -->',r['text']+'  ']
                    plain.append(r['text'])
                else:
                    before=[l for l in rows if l['bbox'][3]<=r['board_bbox'][1]]
                    after=[l for l in rows if l['bbox'][1]>=r['board_bbox'][3]]
                    r['preceding_ocr_lines']=[l['id'] for l in before[-3:]]
                    r['following_ocr_lines']=[l['id'] for l in after[:3]]
                    r['anchor_note']='Source-page proximity only; not a verified move/caption. A (D) cue may refer across intervening analysis or a page break.'
                    text += ['',f'![{r["id"]}](../../{r["image"]})','',f'`{r["id"]}` — 原页位置已保留；图注待核定。','']
                    plain.append(f'[{r["id"]}]')
            text.append('');structured.append(dict(pdf_page=n,source_image=f'source_pages/page-{n:03}.png',lines=rows,figure_ids=[f['id'] for f in fs]))
        path=BASE/'ocr/chapters'/k
        path.with_suffix('.md').write_text('\n'.join(text),encoding='utf-8')
        path.with_suffix('.txt').write_text('\n'.join(plain),encoding='utf-8')
        save(path.with_suffix('.json'),dict(section=sec,status='OCR_preparation_not_proofread',pages=structured))
        count=sum(f['section']==k for f in figures)
        toc.append(f'| {t} | {a}–{b} | [{k}](ocr/chapters/{k}.md) | {count} |')
        stats.append(dict(section=k,expected_pages=b-a+1,ocr_pages=len(structured),figures=count))
    toc+=['','第352页上半部仍属棋手索引，下半部是开局索引，已按区域分别归档。','', '棋图原图与来源坐标：[figures/manifest.json](figures/manifest.json)。']
    (BASE/'OCR_INDEX.md').write_text('\n'.join(toc)+'\n',encoding='utf-8')
    save(BASE/'figures/manifest.json',figures)
    save(BASE/'ocr/review_queue.json',review)
    save(BASE/'ocr/excluded_lines.json',excluded)
    missing=[n for n in range(1,353) if n not in pages]
    invalid=[]
    for f in figures:
        from PIL import Image
        im=Image.open(BASE/f['image']);x,y,r,b=f['crop_bbox']
        if im.size!=(r-x,b-y):invalid.append(f['id'])
    assert not invalid,invalid
    save(BASE/'qa/validation.json',dict(ocr_pages=len(pages),missing_pages=missing,figures=len(figures),invalid_crop_dimensions=invalid,partial_boards=sum(f['partial_board'] for f in figures),review_lines=len(review),excluded_lines=len(excluded),sections=stats,source_sha256=hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),text_status='not_manually_proofread',figure_review='All source-page contact sheets and all crop contact sheets visually inspected; exceptional partial boards manually added.'))
    (BASE/'README.md').write_text('# Art of Attack in Chess — 翻译资料\n\n日期：2026-09-30。当前阶段：英文 OCR 与图片准备，尚未翻译。\n\n'
        +f'已保存352张原页图、{len(figures)}张棋图裁片；已完成{len(pages)}/352页 OCR。'+('缺页：'+str(missing) if missing else 'OCR页覆盖完整。')+'\n\n'
        +'入口：[按目录阅读英文 OCR](OCR_INDEX.md) · [准备记录与注意事项](PREPARATION_NOTES.md) · [棋图浏览页](qa/figure_gallery.html) · [检查报告](qa/validation.json)。\n\n'
        +'按目录独立保存了编者序、导言、12章、符号说明和两份索引，另保存封面封底与目录的 OCR。每一部分都有 Markdown、TXT 与坐标 JSON。\n\n'
        +'OCR尚未逐句校勘。棋子图标、主线与变化、专名、脚注和跨页句子需要在翻译时对照原页核校；不能把本资料当成已经准确校订的棋谱。当前图注留空，原页位置及上下文索引已保存。\n\n'
        +'其他两本待译书暂缓，既有资料与 Romanovsky 第一版成品保持不变。\n',encoding='utf-8')
    # A lightweight local gallery for checking crops against their source pages.
    cards=[]
    for f in figures:
        cards.append(f'<article><h3>{f["id"]}</h3><a href="../source_pages/page-{f["pdf_page"]:03}.png"><img loading="lazy" src="../{f["image"]}"></a><p>Source page {f["pdf_page"]}; {f["section"]}; '+('partial board' if f['partial_board'] else 'full board')+'</p></article>')
    (BASE/'qa/figure_gallery.html').write_text('<!doctype html><meta charset="utf-8"><title>Art of Attack — figures</title><style>body{font-family:system-ui;background:#eee}main{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:16px}article{background:white;padding:12px}img{width:100%;height:300px;object-fit:contain}h3{font-size:16px}</style><h1>Art of Attack — source figures</h1><p>Click any crop to inspect its original page.</p><main>'+''.join(cards)+'</main>',encoding='utf-8')
    print(json.dumps(dict(ocr_pages=len(pages),figures=len(figures),missing=missing),ensure_ascii=False))

if __name__=='__main__':main()
