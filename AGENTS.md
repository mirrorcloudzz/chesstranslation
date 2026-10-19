# 项目接续约定

开始工作先阅读根 README、`docs/HANDOFF.md`、当前书 README 和相关用户订正；具体用户指令优先。

- 当前书为 `translations/art_of_attack/`，全书初译、语言复核及v3中英对照校样已完成，接续任务是用户校对。统一校样位于 `output/pdf/art_of_attack_bilingual_complete/`；其他两本待译书暂缓，《中局计划》第一版保留。
- 新章节沿用 `docs/TRANSLATION_RULES.md` 与已确认术语；旧 skill 快照仅作历史参考。
- 日常校对按用户要求记录或改稿；明确要求更新校样后才重做PDF。记录、改稿、派生数据同步、PDF更新状态分别维护。
- 原书、扫描、原始OCR、历史归档不以人工修订覆盖。权威修订入口为开篇、导言、ch01—ch12、players及openings的 `*_v1.md`；全书有效派生数据为 `*_complete_v3.json`。`*_part1/2_v1.md`和早期分批JSON是组稿与历史记录，不反向覆盖合并后的权威稿。
- 不将 `tmp/` 当作可整体清理的缓存，其中有第一版生成脚本、排版数据与历史检查记录。移动资产前检查引用。
- `tools/audit_workspace.py` 默认只读；`--write` 仅刷新 `docs/inventory/`。历史生成器可能改写译稿或说明，执行前先读代码。
- 新增校勘保留稳定段号和来源页。棋谱合法性检查不等于引擎分析，旧报告不自动覆盖新版本。
- 本机依赖、桌面路径与Git仓库分别确认。不得把旧绝对路径视为当前可用路径。
