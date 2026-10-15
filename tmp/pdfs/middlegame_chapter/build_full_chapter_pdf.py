import html
import math
import re
from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(r"C:\Users\12059\Documents\Codex\chess")
TRANSLATIONS = ROOT / "translations" / "chess_middlegame_planning"
DIAGRAMS = ROOT / "tmp" / "pdfs" / "middlegame_chapter" / "diagrams"
OUTPUT = ROOT / "output" / "pdf" / "chess_middlegame_planning_chapter_planning_zh_proof_v8.pdf"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

pdfmetrics.registerFont(TTFont("CN", r"C:\Windows\Fonts\msyh.ttc", subfontIndex=0))
pdfmetrics.registerFont(TTFont("CNBold", r"C:\Windows\Fonts\msyhbd.ttc", subfontIndex=0))
pdfmetrics.registerFont(TTFont("Mono", r"C:\Windows\Fonts\consola.ttf"))
pdfmetrics.registerFontFamily("CN", normal="CN", bold="CNBold")

PAGE_W, PAGE_H = A4
INK = colors.HexColor("#202622")
MUTED = colors.HexColor("#69736C")
ACCENT = colors.HexColor("#49675A")
PALE = colors.HexColor("#EEF2EF")
LINE = colors.HexColor("#C9D2CC")


class ChapterDocTemplate(BaseDocTemplate):
    def __init__(self, filename):
        super().__init__(
            filename,
            pagesize=A4,
            leftMargin=24 * mm,
            rightMargin=22 * mm,
            topMargin=22 * mm,
            bottomMargin=21 * mm,
            title="《国际象棋中局计划》· 计划篇章中文排版校样",
            author="Peter Romanovsky / 中文翻译校样",
        )
        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            id="body",
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
        )
        self.addPageTemplates([
            PageTemplate(id="plain", frames=[frame], onPage=self.draw_plain),
            PageTemplate(id="body", frames=[frame], onPage=self.draw_body),
        ])

    def draw_plain(self, canvas, doc):
        canvas.saveState()
        canvas.setFillColor(ACCENT)
        canvas.rect(0, PAGE_H - 8 * mm, PAGE_W, 8 * mm, fill=1, stroke=0)
        canvas.restoreState()

    def draw_body(self, canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.5)
        canvas.line(24 * mm, PAGE_H - 15 * mm, PAGE_W - 22 * mm, PAGE_H - 15 * mm)
        canvas.setFont("CN", 7.8)
        canvas.setFillColor(MUTED)
        canvas.drawString(24 * mm, PAGE_H - 12 * mm, "彼得·罗曼诺夫斯基《国际象棋中局计划》｜计划")
        canvas.drawRightString(PAGE_W - 22 * mm, 12 * mm, str(doc.page))
        canvas.restoreState()


styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    "TitleCN", parent=styles["Title"], fontName="CNBold", fontSize=25,
    leading=34, textColor=INK, alignment=TA_LEFT, spaceAfter=6 * mm,
)
subtitle_style = ParagraphStyle(
    "SubtitleCN", fontName="CN", fontSize=11.5, leading=19, textColor=MUTED,
    alignment=TA_LEFT, spaceAfter=10 * mm,
)
part_style = ParagraphStyle(
    "PartCN", fontName="CNBold", fontSize=24, leading=31, textColor=INK,
    alignment=TA_LEFT, spaceAfter=5 * mm,
)
part_sub_style = ParagraphStyle(
    "PartSubCN", fontName="CN", fontSize=11, leading=18, textColor=MUTED,
    alignment=TA_LEFT,
)
section_style = ParagraphStyle(
    "SectionCN", fontName="CNBold", fontSize=17.5, leading=25, textColor=INK,
    alignment=TA_LEFT, spaceBefore=2 * mm, spaceAfter=6 * mm,
)
game_heading_style = ParagraphStyle(
    "GameHeadingCN", fontName="CNBold", fontSize=12.2, leading=18,
    textColor=ACCENT, alignment=TA_LEFT, spaceBefore=4 * mm,
    spaceAfter=2.5 * mm, keepWithNext=True,
)
body_style = ParagraphStyle(
    "BodyCN", fontName="CN", fontSize=10.4, leading=18.2, textColor=INK,
    alignment=TA_JUSTIFY, firstLineIndent=20.8, spaceAfter=3.2 * mm,
    wordWrap="CJK", allowWidows=0, allowOrphans=0,
)
move_style = ParagraphStyle(
    "MoveCN", parent=body_style, fontName="CN", firstLineIndent=0,
    leftIndent=4 * mm, rightIndent=3 * mm, spaceBefore=0.8 * mm,
    spaceAfter=3.2 * mm,
)
bullet_style = ParagraphStyle(
    "BulletCN", parent=body_style, firstLineIndent=0, leftIndent=7 * mm,
    bulletIndent=2 * mm, spaceAfter=1.8 * mm,
)
caption_style = ParagraphStyle(
    "CaptionCN", fontName="CN", fontSize=7.7, leading=11, textColor=MUTED,
    alignment=TA_CENTER, spaceBefore=1.2 * mm,
)
toc_head_style = ParagraphStyle(
    "TocHead", fontName="CNBold", fontSize=17, leading=24, textColor=INK,
    spaceAfter=5 * mm,
)
toc_style = ParagraphStyle(
    "Toc", fontName="CN", fontSize=10.5, leading=19, textColor=INK,
    leftIndent=2 * mm,
)


def inline_markup(text):
    text = html.escape(text.strip())
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    return text


def read_blocks(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    blocks = []
    current = []

    def flush():
        if current:
            text = " ".join(part.strip() for part in current).strip()
            if text:
                kind = "move" if re.fullmatch(r"\*\*`[^`]+`\*\*", text) else "p"
                blocks.append((kind, text))
            current.clear()

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# ") or stripped.startswith("状态：") or stripped.startswith("原书范围："):
            flush()
            continue
        if stripped.startswith("## "):
            flush()
            # Segment identifiers are editorial aids and are intentionally omitted from the book proof.
            continue
        if stripped.startswith("### "):
            flush()
            heading = stripped[4:].strip()
            # Paragraph IDs such as CI-1 are editorial aids; named openings are reader-facing headings.
            if not re.fullmatch(r"[A-Z]{2,3}-\d+", heading):
                blocks.append(("heading", heading))
            continue
        if not stripped:
            flush()
            continue
        if stripped == "（见下一幅棋盘图。）":
            flush()
            continue
        if stripped.startswith("- "):
            flush()
            blocks.append(("bullet", stripped[2:].strip()))
            continue
        current.append(stripped.rstrip("  "))
    flush()
    return blocks


def paragraph_for(kind, text):
    markup = inline_markup(text)
    if kind == "heading":
        return Paragraph(markup, game_heading_style)
    if kind == "bullet":
        return Paragraph(markup, bullet_style, bulletText="•")
    if kind == "move":
        return Paragraph(markup, move_style)
    return Paragraph(markup, body_style)


def diagram_card(name, caption_text):
    path = DIAGRAMS / name
    with PILImage.open(path) as image:
        width, height = image.size
    target_w = 64 * mm
    target_h = target_w * height / width
    picture = Image(str(path), width=target_w, height=target_h)
    flowables = [picture]
    if caption_text:
        flowables.append(Paragraph(caption_text, caption_style))
    table = Table([[flowables]], colWidths=[82 * mm], hAlign="CENTER")
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 1.5 * mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5 * mm),
    ]))
    return table


def figure(name, anchor, caption=""):
    return {"name": name, "anchor": anchor, "caption": caption}


DIAGRAM_SPECS = {
    "02_planning_basic_understanding_zh.md": [
        figure("page-009-diagram-1.png", "白方走。", "白方行棋"),
        figure("page-009-diagram-2.png", "当前局面正属于这一类型。", "白方行棋"),
    ],
    "03_planning_concrete_ideas_zh.md": [
        figure("page-013-diagram-1.png", "3... Bb7 4. Bg5", "白方走完 4. Bg5 后的局面"),
        figure("page-013-diagram-2.png", "10. Qf3 Nc6? 11. Qh3 g6?", "黑方走完 11... g6 后的局面"),
        figure("page-015-diagram-1.png", "14. Rfe1 g6? 15. Bf1 Ng7?", "黑方走完 15... Ng7 后的局面"),
        figure("page-016-diagram-1.png", "27. Rxa5 Na6 28. Qa3 Nab8 29. Ra7 Qc8", "黑方走完 29... Qc8 后的局面"),
        figure("page-017-diagram-1.png", "6... Ngf6 7. O-O Be7 8. b3 O-O 9. Bb2", "白方走完 9. Bb2 后的局面"),
        figure("page-018-diagram-1.png", "10... e4 11. Nd2 Bxe2 12. Qxe2 Bb4!", "黑方走完 12... Bb4 后的局面"),
        figure("page-019-diagram-1.png", "19. Qd3 Rae8 20. Nb1 Ng6 21. Be1?", "白方走完 21. Be1? 后的局面"),
    ],
    "04_planning_dynamics_zh.md": [
        figure("page-022-diagram-1.png", "`9. O-O`", "白方走完 9. O-O 后的局面"),
        figure("page-024-diagram-1.png", "20... c5 21. R4d2 Rxd2 22. Qxd2", "白方走完 22. Qxd2 后的局面"),
        figure("page-025-diagram-1.png", "`10. O-O`", "白方走完 10. O-O 后的局面"),
        figure("page-026-diagram-1.png", "16... Rfd8 17. f4 Be8", "黑方走完 17... Be8 后的局面"),
        figure("page-027-diagram-1.png", "19. Bxf6 Bxf6 20. Nxf6+ gxf6 21. Ne4", "白方走完 21. Ne4 后的局面"),
        figure("page-027-diagram-2.png", "`24... R8d6`", "黑方走完 24... R8d6 后的局面"),
    ],
    "05_planning_harmony_zh.md": [
        figure("page-028-diagram-1.png", "为了说明这一观点，请看下面这个简单局面。"),
        figure("page-029-diagram-1.png", "这一局面出自1929年列宁格勒举行的斯塔尔琴科夫—罗曼诺夫斯基之战。", "斯塔尔琴科夫（白）对罗曼诺夫斯基（黑），黑方行棋"),
        figure("page-031-diagram-2.png", "以下局面取自苏埃京—安托申之战", "苏埃京（白）对安托申（黑），白方行棋"),
        figure("page-031-diagram-1.png", "29... Bh3 30. Qf3 Qe7 31. Kf1 Bg4 32. Qd3 Re8 33. Qd2", "白方走完 33. Qd2 后的局面"),
        figure("page-032-diagram-1.png", "`15. Qxf5 Qc7`", "黑方走完 15... Qc7 后的局面"),
        figure("page-036-diagram-1.png", "16... Nf6 17. Rf2 h5 18. h3 h4 19. Nh1 Kg7 20. Rff1 Nh5", "黑方走完 20... Nh5 后的局面"),
    ],
    "06_squares_weak_points_zh.md": [
        figure("page-038-diagram-1.png", "下面用一个例子说明。", "斯梅斯洛夫（白）对鲁达科夫斯基（黑），白方行棋"),
        figure("page-039-diagram-1.png", "图示局面取自祖巴列夫对鲁宾斯坦一局", "祖巴列夫（白）对鲁宾斯坦（黑），白方行棋"),
    ],
    "07_squares_eternal_knight_zh.md": [
        figure("page-040-diagram-1.png", "此前白方刚走了`18. Qe3`。", "白方走完 18. Qe3 后的局面"),
        figure("page-041-diagram-1.png", "26. Kf1 a4 27. a3 c5 28. Rd2 b5 29. cxb5 Nxb5 30. Be6+ Kg7 31. hxg6 hxg6 32. Kg2 Nd4 33. Bg4 Rfb8", "黑方走完 33... Rfb8 后的局面"),
        figure("page-042-diagram-1.png", "`14. Bg5`", "白方走完 14. Bg5 后的局面"),
        figure("page-043-diagram-1.png", "`19. exd6 cxd6`", "黑方走完 19... cxd6 后的局面"),
        figure("page-043-diagram-2.png", "在布龙斯坦与鲍特维尼克1951年世界冠军赛的第16局中，形成了图示局面。", "布龙斯坦（白）对鲍特维尼克（黑），白方行棋"),
        figure("page-044-diagram-2.png", "`54... Rg8`", "黑方走完 54... Rg8 后的局面"),
        figure("page-044-diagram-1.png", "在特尔普戈夫对布龙斯坦一局", "特尔普戈夫（白）对布龙斯坦（黑），白方行棋"),
        figure("page-045-diagram-1.png", "`42. h5 g5 43. Qf2 Nd4`", "黑方走完 43... Nd4 后的局面"),
    ],
    "08_squares_weak_sixth_rank_zh.md": [
        figure("page-046-diagram-1.png", "皮尔斯伯里对齐果林一局", "皮尔斯伯里（白）对齐果林（黑），白方行棋"),
        figure("page-046-diagram-2.png", "图示局面取自罗曼诺夫斯基对斯莫罗德斯基一局", "罗曼诺夫斯基（白）对斯莫罗德斯基（黑），白方行棋"),
        figure("page-047-diagram-1.png", "36... Ke8 37. Nb6 Rc7 38. Nac4 Bd7 39. Nd6+ Ke7", "黑方走完 39... Ke7 后的局面"),
        figure("page-049-diagram-1.png", "`25... Ne5 26. Bf3 Nd3!`", "黑方走完 26... Nd3 后的局面"),
        figure("page-050-diagram-2.png", "得以围绕白方e4孤兵在中心展开反击。", "黑方走完 24... d5 后的局面"),
        figure("page-050-diagram-1.png", "`27... Qe6 28. Re2 f5 29. Nh1 f4 30. Rd1 d4`", "黑方走完 30... d4 后的局面"),
        figure("page-051-diagram-1.png", "图示局面产生于阿廖欣对米凯纳斯一局", "阿廖欣（白）对米凯纳斯（黑），黑方行棋"),
        figure("page-052-diagram-1.png", "16. Ne2 Nf8 17. a5 b5 18. g3 Rh8 19. Kg2 Kg8 20. Rh1 Kf7 21. Nf4 Rg8 22. b3 Nh7 23. c4 Bd7 24. Rac1 Bf8 25. Be2 Nc8 26. cxd5 cxd5", "黑方走完 26... cxd5 后的局面"),
    ],
    "10_lines_zh.md": [
        figure("page-054-diagram-1.png", "7... f5 8. Qd5", "白方走完 8. Qd5 后的局面"),
        figure("page-055-diagram-1.png", "下面来看几个富有启发性的例子。", "阿廖欣（白）对塔塔科维尔（黑），白方行棋"),
        figure("page-055-diagram-2.png", "`31... Qf3!`", "黑方走完 31... Qf3 后的局面"),
        figure("page-056-diagram-1.png", "`33. Nxf3 Nxf3+ 34. gxf3`", "白方走完 34. gxf3 后的局面"),
        figure("page-056-diagram-2.png", "他的许多对局都建立在这一攻击基础之上。", "施密特（白）对齐果林（黑），白方行棋"),
        figure("page-057-diagram-1.png", "27... Rg6 28. c4 Rg4 29. Bc1 Qc6 30. Rg1 Rh8 31. Rb2 Qf3 32. Nf2", "白方走完 32. Nf2 后的局面"),
        figure("page-057-diagram-2.png", "21. Qd2 d4 22. Ne1 Qe8 23. Nd3 Qc6", "黑方走完 23... Qc6 后的局面"),
        figure("page-059-diagram-1.png", "19. Rf1 Qg4 20. Nd2 Re2 21. Ne4 Qf3 22. Qa5 Rxe4 23. c4", "白方走完 23. c4 后的局面"),
        figure("page-059-diagram-2.png", "图示为白方齐果林第40回合`40. Nf2`后的局面。", "齐果林（白）对塔拉什（黑），黑方行棋"),
        figure("page-060-diagram-1.png", "44... Rxb2 45. g5 hxg5 46. hxg5 Rcc2", "黑方走完 46... Rcc2 后的局面"),
    ],
}


subsections = [
    ("A", "一般原则", "1　基本认识", "02_planning_basic_understanding_zh.md"),
    ("A", "一般原则", "2　具体构想", "03_planning_concrete_ideas_zh.md"),
    ("A", "一般原则", "3　动态性", "04_planning_dynamics_zh.md"),
    ("A", "一般原则", "4　协调性", "05_planning_harmony_zh.md"),
    ("B", "格子", "1　弱点", "06_squares_weak_points_zh.md"),
    ("B", "格子", "2　铁马", "07_squares_eternal_knight_zh.md"),
    ("B", "格子", "3　第六（第三）横线上的弱格", "08_squares_weak_sixth_rank_zh.md"),
    ("B", "格子", "4　若干结论", "09_squares_some_conclusions_zh.md"),
    ("C", "线", "C　线", "10_lines_zh.md"),
]


story = []
story.append(NextPageTemplate("plain"))
story.append(Spacer(1, 33 * mm))
story.append(Paragraph("国际象棋中局计划", title_style))
story.append(Paragraph("计划｜整章中文排版校样", ParagraphStyle(
    "Kicker", fontName="CNBold", fontSize=14, leading=21, textColor=ACCENT,
    alignment=TA_LEFT, spaceAfter=7 * mm,
)))
story.append(Paragraph(
    "彼得·罗曼诺夫斯基 著<br/>中文翻译校样 · 版本 8<br/><br/>本校样收入 A「一般原则」、B「格子」与 C「线」全部译文，并按原书论述顺序配置棋盘图。",
    subtitle_style,
))
story.append(Spacer(1, 18 * mm))
motif = []
for rank in range(4):
    row = []
    for file in range(8):
        row.append("")
    motif.append(row)
board = Table(motif, colWidths=[8 * mm] * 8, rowHeights=[8 * mm] * 4, hAlign="LEFT")
board_cmds = [("GRID", (0, 0), (-1, -1), 0.3, LINE)]
for rank in range(4):
    for file in range(8):
        board_cmds.append(("BACKGROUND", (file, rank), (file, rank), PALE if (file + rank) % 2 == 0 else ACCENT))
board.setStyle(TableStyle(board_cmds))
story.append(board)
story.append(PageBreak())

story.append(NextPageTemplate("body"))
story.append(Paragraph("目录", toc_head_style))
toc_rows = [
    ("A", "一般原则", ["1　基本认识", "2　具体构想", "3　动态性", "4　协调性"]),
    ("B", "格子", ["1　弱点", "2　铁马", "3　第六（第三）横线上的弱格", "4　若干结论"]),
    ("C", "线", ["线：斜线配合、开放线与重子入侵"]),
]
for letter, name, items in toc_rows:
    story.append(Paragraph(f"<b>{letter}　{name}</b>", toc_style))
    for item in items:
        story.append(Paragraph(f"　　{item}", toc_style))
    story.append(Spacer(1, 3 * mm))
story.append(Spacer(1, 7 * mm))
story.append(Paragraph(
    "排版说明：棋谱统一采用现代 SAN。每张棋局图都绑定原版中的具体文字锚点：完整例局按形成局面的最后一步标注，短片段按对局双方与行棋方标注；图片单独居中，并尽量与形成局面的最后一步及其评注安排在同一页。段落编号保留在可编辑译稿中，本书稿校样省略编号。",
    ParagraphStyle("Note", parent=body_style, firstLineIndent=0, textColor=MUTED),
))
story.append(PageBreak())

current_part = None
for part, part_name, section_name, filename in subsections:
    if part != current_part:
        if current_part is not None:
            story.append(PageBreak())
        story.append(NextPageTemplate("body"))
        story.append(Paragraph(f"{part}　{part_name}", part_style))
        current_part = part

    if section_name != f"{part}　{part_name}":
        story.append(Paragraph(section_name, section_style))
    blocks = read_blocks(TRANSLATIONS / filename)
    specs = DIAGRAM_SPECS.get(filename, [])
    placed = set()
    block_index = 0
    while block_index < len(blocks):
        kind, text = blocks[block_index]
        matches = [spec for spec in specs if spec["name"] not in placed and spec["anchor"] in text]
        if len(matches) > 1:
            raise ValueError(f"Multiple diagrams match one block in {filename}: {[item['name'] for item in matches]}")
        if not matches:
            story.append(paragraph_for(kind, text))
            block_index += 1
            continue

        spec = matches[0]
        placed.add(spec["name"])
        cluster = [
            paragraph_for(kind, text),
            Spacer(1, 1.5 * mm),
            diagram_card(spec["name"], spec["caption"]),
            Spacer(1, 2.2 * mm),
        ]
        # Keep the position-forming move, the diagram and the immediately
        # following comment together whenever the resulting cluster fits.
        if block_index + 1 < len(blocks):
            next_kind, next_text = blocks[block_index + 1]
            next_has_figure = any(
                candidate["name"] not in placed and candidate["anchor"] in next_text
                for candidate in specs
            )
            if not next_has_figure:
                cluster.append(paragraph_for(next_kind, next_text))
                block_index += 1
        story.append(KeepTogether(cluster))
        block_index += 1

    missing = [spec["name"] for spec in specs if spec["name"] not in placed]
    if missing:
        raise ValueError(f"Unplaced diagrams in {filename}: {missing}")
    story.append(Spacer(1, 7 * mm))

doc = ChapterDocTemplate(str(OUTPUT))
doc.build(story)
print(OUTPUT)
