"""Publish current-version documentation after v3 language and PDF QA pass."""
import hashlib
import json
from pathlib import Path
from build_opening_proofs import PROJECT, ROOT

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(path,text):
    path.write_text(text,encoding='utf-8',newline='\n')

def main():
    data=PROJECT/'translation'
    manifest=read_json(data/'proof_manifest_complete_v3.json')
    qa=read_json(data/'layout_validation_complete_v3.json')
    review=read_json(data/'language_review_complete_20261018.json')
    checks={s['section']:s for s in qa['sections']}
    assert len(manifest)==len(checks)==16 and not review['errors']
    assert len(review['scan_verified_english_exceptions'])==10
    for suffix in ['opening_ch01_03','ch04_06','ch07_09','ch10_indexes','ch11_part2']:
        assert (data/f'REVIEW_NOTES_language_{suffix}_20261018.md').is_file()
    assert (data/'REVIEW_NOTES_visual_complete_v3.md').is_file()
    for m in manifest:
        r=checks[m['section']]
        assert r['ok'] and r.get('rendered_pages')==m['pages']
        assert digest(ROOT/m['path'])==m['sha256']==r['sha256']
    for stem,sha in review['source_sha256'].items():
        assert digest(data/f'{stem}_v1.md')==sha,stem
    pages=sum(m['pages'] for m in manifest)
    figures=sum(m['figures'] for m in manifest)
    units=sum(m['segments'] for m in manifest)
    assert figures==332 and units==3410
    report=f'''# 全书语言复核与v3校样更新

2026-10-18。全书开篇、导言、十二章与两份索引已完成逐单元EN/ZH语言阅读，共{units}单元，并检查图注。修正{review['changed_units']}个单元、{review['changed_fields']}个字段；完整前后文本在[全书修改日志](language_review_complete_20261018.json)。

## 阅读与修改范围

- [开篇至第三章](REVIEW_NOTES_language_opening_ch01_03_20261018.md)：583单元。
- [第四至第六章](REVIEW_NOTES_language_ch04_06_20261018.md)：701单元。
- [第七至第九章](REVIEW_NOTES_language_ch07_09_20261018.md)：945单元。
- [第十章、第十一章前半、第十二章与索引](REVIEW_NOTES_language_ch10_indexes_20261018.md)：990单元。
- [第十一章后半补充复核](REVIEW_NOTES_language_ch11_part2_20261018.md)：191单元。

检查错译、漏译、条件及否定范围、评价强弱、主客体指代、子力交换方向、中文语序和术语一致性。纯棋谱与索引数据也在阅读范围内，但不把其中每一单元都计作语言错误。修改只针对有依据的问题，不追求修改数量。

英文校订稿、稳定段号、来源页、单元类型、图号及脚注归属与v2结构快照逐项比较。英文另有10个单元的转写修正，涉及原书253、256、258、259、260、275、276、282、292及332页：作者姓名乱码、回合号字形、黑方省略号、评注符号、漏括号及间距。均直接查看扫描确认，单独列为明确例外；没有改写原书走法或分析。第332页实际为Ne4!，保留正确中文单叹号，修复英文OCR的重复叹号。原书分析与历史陈述的疑点沿用既有校勘记录，不以语言润色静默改写。棋谱合法性不等于引擎评价。

## PDF及检查

本次有效版本为[统一文件夹目录](../../../output/pdf/art_of_attack_bilingual_complete/README.md)中的16份v3 PDF，共{pages}页、{figures}图。两栏分别为英文校订稿、中文语言校订稿。

- [版面和文字覆盖检查](layout_validation_complete_v3.json)：逐栏文字完整、页面边界、棋图数量及图文锚点均通过，并渲染全部页面。
- [视觉复核](REVIEW_NOTES_visual_complete_v3.md)：按记录查看本次联系图和代表性完整页。
- [棋谱检查](chess_validation_complete_v3.json)：只覆盖明确起始局面的moves单元，保留未验证片段，未使用引擎重评。
- [结构回归](language_review_complete_20261018.json)：记录新源稿SHA-256、受保护字段比较和旧v2 PDF校验值。

原书PDF、原始扫描、原始OCR、棋图及旧v2 PDF保持；新的JSON使用complete_v3名称，旧complete_v2保留历史状态。人工修订仍使用原有稳定文件名的权威Markdown，不重新组装旧part稿。

这是一轮完整语言复核及修订后的人工校对用校样，并非保证全部问题已被穷尽发现的出版定稿。
'''
    write(data/'REVIEW_NOTES_language_complete_20261018.md',report)
    book=PROJECT/'README.md'
    old=book.read_text(encoding='utf-8')
    current,sep,history=old.partition('## 早期v1记录')
    current=current.partition('## 2026-10-18语言复核')[0].replace('v2','v3')
    lines=current.splitlines()
    lines[2]=f'2026-10-18：全书已完成逐单元中英语言复核并修订{review["changed_units"]}个单元。当前为v3中英对照校样，16份PDF、{pages}页、{units}个对照单元、332幅原书棋图，供用户人工校对。'
    current='\n'.join(lines)+'\n\n'
    current+='## 2026-10-18语言复核\n\n- [全书复核报告](translation/REVIEW_NOTES_language_complete_20261018.md) · [完整修改日志](translation/language_review_complete_20261018.json)。\n- v2 PDF及complete_v2数据保留原位作为2026-10-16历史快照；当前入口以上方v3为准。\n\n'
    history=history.replace('当前应用状态以上方v2','当前应用状态以上方v3')
    write(book,current+sep+history)
    p=ROOT/'AGENTS.md';text=p.read_text(encoding='utf-8').replace('v2','v3')
    text=text.replace('全书初译及v3中英对照校样已完成','全书初译、语言复核及v3中英对照校样已完成')
    write(p,text)
    p=ROOT/'docs/HANDOFF.md';text=p.read_text(encoding='utf-8').replace('整理日期：2026-10-16','整理日期：2026-10-18').replace('v2','v3')
    text=text.replace('全书初译、扫描校订与v3中英对照校样已完成','全书初译、扫描校订、语言复核与v3中英对照校样已完成')
    if '语言复核前的历史版本' not in text:
        text=text.replace('## 下一步工作顺序','2026-10-16的16份v2 PDF及complete_v2数据保持原位，作为语言复核前的历史版本。本次修改详情见 `translation/REVIEW_NOTES_language_complete_20261018.md`（相对于当前书目录）。\n\n## 下一步工作顺序')
    write(p,text)
    p=ROOT/'README.md';text=p.read_text(encoding='utf-8').replace('截至 2026-10-16','截至 2026-10-18')
    text=text.replace('全书初译及扫描校订已完成，已应用此前确认的订正，进入全书校对阶段','全书初译、扫描校订及语言复核已完成，已应用此前确认的订正，当前为v3对照校样，进入人工校对阶段')
    text=text.replace('全书初译及对照校样已完成，待用户校对','全书语言复核及v3对照校样已完成，待用户校对')
    write(p,text)
    p=ROOT/'books/README.md';text=p.read_text(encoding='utf-8').replace('当前安排（2026-10-16整理）','当前安排（2026-10-18更新）')
    text=text.replace('全书初译、扫描校订与v2中英对照校样已完成','全书初译、扫描校订、语言复核与v3中英对照校样已完成')
    write(p,text)
    p=data/'USER_CORRECTIONS.md';text=p.read_text(encoding='utf-8').partition('## 2026-10-18 全书语言复核与v3更新')[0].rstrip()+'\n'
    text+='\n## 2026-10-18 全书语言复核与v3更新\n\n- 本次由用户要求进行全书语言检验并更新PDF，已保留此前确认的全部订正。\n- 修改、派生数据、PDF与检查状态见 `REVIEW_NOTES_language_complete_20261018.md`；新有效数据为complete_v3，旧v2保留历史状态。\n'
    write(p,text)
    print(json.dumps({'pdfs':16,'pages':pages,'figures':figures,'units':units,'changed_units':review['changed_units']},ensure_ascii=False))

if __name__=='__main__':main()
