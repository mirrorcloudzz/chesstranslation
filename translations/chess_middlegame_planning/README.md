# 《国际象棋中局计划》中文翻译

本目录保存可持续修订的章节译稿。PDF 校对稿位于 `../../output/pdf/`。

## 校样 PDF 更新约定

- 桌面文件夹 `C:\Users\12059\Desktop\国际象棋中局计划_最新校样PDF` 保存各完整章节最近一次生成的校样 PDF。
- 日常校对中，用户指出的修改默认只写入译稿、术语规范或排版记录，不重新生成 PDF。
- 只有用户明确要求“更新校样 PDF”或同等含义的操作时，才重新排版、完成视觉检查，并替换桌面文件夹中对应章节的 PDF。
- 桌面文件夹采用完整章节级文件：英译者序与导言、“计划”整章、第一章、第二章；已经被整章校样取代的早期分节校样不重复收录。

## 章节

- [英译者序与导言](01_preface_introduction_zh.md) - 校对中
- [计划 - 一般原则 - 基本认识](02_planning_basic_understanding_zh.md) - 已确认保留
- [计划 - 一般原则 - 具体构想](03_planning_concrete_ideas_zh.md) - 初译校对中
- [计划 - 一般原则 - 动态性](04_planning_dynamics_zh.md) - 初译校对中
- [计划 - 一般原则 - 协调性](05_planning_harmony_zh.md) - 初译校对中
- [格子 - 弱点](06_squares_weak_points_zh.md) - 初译校对中
- [格子 - 铁马](07_squares_eternal_knight_zh.md) - 初译校对中
- [格子 - 第六（第三）横线上的弱格](08_squares_weak_sixth_rank_zh.md) - 初译校对中
- [格子 - 若干结论](09_squares_some_conclusions_zh.md) - 初译校对中
- [线](10_lines_zh.md) - 初译校对中
- [第一章：威廉·斯坦尼茨的两场胜局](11_chapter_one_steinitz_zh.md) - 初译校对中
- [第二章：计划的各个阶段](12_chapter_two_stages_zh.md) - 初译校对中
- [第三章：a线上的战斗](13_chapter_three_a_file_zh.md) - 用户已完成文字校对；已生成含原书10张棋图的中文整章校样v1，待图文排版校对
- [第四章：中心及其战略意义](14_chapter_four_centre_zh.md) - 已依原书印刷页99–142完成整章复核，待用户校对

第三章复核后的中英文权威底稿保存在 `13_chapter_three_reviewed.json`，中英文 Markdown 及后续校样由此同步。后续校对须同步修改该文件，避免被初译清理流程覆盖。误断的段落合并后保留原编号范围（如 CH3-14–15），其他编号不变；原 CH3-158 为孤立 OCR 噪声，已删除并保留空号。详见 `13_chapter_three_review_notes.md`。

第三章带图整章校样采用已校对底稿（包括“英国式开局”修订），14页，保留全部译注。棋图原图及逐图来源、锚点、图注依据保存在 `chapter_three_figures/manifest.json`：前4图采用片段对局信息与行棋方；后6图标注最后一步。末图依据原文“see next diagram”对应38. Bh4后。全部单图居中，与对应文字组合分页，不以节省空间为优先。桌面主文件夹保存整章版，中英对照v2移入“历史版本”保留。

第四章复核后的中英文权威底稿保存在 `14_chapter_four_reviewed.json`，中英文 Markdown 及后续校样由此同步。后续校对须同步修改该文件。95组误断片段合并为原编号范围，599个校对单元覆盖全部714个原编号；原书疑点另加校勘注，详见 `14_chapter_four_review_notes.md`。本次未更新PDF，待用户明确指定时再生成。

Dynamics 的逐段英文 OCR 校正版另存为 [04_planning_dynamics_en_ocr.md](04_planning_dynamics_en_ocr.md)，供双语校对稿调用。
Harmony 的逐段英文 OCR 校正版另存为 [05_planning_harmony_en_ocr.md](05_planning_harmony_en_ocr.md)，供双语校对稿调用。
“格子”四节的逐段英文 OCR 校正版分别另存为 `06` 至 `09` 对应的 `_en_ocr.md` 文件，供双语校对稿调用。
“线”的逐段英文 OCR 校正版另存为 [10_lines_en_ocr.md](10_lines_en_ocr.md)，供校对时回看原文。
第一章和第二章的逐段英文 OCR 校正版分别另存为 [11_chapter_one_steinitz_en_ocr.md](11_chapter_one_steinitz_en_ocr.md) 与 [12_chapter_two_stages_en_ocr.md](12_chapter_two_stages_en_ocr.md)，供中英文对照校样调用。

## 第五至第八章译文复核（2026-09-28）

- [第五章：进一步谈兵的积极行动](15_chapter_five_active_pawns_zh.md)
- [第六章：重子斗争](16_chapter_six_heavy_pieces_zh.md)
- [第七章：调动与主动权](17_chapter_seven_manoeuvring_initiative_zh.md)
- [第八章：双象](18_chapter_eight_two_bishops_zh.md)

已完成四章语言与术语复核，保留原校对编号；中文、英文OCR及对应的 `_reviewed.json` 已同步。后续校样应使用本轮底稿，不可用旧初译后处理流程覆盖。原书疑点、复核范围和备份说明见[本轮复核记录](15-18_language_review_notes_20260928.md)。本次未更新PDF。

## 已确认术语

- `pawn storm`：兵风暴（不再使用“兵潮”）。
- `king's bishop` / `queen's bishop`：按上下文的执棋方译为“白格象”或“黑格象”，避免直译为“王翼象”“后翼象”。白方的 king's bishop 为白格象、queen's bishop 为黑格象；黑方的 king's bishop 为黑格象、queen's bishop 为白格象。须先确认所指一方，不作脱离上下文的统一替换。
- `English Opening`：英国式开局
- `develop the pieces` / `development of pieces`：出子
- `stalemate`：逼和；“逼和”仅用于这一规则术语，其他和棋情形不得使用。
- `force a draw`：强制和棋。
- `He had a draw at hand`：他本可以立即确保和棋。
- `win a piece` / `lose a piece` 及类似表述：得子 / 失子
- `sacrifice`：弃子；可按具体兵种写作“弃兵”“弃马”等
- `blunder of a pawn`：送兵；`blunder of a piece` 及类似表述按具体棋子译为“送子”“送马”“送象”“送车”“送后”等
- `bishop move` / `queen move` / `knight move` / `rook move` 及类似动子表述：动象 / 动后 / 动马 / 动车；例如“这步动象”“这步动后”
- `tempo`：先手；例如 `gain a tempo` 译为“赢得一个先手”，`lose/waste a tempo` 译为“损失/浪费先手”
- `return match`（世界冠军赛中，失去冠军者立即挑战新冠军的回敬赛制）：世界冠军回敬赛
- `a weak move`：一步软着
- `move`：一般译为“步”，不用“着”；仅在“软着”“漏着”“过渡着”等中文国际象棋固定搭配中保留“着”
- 正文避免使用生硬的“棋步”；应结合句意自然写作“步”“走法”“招法”“着法”或直接改写句子。
- `intermediate move`：过渡着
- `win a queen`：得后
- `continuation`：后续手段；结合句法可写作“正确的后续手段”“强制性的后续手段”等
- `eternal knight`：铁马
- `pawn move`（非吃子语境）：冲兵；`pawn advance to e4` 一类表述：冲起e4
- `pawn offensive` / `pawn attack`：兵的攻击
- `castle queenside`：长易位；不译作“后翼易位”
- `handle the pawns` / `handling of pawns`：运用兵；不译作“运兵”，以免产生歧义
- `book reply`：常见谱招
- `opening handbooks`：开局谱
- `break`（以兵冲击对方兵链、打开局面的语境）：冲兵突破；如 `break f3`：f3冲兵突破
- `pawn majority`：结合具体所在翼译为“后翼多兵”或“王翼多兵”；它通常表示一方在该翼的兵数占优，并不等于全盘多一兵
- `material advantage`：子力优势；`material` 涉及棋子数量、价值或子力对比时，按语境译为“子力”“子力得失”等，不译为“物质”
- `position of the king` / `king's position`：王的位置；不缩写为容易产生歧义的“王位”
- `square`：一般译为“格”，不译为“方格”；例如 `a8 square` 译为“a8格”
- `mate in N moves`：N步杀；例如 `mate in three moves` 译为“三步杀”
- 棋谱采用现代 SAN 回合格式：`1. Kf4`、`1... Kf6`、`2. Kg4 Kg6`
- 正文中的招法、棋盘格名称与普通文字统一使用同一套正文字体，不为行内招法另设等宽或其他特殊字体。
- 正文叙述黑棋招法时，以三个英文句点表示黑方行棋，例如“黑方应走...Nbd7”；不得使用中文六点省略号代替。
- 棋谱字重遵循原书层级：原书粗体排出的主线招法在译稿中相应加粗；分析变化及普通行内招法保持常规字重。正文不使用绿色底框区分棋谱。

## 已确认开局名称与区分

- `Nimzo-Indian Defence`：尼姆佐-印度防御，不得译为“尼姆佐维奇防御”。
- “尼姆佐维奇防御”指以`1. e4 Nc6`开始的开局，不与上述开局混淆。
- 按具体对局确认的特殊订正仍保留：CH4-608的“列蒂开局”不因英文原书标题为Nimzo-Indian Defence而改回。

## 已确认人名

- `Tartakower`（用户写作tatakover）：塔塔科维尔
- `Breyer`：布雷耶尔
- `Makogonov`：马卡戈诺夫
- `Taimanov`：泰曼诺夫
- `E. Bogolyubov`：E. 波戈留波夫
- `G. Maroczy`：G. 马洛契
- `M. Chigorin`：M. 齐果林

## 当前采用、待校对术语

已确认地名：`Hastings`统一译为“黑斯廷斯”，不使用“哈斯廷斯”。

- `passed pawn`：通路兵
- `queening square`：升变格
- `dynamics` / `dynamic`：动态性 / 动态的、富于动态性（按句法调整）
- `harmony` / `harmonious operation`：协调性 / 协调行动、协调配合（按句法调整）

## 正文中的对局信息表述

- 对“对局双方—地点—时间”的组合，组织成自然的中文句子，不按英文顺序逐项用逗号拼接。通常采用“某年在某地的甲对乙一局”，并与下文顺畅衔接。
- 例如 `Makogonov-Smyslov, Sverdlovsk 1943, saw a similar plan:` 译为“1943年在斯维尔德洛夫斯克的马卡戈诺夫对斯梅斯洛夫一局，也采用了类似计划：”。
- 此项适用于正文叙述；独立对局信息栏及棋图图注继续遵循各自已有规范。

## 棋局图图注规范

- 短片段局面：按原文标注对局双方、执白执黑以及轮到哪一方行棋，例如：“阿廖欣（白） 对 卡帕布兰卡（黑），白方行棋”。
- 完整例局中的局面图：标注形成该局面的最后一步，例如：“白方走完 `10. e5` 后的局面”。
- 图注所标最后一步中的感叹号、问号及其组合一律省略；正文棋谱中的评注符号保留。将军号与将杀号不属于此处省略的评注符号。
- 图注中的棋手信息、行棋方和最后一步必须能由原文上下文或完整棋谱可靠确认。
- 如果上下文不足，无法确定对局信息、行棋方或局面形成于哪一步，不作推测；保留空白图注位，交由人工校对补充。

## 全书校样（2026-09-28）

### 中文译本第一版成品

- 依用户确认，在全书校样基础上保存第一版成品：`output/pdf/chess_middlegame_planning_zh_first_edition.pdf`；桌面文件为`国际象棋中局计划_中文译本_第一版.pdf`。
- 全书第7页四处漏点记谱改为`1.c4`、`1.d4`、`1.Nf3`、`1.e4`，已同步“基本认识”译稿；此处按用户指定格式，不对其他招法间距作全书替换。
- 所有页眉移除“全书中文校样”及前置分隔符；封面标为“中文译本 · 第一版”。原校样与分章PDF保留不变。
- 第一版仍为242页、183图；两处译注继续隐藏，校勘注保留。全文覆盖检查无差异；全页重新渲染后，除页眉外仅封面和第7页发生视觉变化，目录和其他正文分页不变。
- 复现：`tmp/pdfs/build_whole_book.py --edition`；验证：`tmp/pdfs/qa_whole_book.py --edition`。检查记录位于`tmp/pdfs/whole_book_edition1/`。

- 已按最新译稿重排全书中文带图校样v1，242页、183张棋图，含连续页码、目录及12个章节书签，收录英译者序、导言、计划篇、第一至第八章及代后记。
- 桌面文件：`00_全书_带图中文校样_v1.pdf`；各章独立校样未替换。
- 本版仅在排版层隐藏两处用户提供的译注：“具体构想”中的现代引擎评估说明、CH3-3后的a线斗争与残局说明。源稿及分段校对资料保留原文，便于以后恢复；其他校勘注不隐藏。
- 纳入CH8-37至40的28. Nf6校正，8处图注去除评注符号，正文评注符号保留。
- 全文逐块比对未发现漏文，183张棋图计数一致；完成全页渲染检查。复现排版程序为`tmp/pdfs/build_whole_book.py`，检查记录位于`tmp/pdfs/whole_book/`。

## 第五章当前校样（2026-09-28）

- 整章带图中文底稿：`15_chapter_five_active_pawns_illustrated_zh.md`；本版38页、30张原书棋图。
- 分段修订以`15_chapter_five_active_pawns_reviewed.json`为准，已同步中文稿及合并数据；CH5-348–350、CH5-356–357合并，保留原编号对应关系。
- 本轮断段、OCR、记谱及图注复核说明见`15_chapter_five_illustrated_review_notes.md`。旧的语言修订候选数据不包含本轮修正，不应覆盖当前稿。

## 第六章当前校样（2026-09-28）

- 整章带图中文底稿：`16_chapter_six_heavy_pieces_illustrated_zh.md`；本版20页、14张原书棋图。
- 分段修订以`16_chapter_six_heavy_pieces_reviewed.json`为准，已同步中文稿及合并数据；合并单元保留source_ids，不应以旧候选数据覆盖。
- 断段、记谱与图文复核说明见`16_chapter_six_illustrated_review_notes.md`。v1第14页的记谱疑点已由用户确认为53... Qc2+，文稿已修改，待下次指定更新PDF时纳入。
