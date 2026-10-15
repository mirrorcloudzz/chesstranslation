# Art of Attack OCR 准备工具

运行位置：项目根目录 `C:/Users/12059/Documents/Codex/chess`。Python 为 Codex 自带 Python 3.12，项目依赖位于 `tmp/ocrdeps/`。

## 流程

1. `prepare_art_of_attack.py extract`：归档原书，逐页保存原始分辨率页图，应用 PDF 旋转属性。注意这一步会重新写入页图、来源清单与初始目录。
2. `prepare_art_of_attack.py crops`：检测整幅棋盘，并加入本轮人工检查确认的例外裁框，生成332张裁片和检查图。重新运行后必须再次目检；不应直接用于其他书。
3. `ocr_art_of_attack_windows.py`：优先使用 Windows 内置 en-US OCR 处理缺少结果的页面；已有 `ocr/raw/page-NNN.json` 跳过，不覆盖。需 PyWinRT 的 Media.Ocr、Globalization、Graphics.Imaging、Storage、Storage.Streams、Foundation、Foundation.Collections 包。安装 namespace 包时宜一次安装全部，避免 pip --target 的目录合并问题。
4. `prepare_art_of_attack.py ocr --start N --end M`：RapidOCR 备用通道，也跳过已有页。它在本机明显慢于 Windows OCR。
5. `export_art_of_attack.py`：从逐页原始结果重建目录、各章 MD/TXT/JSON、图片上下文索引、检查报告和资料入口。第352页按上下区域分别放入棋手索引和开局索引。

所有 OCR 都是本地处理；无上传操作。Windows OCR 不提供置信度，保留为 null。上述脚本不会翻译，不会将识别到的棋子图标自动修复为 SAN。

输出目录：`translations/art_of_attack/`。已核对原书副本 SHA-256，352页 OCR 齐全，332张棋图（其中17张原书局部棋盘），各图在章节中有唯一引用。

代码重跑可能覆盖生成文件。正式翻译与人工校订应另存，不要直接修改生成的 OCR 文件后又重新运行导出程序。
