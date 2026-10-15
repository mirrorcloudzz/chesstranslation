# Art of Attack in Chess：翻译准备记录

日期：2026-09-30。本轮仅准备英文原稿和图片，不执行翻译。

## 原书与页码

原始 PDF 为352页扫描件，无可用文本层。第1页是封面，第2页是封底；第3页起，PDF页序与印刷页码一致。按原书目录分为符号说明、John Nunn 编者序、导言、12章、棋手索引和开局索引。棋手索引延续到第352页上半部，开局索引从该页下半部开始。

原书已逐字节复制到 `../../books/originals/`，SHA-256：`888016578278b4b822afbf47600c601b61c4d9958dab0fdbc89280ded83d511a`。

正文页的 PDF 旋转属性为180°。提取内嵌扫描图后已应用该旋转，得到正确朝向；没有缩小原始页图，也没有重绘棋图。

## 文件组织

- `source_pages/`：352张完整原页图，作为一切校核的依据。
- `source_manifest.json`：原书校验值、每页尺寸、旋转处理记录和页图路径。
- `contents.json` / `OCR_INDEX.md`：按目录建立的章节边界与资料入口。
- `ocr/raw/`：逐页原始 OCR，包含每一识别行的坐标、文字及置信度。保留原始结果，不覆盖为猜测的正确招法。
- 识别工具：前批使用 RapidOCR PP-OCRv4，后批使用电脑内置 Windows OCR（en-US）；每页 JSON 的 `engine` 字段记录来源。Windows OCR 不提供置信度，其 `confidence` 为 `null`，不能视为零分或满分。全部处理在本机完成，没有上传书页。
- `ocr/chapters/`：按目录组织的 Markdown、纯文本和 JSON；Markdown在原页纵向位置插入棋图，保留原页链接和稳定行号。
- `ocr/excluded_lines.json`：整理稿中排除的页眉、页码、图内识别噪声；原始结果仍保留。
- `ocr/review_queue.json`：低置信度、异常汉字、可能涉及记谱的识别行。它不是全部错误的清单，高置信度也可能识别错误。
- `figures/`：按章节分目录保存的原始扫描裁片。`manifest.json`记录来源页、棋盘范围、裁剪范围、上下文行号及待定图注。
- `qa/`：全页红框缩略图、裁图片集、图片浏览页和机器检查报告。

## 需要延续的工作方法

1. 本书这一版本包含 John Nunn 的编者序及分析脚注。翻译时必须区分原作者正文、原版编者注和新译者注；不能把编者注擅自并入作者正文。
2. 原书正文棋谱使用棋子图标。普通 OCR 会将它们误识别成数字、字母、中文或直接漏掉。所有主线与分析变化在用于译稿前都须回看原页，转换为现代 SAN 后再检查，不得仅凭置信度视作正确棋谱。
3. 保留扫描行和跨页边界。后续翻译时按语义恢复段落，特别检查正文、主线、变化和脚注之间的关系；不能把分页当作段落结束，也不能把相邻分析变化强行拼接。
4. 棋图直接裁自原扫描，保留左侧 W/B 标记。第四章许多示意图本来就只有部分棋盘且没有下边框，这是原书版式，并非裁切错误；不补画其余棋盘。
5. 本书符号 `(D)` 表示 “see next diagram”。它可能跨过分析文字或分页指向下一张图。图注不能一律取图前最近出现的招法；应先检查 `(D)` 与上下文，再确定准确局面。
6. 当前图片的上下文行号只是位置索引，不是已确认图注。暂不生成 FEN、不猜测走到哪一步、不虚构行棋方；最终中文图注仍按既有规范确定。
7. 图片与其刚走出的招法、下一步注解应尽量同页且邻近；单图居中，不为节约空间把图移远。原书图下的命名（如各种杀王模式的名称）留在文字 OCR 中，之后译为独立图注。
8. 页码、文字内容、图片对应关系和棋谱准确性是不同层面的验收。本轮完成的是资料准备，不等同于逐句校勘或可直接排版出版的定稿。

## 原书符号表的人工核录（原书第4页，英文不翻译）

| Symbol | Meaning |
| --- | --- |
| + | check |
| # | checkmate |
| x | capture |
| !! | brilliant move |
| ! | good move |
| !? | interesting move |
| ?! | dubious move |
| ? | bad move |
| ?? | blunder |
| Ch | championship |
| Ct | candidates event |
| OL | olympiad |
| 1-0 | the game ends in a win for White |
| ½-½ | the game ends in a draw |
| 0-1 | the game ends in a win for Black |
| (n) | nth match game |
| (D) | see next diagram |

## 项目安排

《Art of Attack in Chess》为当前项目。Chernev《Logical Chess Move By Move》及 Przewoznik / Soszynski《How to think in chess》暂缓，已有资料保持不变。Romanovsky 第一版中文成品保持不变。后续沿用 `chess-book-zh-translation` 技能中的中文术语、校订和排版规范，但本书的版本特点以此记录补充。
