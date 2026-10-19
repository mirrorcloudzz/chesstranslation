# 翻译项目接续与迁移说明

整理日期：2026-10-18。当前工作目录为 `D:/Projects/chesstranslation`。历史记录中的 `C:/Users/12059/Documents/Codex/chess` 是旧工作目录；阅读历史记录时将其与本仓库对应，执行脚本前另查代码中的实际路径。

## 当前权威文件

《进攻的艺术》全书初译、扫描校订、语言复核与v3中英对照校样已完成。持续修订入口是 `translations/art_of_attack/translation/` 内的 `front_preface_v1.md`、`introduction_v1.md`、`ch01_v1.md`至`ch12_v1.md`、`players_v1.md`与`openings_v1.md`。当前有效派生数据为 `segments_complete_v3.json`、`figure_anchors_complete_v3.json`及`proof_manifest_complete_v3.json`。所有章节校样统一保存在 `output/pdf/art_of_attack_bilingual_complete/`。

前两批v1 JSON、PDF与报告保留历史状态。`ch08/ch11_part1/2_v1.md`与assembly_map记录并行分稿的衔接，合并后的 `ch08_v1.md`、`ch11_v1.md`才是接续修订入口；不能重新以旧part覆盖合并稿。

《中局计划》早期01—12部分以中文 Markdown 及相应既有排版资料接续；第三、四章以13、14开头的 reviewed JSON 为权威数据；第五至八章以15—18前缀的 reviewed JSON 为准，并核对带图 Markdown 与排版块是否同步。代后记保留19前缀数据。不要用 draft、旧语言修订候选或 archive 数据覆盖当前稿。

第一版 PDF 已保存，历史记录为242页、183图。第六章 `53... Qc2+` 等源稿修订与 PDF 更新状态应继续分别确认；“第一版已保存”不表示后来的订正都已纳入。

2026-10-16的16份v2 PDF及complete_v2数据保持原位，作为语言复核前的历史版本。本次修改详情见 `translation/REVIEW_NOTES_language_complete_20261018.md`（相对于当前书目录）。

## 下一步工作顺序

1. 从统一文件夹的目录选择章节，按v3 PDF中的稳定段号提出校对意见。
2. 阅读当前书README、USER_CORRECTIONS及各章REVIEW_NOTES。此前确认的订正已纳入当前稿和v3；后续意见继续区分记录、改稿与PDF更新。
3. 修改上述权威Markdown，同步全书有效派生数据及图注锚点；原始OCR、扫描、历史PDF保留。
4. 对原书7...Rxd8、313页10...a5等疑点保留校勘依据，区分作者、纳恩编者与译者校勘注；不要用引擎判断静默改写原书。
5. 只有明确要求更新校样时才运行全书生成器与QA。源稿的完整页码覆盖、棋图数量、棋谱合法性、文字覆盖与视觉质量分别验收。
6. 更新交付目录、版本清单及检查记录后再提交Git。全书当前稿是供用户校对的中文初译，不把尚未穷尽的分析分支宣称为全部验证。

## 本机运行准备

项目根目录已建立 `.venv`，使用 Python 3.12.10。已安装并验证 Pillow、NumPy、pypdf、ReportLab、pdfplumber、python-chess、OpenCV、RapidOCR/ONNX Runtime 和 Windows OCR 的 PyWinRT 包。当前校样字体、Poppler、Windows en-US OCR 引擎与 RapidOCR 的空白合成图片推理均检查通过。安装与检查期间未处理实际书页，未生成 PDF。

日常使用以下命令，无需激活环境或修改 PowerShell 执行策略：

```powershell
.\.venv\Scripts\python.exe tools/check_environment.py
.\.venv\Scripts\python.exe tools/audit_workspace.py
.\.venv\Scripts\python.exe -m unittest discover -s tools/tests -v
```

依赖声明在 `requirements.txt`；当前 Windows 环境的完整版本快照在 `requirements-lock.txt`。在另一台 Windows / Python 3.12 机器复现时，先运行 `python -m venv .venv`，再运行 `.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt`。其他平台以 `requirements.txt` 的条件依赖为基础另行验证。Poppler 与 Windows 字体属于本机资源，不包含在 pip 锁文件内。

现有352页 OCR 齐全，续译不需要重新跑 OCR。历史机器翻译实验脚本的外部服务、模型与专用依赖未纳入当前人工翻译及校样工作流。

## 已修复的迁移问题及生成器行为

- `prepare_art_of_attack.py` 已改为默认读取 `books/originals/` 中原书并验证既有 SHA-256，不再依赖 Downloads。确需从其他位置导入同一版原书时用 `extract --source PATH`；源文件缺失或哈希不符时在写入前报错。`tmp/pdfs/` 的同名副本已同步修复。
- 两份 `export_art_of_attack.py` 已改为只在 README 不存在时创建入口，保留已有文件的所有字节；进度与用户规则由人工维护。重复导出保护已有README的行为已用临时目录测试。导出仍会更新生成的OCR、目录与棋图索引，需要时才执行。
- `build_ch02_05_proofs.py` 不只是输出PDF，还会重排并写回章节 Markdown、重建派生JSON；不能将运行生成器当作只读校验。
- Poppler 的脚本硬编码路径已改为共享发现函数：优先 `CHESS_PDFTOPPM` 环境变量，然后 PATH，最后当前用户的 Codex 运行时缓存。当前 Deng 与 Times 字体可用。
- 历史脚本中旧项目目录已改为相对脚本位置计算的仓库路径；涉及旧 Poppler 路径的检查程序也已接入共享发现函数。两批校样检查入口会在内存中转换历史 manifest 路径，不改写已归档JSON。当前书优先使用 `tools/art_of_attack/`；第一版全书复现仍依赖 `tmp/pdfs/build_whole_book.py` 与 `qa_whole_book.py`，不能整体搬走 tmp。
- 桌面交付路径是历史交付约定，不随 Git 自动同步；仓库内交付文件统一从 `output/pdf/` 查找。本次未复制或替换桌面 PDF。
- 仓库保存的是 `chess-book-zh-translation` 的多份历史备份，未发现项目内正式的最新技能文件。继续工作先按项目 README、用户校对记录与 `TRANSLATION_RULES.md` 执行，不将旧快照重新安装为最新版。

## 本次整理范围

新增根入口、接续说明、规则摘要、文件清单与只读检查程序；保留所有既有译稿、图片、PDF与归档的位置和内容。全文件扫描会读取文本并解析JSON、检查Python语法，同时计算所有纳入文件的SHA-256；不等于逐句重译全部正文或逐页重新目检二进制文档。既有棋谱、排版报告保留原检查日期及范围。
