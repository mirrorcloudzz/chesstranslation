"""Refresh the project handoff only after the current complete PDFs pass QA."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'translations/art_of_attack'


def main():
    manifest=json.loads((BASE/'translation/proof_manifest_complete_v2.json').read_text(encoding='utf-8'))
    qa=json.loads((BASE/'translation/layout_validation_complete_v2.json').read_text(encoding='utf-8'))
    reports={r['section']:r for r in qa['sections']}
    assert len(manifest)==16 and len(reports)==16
    for m in manifest:
        digest=hashlib.sha256((ROOT/m['path']).read_bytes()).hexdigest()
        assert reports[m['section']]['ok'] and digest==m['sha256']==reports[m['section']]['sha256'],m['section']
    pages=sum(m['pages'] for m in manifest);figures=sum(m['figures'] for m in manifest);units=sum(m['segments'] for m in manifest)
    assert figures==332
    folder='../../output/pdf/art_of_attack_bilingual_complete'
    header=f'''# Art of Attack in Chess 翻译资料

2026-10-16：全书开篇材料、导言、十二章及两份索引的中文初译与扫描校订已完成。当前统一交付为v2中英对照校样，16份PDF、{pages}页、{units}个对照单元、332幅原书棋图，待用户继续校对。

## 当前全书校样与权威稿

- [统一校样文件夹及目录]({folder}/README.md)。所有章节在同一文件夹，各章独立PDF。
- 人工修订入口：`translation/front_preface_v1.md`、`introduction_v1.md`、`ch01_v1.md`至`ch12_v1.md`、`players_v1.md`、`openings_v1.md`。这些是持续修订的源稿，文件名中的v1不代表仍停留在原校样状态。
- [全书结构化数据](translation/segments_complete_v2.json)、[校样清单](translation/proof_manifest_complete_v2.json)、[棋图锚点](translation/figure_anchors_complete_v2.json)。这些是当前有效派生数据；早期分批v1 JSON、PDF及其报告保留历史版本，不替代全书v2。
- [当前版面检查](translation/layout_validation_complete_v2.json)与[视觉复核记录](translation/REVIEW_NOTES_visual_complete_v2.md)。文字覆盖、边界、棋图数量与图文锚点逐项检查；视觉复核按记录的最新渲染范围执行。
- [当前棋谱检查](translation/chess_validation_complete_v2.json)：明确列出可从已知初始局面验证的moves单元、未提供起始局面的片段与未穷尽的正文变化；另见各章校勘记录及第六章独立FEN核验。合法性检查不是引擎评价，不表示所有原书分析结论均正确。
- [用户订正应用记录](translation/USER_CORRECTIONS.md)、[逐字段修改日志](translation/confirmed_corrections_applied_20261016.json)、[SAN格式整理日志](translation/san_typography_changes_20261016.json)。IN-40、古典弃象、positional、人名、开局接受/拒弃兵命名、伊文斯弃兵和盲棋车轮战等已落实至当前稿及v2校样。

352张完整扫描页、352页原始OCR及332张棋图继续独立保存，未以人工校订覆盖。来源入口：[英文OCR目录](OCR_INDEX.md) · [准备记录](PREPARATION_NOTES.md) · [棋图浏览](qa/figure_gallery.html)。

日常校对继续区分记录、改稿、派生数据同步和PDF更新；只有明确要求更新校样时才重新生成。原作者、纳恩编者与译者校勘注分别保留；信息不足的教学图注留空，不猜填。

## 新增校勘记录

- [第六章、第九章及分段范围](translation/REVIEW_NOTES_ch06_ch09.md)
- [第六章示意局面的独立核验](translation/REVIEW_NOTES_ch06_positions.md)：脚注归属、原书7...Rxd8疑点及SAN消歧说明。
- [第七章及第八章前半](translation/REVIEW_NOTES_ch07_ch08.md)
- [第十、十一章](translation/REVIEW_NOTES_ch10_ch11.md)：包括第313页10...a5到10...Na5的显式校勘依据。
- [第十二章与索引](translation/REVIEW_NOTES_ch12_indexes.md)：含图面与(D)提示不一致的处理。

## 早期v1记录

以下保留早期分批交付及2026-10-12、13规则确认的历史背景。其中“尚未改稿”“待应用”等描述属于当时状态；当前应用状态以上方v2及用户订正记录为准。

'''
    previous=(BASE/'README.md').read_text(encoding='utf-8')
    if '## 当前译稿与校样' in previous:history=previous.split('## 当前译稿与校样',1)[1]
    elif '## 早期v1记录' in previous:history=previous.split('## 早期v1记录',1)[1].split('\n\n',2)[-1]
    else:history=''
    (BASE/'README.md').write_text(header+history,encoding='utf-8',newline='\n')
    corrections=BASE/'translation/USER_CORRECTIONS.md'
    text=corrections.read_text(encoding='utf-8')
    text=text.split('## 2026-10-16 通用规范落实',1)[0].rstrip()+'\n'
    text=text.replace('本文件保存待统一应用的逐段订正。一般校对意见只记录；用户指定修改或更新时，再同步权威译稿、派生数据及所要求的PDF。记录状态与“已改稿”“PDF已更新”分别管理。',
        '本文件保存用户确认的逐段订正。2026-10-16已将以下意见应用至权威Markdown、全书结构化数据与统一文件夹的v2对照PDF。今后新增意见继续分别管理记录、改稿和PDF更新状态。')
    text=text.replace('· 待应用','· 已应用至2026-10-16 v2')
    lines=[]
    for line in text.splitlines():
        if line.startswith('- 状态：'):line='- 状态：2026-10-16已改稿、同步全书有效派生数据，并更新统一文件夹内的v2 PDF；旧版PDF保留。'
        lines.append(line)
    lines+=['','## 2026-10-16 通用规范落实','',
            '- 古典弃象、局面棋相关表述、开局名称中的接受/拒弃兵变例已按语境应用至当前有效稿。',
            '- 既有稿36个中文字段的修改详情见confirmed_corrections_applied_20261016.json；新章节术语核对另有记录。',
            '- 全书v2是本次完整交付，早期批次JSON与PDF作为历史快照保留。','']
    corrections.write_text('\n'.join(lines),encoding='utf-8',newline='\n')
    print(json.dumps({'pdfs':16,'pages':pages,'segments':units,'figures':figures},ensure_ascii=False))


if __name__=='__main__':main()
