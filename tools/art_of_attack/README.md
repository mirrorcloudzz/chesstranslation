# Art of Attack OCR 准备工具

运行位置：项目根目录（当前为 `D:/Projects/chesstranslation`）。使用 `.venv/Scripts/python.exe`；当前所需依赖已安装，版本记录在根目录 `requirements-lock.txt`。安装与迁移说明见[接续说明](../../docs/HANDOFF.md)。

先运行 `.\.venv\Scripts\python.exe tools/check_environment.py` 检查环境，或运行 `.\.venv\Scripts\python.exe tools/audit_workspace.py` 做文件完整性检查。下列提取、裁图、导出与校样生成步骤会写文件；已有OCR与扫描完整时，继续翻译无需重跑准备流程。导出器只在README不存在时创建入口，已有人工维护内容保持原样；OCR与其他生成资料仍会更新。

## 流程

1. `prepare_art_of_attack.py extract`：默认读取仓库原书并检查SHA-256，逐页保存原始分辨率页图，应用 PDF 旋转属性。若原书尚未归档，可用 `extract --source PATH` 显式导入同一版PDF。注意这一步会重新写入页图、来源清单与初始目录。
2. `prepare_art_of_attack.py crops`：检测整幅棋盘，并加入本轮人工检查确认的例外裁框，生成332张裁片和检查图。重新运行后必须再次目检；不应直接用于其他书。
3. `ocr_art_of_attack_windows.py`：优先使用 Windows 内置 en-US OCR 处理缺少结果的页面；已有 `ocr/raw/page-NNN.json` 跳过，不覆盖。需 PyWinRT 的 Media.Ocr、Globalization、Graphics.Imaging、Storage、Storage.Streams、Foundation、Foundation.Collections 包。安装 namespace 包时宜一次安装全部，避免 pip --target 的目录合并问题。
4. `prepare_art_of_attack.py ocr --start N --end M`：RapidOCR 备用通道，也跳过已有页。它在本机明显慢于 Windows OCR。
5. `export_art_of_attack.py`：从逐页原始结果重建目录、各章 MD/TXT/JSON、图片上下文索引、检查报告和资料入口。第352页按上下区域分别放入棋手索引和开局索引。

所有 OCR 都是本地处理；无上传操作。Windows OCR 不提供置信度，保留为 null。上述脚本不会翻译，不会将识别到的棋子图标自动修复为 SAN。

输出目录：`translations/art_of_attack/`。已核对原书副本 SHA-256，352页 OCR 齐全，332张棋图（其中17张原书局部棋盘），各图在章节中有唯一引用。

## 全书翻译和校样

全书人工修订以 `translation/` 内开篇、导言、ch01—ch12、players与openings的 `*_v1.md` 为准；文件名沿用原有稳定版本名。当前统一校样为 `output/pdf/art_of_attack_bilingual_complete/` 中的v3语言校订版，各章独立PDF；旧v2及其complete_v2数据保留历史状态。

以下命令供明确要求更新校样时使用，需从项目根目录运行：

```powershell
.\.venv\Scripts\python.exe tools/art_of_attack/build_complete_proofs.py --check-only --version v3
.\.venv\Scripts\python.exe tools/art_of_attack/build_complete_proofs.py --version v3 --date 2026-10-18
.\.venv\Scripts\python.exe tools/art_of_attack/qa_complete_proofs.py --version v3
.\.venv\Scripts\python.exe tools/art_of_attack/validate_complete_chess.py --version v3
```

`--sections ch06`等参数可限定生成与检查范围。`qa_complete_proofs.py`逐段核对英文及中文、检查边界与图文同页，并渲染所有页；最终还须查看联系图与代表性完整页。正文中无法从已知局面接续的片段会在棋谱报告中列为未验证，不视为自动通过。

为兼容历史命令，以上工具默认仍为v2；当前工作必须显式传入`--version v3`，不能把默认重跑当作只读检查。v3页面与派生数据另存，统一目录README与manifest指向当前版本。

2026-10-18语言复核记录与各单元修改日志在`translation/REVIEW_NOTES_language_complete_20261018.md`。`check_language_review_20261018.py`比较当前源稿与未修改的v2快照，汇总有理由的变更并检查受保护字段、十处扫描确认的英文转写例外和旧PDF校验值；这是结构回归，不能自动判断语言。`finalize_language_review_20261018.py`仅在对应v3 QA、源稿哈希和视觉记录均齐全后更新接续文档。

`assemble_translation.py`只用于本次并行分稿的组装和SAN格式整理；part文件和assembly_map保留溯源。用户开始修订合并稿后，不应重新合并旧part覆盖当前稿。`apply_confirmed_corrections.py`限定处理此前记录的前五章订正；对应完整逐字段日志已保存。

代码重跑可能覆盖生成文件。正式翻译与人工校订应另存，不要直接修改生成的 OCR 文件后又重新运行导出程序。
