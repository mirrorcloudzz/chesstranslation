import re
from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import CondPageBreak, Image, LongTable, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(str(Path(__file__).resolve().parents[3]))
WORK = ROOT / "tmp" / "pdfs" / "middlegame_concrete_ideas"
SOURCE_MD = ROOT / "translations" / "chess_middlegame_planning" / "03_planning_concrete_ideas_zh.md"
OUTPUT = ROOT / "output" / "pdf" / "chess_middlegame_planning_concrete_ideas_zh_proof_v8.pdf"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

pdfmetrics.registerFont(TTFont("Deng", r"C:\Windows\Fonts\Deng.ttf"))
pdfmetrics.registerFont(TTFont("DengBold", r"C:\Windows\Fonts\Dengb.ttf"))

NAVY = colors.HexColor("#15324A")
TEAL = colors.HexColor("#28756B")
PALE = colors.HexColor("#F2F6F5")
PALE_BLUE = colors.HexColor("#EFF4F8")
MID = colors.HexColor("#B9C7CF")
TEXT = colors.HexColor("#1F2933")
MUTED = colors.HexColor("#5B6770")

styles = getSampleStyleSheet()
cover_title = ParagraphStyle("CoverTitle", parent=styles["Title"], fontName="DengBold", fontSize=24, leading=33, textColor=NAVY, alignment=TA_CENTER, spaceAfter=12, wordWrap="CJK")
cover_subtitle = ParagraphStyle("CoverSubtitle", parent=styles["Normal"], fontName="Deng", fontSize=14, leading=22, textColor=TEAL, alignment=TA_CENTER, wordWrap="CJK")
section_title = ParagraphStyle("SectionTitle", parent=styles["Heading1"], fontName="DengBold", fontSize=18, leading=24, textColor=NAVY, spaceAfter=10, wordWrap="CJK")
section_note = ParagraphStyle("SectionNote", parent=styles["Normal"], fontName="Deng", fontSize=9, leading=14, textColor=MUTED, spaceAfter=10, wordWrap="CJK")
table_head = ParagraphStyle("TableHead", parent=styles["Normal"], fontName="DengBold", fontSize=10, leading=14, textColor=colors.white, alignment=TA_CENTER, wordWrap="CJK")
eng_style = ParagraphStyle("English", parent=styles["BodyText"], fontName="Times-Roman", fontSize=8.3, leading=11.6, textColor=TEXT, alignment=TA_LEFT)
zh_style = ParagraphStyle("Chinese", parent=styles["BodyText"], fontName="Deng", fontSize=9.1, leading=14.4, textColor=TEXT, alignment=TA_LEFT, wordWrap="CJK")
label_style = ParagraphStyle("Label", parent=styles["Normal"], fontName="DengBold", fontSize=8, leading=10, textColor=TEAL, wordWrap="CJK")
info_style = ParagraphStyle("Info", parent=styles["BodyText"], fontName="Deng", fontSize=10, leading=16.5, textColor=TEXT, wordWrap="CJK")
scan_caption = ParagraphStyle("ScanCaption", parent=styles["Normal"], fontName="DengBold", fontSize=10, leading=14, textColor=NAVY, alignment=TA_CENTER, spaceAfter=7, wordWrap="CJK")


ENGLISH = {
    "CI-1": """The most purposeful, the most well-founded and therefore having the most chances of being successfully realised, are plans at the basis of which lie concrete ideas.

With concrete ideas one should take into account those ideas in which the thoughts of a chessplayer embrace both special-purpose objectives, arising out of real positional considerations, and ways to achieve them, since the latter provides the greatest possible detailing of them.

If, however, the objective chosen is incorrect or the way to achieving it shrouded in a haze, then the idea does not prove to be concrete and almost certainly will be doomed to failure. Not without reason, in chess literature, in such cases one talks of "chasing after shadows".""",
    "CI-2": """It is necessary to distinguish between strategical and tactical ideas.

Strategy - this is the plan as a whole; tactics - separate operations, leading to its fulfilment. If, graphically, a strategical plan is represented in the form of a chain, then tactical ideas make up its links. Tactical ideas are the means of realising a strategical idea.

A concrete strategical idea represents the main overall task in a given stage of the struggle. It is based on the created positional situation ensuing from it and allows a rough mapping out of a path to solve the problems with which one is confronted.

An incorrect choice of the objective should be regarded as a strategical mistake, as also are moves which are in conflict with the projected plan. A tactical mistake is an error in calculation, which overlooks the opponent's reply, all of which makes difficult or absolutely impossible the carrying out of a concrete strategical idea.""",
    "CI-3": """There will be positions in the process of the struggle where it is very difficult to think of a real objective and, consequently, to work out a concrete idea. In such cases one has to be content with a general appraisal of considerations, directing concrete thoughts in the main to a prevention of the opponent's threats, while special-purpose objects of the plan have not come to light and the struggle has not joined the rails of concrete ideas.

Sometimes, in a locked pawn chain, the game through necessity assumes the form of more or less lengthy piece manoeuvres. In such cases the question arises of an approximate form of action, which perhaps is more difficult than even considering a plan. The objective is very hazy or in general absent, while the moves assume either a waiting character or have only a narrow tactical motivation.

The process of play under conditions where there is no concrete object for thought (and consequently there cannot be concrete ideas), often proceeds under the slogan of equilibrium and ends in a drawn outcome. Creatively this process will usually be of little interest, with the ideas of the two sides being colourless.

We examine, in the light of the above-mentioned planned side and concrete ideas, the following game.""",
    "CI-4": """Queen's Indian Defence
White: K. Klaman
Black: V. Smyslov
(15th USSR Championship 1947)

1 d4 Nf6 2 Nf3 b6

Into this move goes a great planning idea, consisting of the creation of strong piece pressure on the central d5 and e4 squares, and, if White does not duly counteract this, then also of the occupation of the e4 square by the knight with a subsequent consolidation of it by ... f5. This sort of set-up, met sometimes in the Dutch Defence, promises Black good attacking prospects on the king's flank.

From the modest opening move with the pawn on the queen's flank, right up to mate of the opponent's king - this is the true range of a creative concrete idea!

3 Nc3

White's plan consists of organising counter-pressure on the e4 square and preparing the move e4. Pawns standing side by side on e4 and d4, in chess theory are called the pawn centre. We will in due course give particular attention to this important positional element. For the present, however, we note that the pawn centre is one of the most powerful forces in the struggle for the central squares and in the majority of cases one can look upon it as a positional achievement. Therefore the threat of constructing a pawn centre usually evokes an appropriate counter-action from the opposite side.

3 ... Bb7 4 Bg5

A difficult and tense moment has been reached already on the 4th move.""",
    "CI-5": """White is ready to carry out his threat (Bxf6 and e4). Black is in a thoughtful mood, whether to prevent this and, if so, in what way. A good method of contending with a pawn centre is by an immediate attack on a central pawn, in the present position - 4 ... c5. If White, in reply to this, exchanges pawns or plays 5 e3, then Black's problem turns out to be solved.

However, White also has at his disposal another possibility - 5 d5 or a preliminary 5 Bxf6 gxf6 (exf6) and once again 6 d5, severely constraining the enemy pieces on the queen's flank. Apparently, these considerations lead Black to thinking about the need to mechanically slow down the advance of the White king's pawn to e4.

4 ... d5?

Though this move also prevents the formation of the pawn centre, it is nevertheless a serious strategical mistake. The fact is that it is in conflict with the planned line, which Black intended with his 2nd and 3rd moves. Black's bishop on b7 becomes inactive and in general the forces of his queen's flank turn out to be cut off from the king's side. In addition to this, it allows an invasion of the enemy knight on e5, since with the move ... d5 he loses control of this square.

White now has at his disposal a concrete plan, a virtually irresistible attack on the opponent's castled position. The immediate course of the game shows how easily and freely White realises his plan.

5 e3 e6 6 Ne5 Be7 7 Bb5+ c6 8 Bd3 c5 9 0-0

On 9 Bb5+ follows 9 ... Kf8 and, in view of the threat ... c4, the White bishop is in danger.

9 ... 0-0?

Straight into White's attack! He should play ... a6, in order to secure the b5 square, and then try to exchange the opponent's centralised knight by ... Nbd7 or ... Nc6. Black has not drawn up a concrete plan of defence and makes routine moves, apparently unaware of all the dangers in his position.

10 Qf3 Nc6? 11 Qh3 g6?""",
    "CI-6": """Near the end; furthermore a tactical oversight, admittedly in a difficult position. After the correct 11 ... Nxe5 12 dxe5 Ne4 13 Bxe4 dxe4 14 Rad1 Qe8, White has an indisputable advantage but it is still a long way for him to victory.

12 Ba6!

A witty and surprising idea, leading to the win of the exchange: 12 ... Qc8 13 Nxc6 Qxc6 14 Bxb7 Qxb7 15 Qh4 Kg7 16 Bh6+ [matters are not changed by 12 ... Bxa6 13 Nxc6 Qe8 14 Nxe7+ Qxe7 15 Qh4 Kg7 16 Bh6+].

However, it must be emphasised that White's idea rested upon the weakening of Black's king's flank by the move ... g6, hence it is in itself quite logical. It completes, as it were, White's whole plan of attack.""",
    "CI-7": """Indian Defence
White: M. Yudovich
Black: K. Klaman
(15th USSR Championship 1947)

1 d4 Nf6 2 Nf3 d6

The immediate aim in this opening system is the advance ... e5, reinforced with the knight from the d7 square, the bishop from g7, and sometimes also the rook from e8.

3 Bf4 Bg4 4 e3 Nbd7 5 Be2 e6?

Black's trouble begins with this move. He surprisingly refrains from realising his plan, which would guarantee him (for example, after 5 ... Bxf3 6 Bxf3 e5 7 Bg5 c6, followed by ... Be7 and ... 0-0) a quite satisfactory position and begins to confine himself to purely "trench" warfare waiting tactics. In the meantime, White, of course, mobilises all his army, preparing a general offensive in the centre.

6 h3 Bh5

Even now it was necessary to go back to the indicated plan. The retreat of the bishop is absolutely pointless.

7 0-0 Be7 8 c4 0-0

Black has obtained a cramped position; one cannot see good prospects of action for the majority of his pieces - both rooks, queen, bishop on h5. But nevertheless, if henceforth he based his play on a concrete idea, it would not be easy for the opponent to realise his plan of attack.

9 Nc3 Ne8?

This retreat lacks concrete purpose and worsens even more the arrangement of Black's pieces. Black cannot well solve the problems confronting him without the advance ... e5. His following play must include preparation for this pawn move.""",
    "CI-8": """Admittedly, after 9 ... Re8 10 Qd2 Bf8 11 Rad1 e5, White obtains the advantage by 12 dxe5 dxe5 13 Nxe5! Nxe5 14 Qxd8 Raxd8 15 Rxd8 Rxd8 16 Bxh5 Nxh5 17 Bxe5, but the continuation 9 ... Bxf3 10 Bxf3 e5 11 Bh2 c6 and only then ... Re8 and ... Bf8 secures Black good chances of resistance.

10 Qd2 f6 11 Rad1 Bf7

Was Black intending to play 11 ... e5 now? This would be a tactical mistake in view of 12 dxe5 fxe5 13 Nxe5! Bxe2 14 Nxd7 Bxf1 15 Qd5+ Kh8 16 Nxf8 Bxc4 17 Ng6+ hxg6 18 Qxc4 with a great positional advantage for White.

12 Bh2 c6 13 e4 Kh8?

Both now and on the following moves he should play ... e5. The well-fortified pawn in the centre would have allowed Black to construct a plan of defence. Instead of this, he waits passively for the opponent's attack. He is not kept waiting long.

14 Rfe1 g6? 15 Bf1 Ng7? 16 c5!

The beginning of a concrete plan, the aim of which is a pawn offensive on the queen's flank.""",
    "CI-9": """16 ... d5

16 ... Qc7 is bad in view of 17 e5! fxe5 18 cxd6 Qxd6 [18 ... Bxd6 leads to the loss of a piece after 19 dxe5] 19 Nxe5 Nxe5 20 Bxe5 Qd8 21 Ne4, and White obtains a strong attack in connection with the threats of Qh6 and Bc4.

17 exd5 exd5 18 b4

The White bishop on h2 rakes the whole board and, in particular, the important c7 and b8 squares on the queen's flank. With support from this bishop, the pawn offensive proves to be very threatening, the more so in that the enemy pieces, as before, are hampered in their movements.

18 ... b5

Otherwise, after b5, White opens the b-file with advantage.

19 a4

White's idea is clear and concrete - to open the a-file, occupy it with heavy pieces and invade the opponent's camp.

19 ... a6 20 axb5 axb5 21 Ra1 Re8 22 Ra2

A typical tactical method for occupying an open line. A prerequisite for this has been created by the fact that White controls greater space on the queen's flank.

22 ... Qc8 23 Rea1 Qb7 24 Qb2 Ne6 25 Ra3 Nc7 26 Ra5! Rxa5

White threatened to win a piece (Bxc7), therefore the exchange is forced.""",
    "CI-10": """27 Rxa5 Na6 28 Qa3 Nab8 29 Ra7 Qc8

The objective has been achieved. The stage approaches for realisation of the advantage.

30 Nxb5

This sacrifice is not the only way to victory. 30 Rc7 Qd8 31 Qa7 is also sufficient.

30 ... cxb5 31 Bxb5 Kg7 32 Bxb8 Nxb8 33 Bxe8 Qxe8 34 b5 Bf8 35 Qe3 Qc8 36 Qf4

White threatens both Ne5, and Ra8 and Qc7.

1:0

A just punishment for his planless play.""",
    "CI-11": """Queen's Gambit
White: I. Bondarevsky
Black: M. Botvinnik
(Match-tournament for absolute champion of USSR 1941)

1 d4 d5 2 Nf3 c6

Here, already on the 2nd move, begins the planning of the game. On 3 c4, Black could take the pawn and defend it later by ... b5. The move 3 Bf4 would allow Black to create pressure on the weakened b2 point, by playing ... Qb6.

3 e3

Usually one of White's tasks in the opening is to create difficulties for the opponent in the development of his pieces. In particular, in many variations of the Queen's Gambit, Black has quite a lot of trouble deploying his forces on the queen's flank.

However, in the present game, White not only does not pretend to hamper the opponent, but also limits the activity of his own pieces on the queen's flank. This allows Black to realise a purposeful plan of play without difficulty.

White's plan is as modest as can be: he will play c4, Nc3, Be2 [or Bd3], 0-0, b3 and Bb2, and only then decide what he can extract from such an arrangement of pieces. Such a self-denial of the initiative cannot be recommended. Both 3 c4 and 3 Bf4 would have prevented Black from feeling as carefree as he does in the game.""",
    "CI-12": """3 ... Bg4 4 c4 e6 5 Nc3

On 5 Qb3, possible is 5 ... Qb6, and it is hard for White to think of a concrete actual plan.

5 ... Nd7 6 Bd3

In three moves White retreats the bishop to e2. If he is not planning to play the move e4 [and that's the way it seems] then the move must be seen as tactical carelessness.

6 ... Ngf6 7 0-0 Be7 8 b3 0-0 9 Bb2

Both sides have completed their initial arrangement of forces in accordance with the intended plans. The middlegame struggle is begun with Black's move - this undoubtedly is an achievement for him. Also telling against White is the fact that his queen's knight, in the present position, would be better deployed not on c3, but on d2.

The main criticism that can be levelled against him is that, in drawing up a plan of development in the opening, he firstly does not sufficiently concretely co-ordinate it with the basic strategical plan and secondly he does not give due consideration to the tactical niceties of the opening. The moves Bd3, Nc3 were made routinely, since the objective in White's opening plan was too vague and dim, his plan turns out to be not very concrete. In this case it was difficult to decide where best to post the bishop - on e2 or d3, the knight - on c3 or d2.""",
    "CI-13": """9 ... e5

A pawn move, leading to exchanges and hence to an opening of the position, which serves as an inevitable introduction to a piece skirmish, and sometimes also to a general battle; it can provoke a sharpening of the game.

Black's decision is prompted by the nature of Botvinnik's style and possibly also considerations of a sporting character.

Another concrete plan here was to play for occupation of the e4 square and the associated gain of space in the centre and on the king's flank. The starting point of this plan would be the move 9 ... Bb4 and if 10 a3, then 10 ... Bxc3 11 Bxc3 Ne4 12 Be1 f5.

10 Be2

White declines to accept the challenge, but the move in the game is not only a retreat but also the beginning of a fine, very concrete plan of counterattack.

The fact is that Black has nothing better now than to advance his e-pawn to e4. The variation 10 ... exd4 11 Nxd4 provokes an exchange of the white-squared bishops and hands over to White a square of invasion for the knight on f5. After 10 ... e4, however, there arises the concrete idea of the dangerous break f3.

This is not the only plan. Also possible is a relaxing of the situation in the centre: 10 cxd5 exd4 11 exd4 Nxd5 12 Nxd5 cxd5, but in this case the pin on the knight f3 and the passive position of the bishop b2 makes a concrete plan of play difficult.""",
    "CI-14": """However, White did not fancy the sharp struggle produced on the way by 10 dxe5 Nxe5 11 Nxd5 (after 11 Be2 Nxf3+ 12 Bxf3 Bxf3 13 Qxf3 dxc4 14 Rad1 Qc8, Black's extra pawn on the queen's flank can imperceptibly prove to be a planned advantage the more the game is simplified) 11 ... Nxf3+ 12 gxf3 Bh3 13 Nxe7+ Qxe7 14 Kh1! (14 Re1 Ne4 15 f4 Rad8 16 Qe2 Rxd3 17 Qxd3 Qe6, and Black wins) 14 ... Bxf1 15 Qxf1, since this entails a certain amount of risk.

10 ... e4 11 Nd2 Bxe2 12 Qxe2 Bb4!

The attention of both opponents is riveted to the e4 point, for the control of which begins a decisive struggle. With his last move Black endeavours not only to exchange the knight c3, but also, by clearing the e-file, to allow his heavy pieces establish communication with this point.

13 a3?

A loss of an important tempo in the struggle for the e4 square.

Admittedly, the break 13 f3 has no strength in view of 13 ... Bxc3 14 Bxc3 Re8, retaining control over the e4 square, while in the event of 15 fxe4 Nxe4 - he has created on it a good base for his pieces.""",
    "CI-15": """However, White has at his disposal another plan consisting of a pawn attack on the king's flank, and a pawn break in the centre if Black exchanges the e4 pawn. The question is about the move 13 f4, giving Black a choice: whether to take the pawn 13 ... exf3 14 gxf3 Bxc3 15 Bxc3 Re8 16 Rae1 Nh5 17 Qg2 Qh4 with a very sharp and difficult to evaluate situation, or to take up a defensive position by 13 ... Re8 14 g4 Kh8 15 g5 Ng8 16 Qg4 Nf8 17 f5 Qd7.

13 ... Bxc3 14 Bxc3 Re8 15 f3

A consistent continuation of the plan, thought out on the 10th move. Now 15 f4 would oblige Black to play 15 ... exf3, but he should not be afraid of this. On 16 gxf3 follows 16 ... Nh5 with the threat ... Nf4 and ... Qg5+. White's e3 pawn is very weak. Therefore he needs to take on f3 with the queen, but then 16 ... Qe7 17 Rfe1 (17 Rae1 Qxa3) 17 ... Ne4 and Black has an indisputable advantage.

In reply to the move in the game, Black could also choose 15 ... exf3, which was the most energetic way of exploiting White's strategical mistake on the 13th move.

15 ... Nf8? 16 Rf2?""",
    "CI-16": """It was still not too late to choose the other plan (the other objective) and leave the e4 pawn in peace. By playing 16 f4, and if 16 ... Qd7, then 17 f5, White could count on an initiative.

16 ... Qd7 17 Raf1?

Once again consistent, but not taking sufficient account of the opponent's counter-play. The objective which White pursues is unattainable and his plan does not prove to be concrete. More hopes were promised by the self-same move 17 f4 Qf5 18 h3 h5 19 Kh2 h4 20 Rg1 with a subsequent opening of the g-file.

17 ... exf3

At last! Not possible now is 18 gxf3 Ng6, and if 19 Qd3, then 19 ... Qe6 winning the e3 pawn.

18 Rxf3 Re6

Black's concrete intention is triumphant. The e4 point is in his hands, the e3 pawn is weak and subject to attack on the e-file. All Black's pieces take part in the attack, whereas the enemy bishop and knight are inactive.

19 Qd3 Rae8 20 Nb1 Ng6 21 Be1?

A tactical oversight, which, just like other such mistakes, is a consequence of a strategically difficult position. However, White cannot save the game. After 21 Bd2 Ne4, unsatisfactory are both 22 Rxf7 Qxf7 23 Rxf7 Kxf7 and 22 Nc3 dxc4 23 bxc4 Nxd2 24 Qxd2 Ne5 winning two pawns.""",
    "CI-17": """21 ... dxc4 22 Qxc4

If 22 bxc4 Ne5 and White loses the exchange. It is possible he overlooked this fact when making his previous move.

22 ... Rxe3 23 Rxe3 Rxe3

The last period of the struggle is approaching - the realisation of the advantage which has been achieved. Black has an extra pawn and a strong position - this will be quite sufficient to quickly conclude the game.

24 Bf2 Nd5! 25 Nd2

Or 25 Bxe3 Nxe3 26 Qd3 Nxf1 27 Kxf1 Nf4 28 Qe4 Ne6 winning a second pawn.

25 ... Ngf4 26 h3 Rc3 27 Qa4 Ne2+ 28 Kh2 Rxh3+ 0:1

After 29 gxh3 Ndf4 White gets mated.

This game, like the two previous ones, is a good example of the triumph of concrete ideas over an unrealistic appraisal of a position.""",
}


def parse_chinese_sections():
    text = SOURCE_MD.read_text(encoding="utf-8")
    parts = re.split(r"^## (CI-\d+)\s*$", text, flags=re.MULTILINE)
    sections = {}
    for i in range(1, len(parts), 2):
        sections[parts[i]] = parts[i + 1].strip()
    return sections


def rich_text(text, style, chinese=False):
    escaped = escape(text)
    escaped = re.sub(r"`([^`]+)`", r"\1", escaped)
    escaped = re.sub(r"^### (.+)$", r'<font name="DengBold" size="11">\1</font>', escaped, flags=re.MULTILINE)
    escaped = re.sub(
        r"^译注：(.*)$",
        r'<font name="DengBold" color="#28756B">译注：</font><font color="#5B6770">\1</font>',
        escaped,
        flags=re.MULTILINE,
    )
    escaped = escaped.replace("  \n", "<br/>")
    escaped = escaped.replace("\n\n", "<br/><br/>").replace("\n", "<br/>")
    return Paragraph(escaped, style)


def labelled(label, text, style, chinese=False):
    return Paragraph(
        f'<font name="DengBold" color="#28756B">{label}</font><br/>' +
        rich_text(text, style, chinese).text,
        style,
    )


def bilingual_table(labels, chinese_sections):
    data = [[Paragraph("经校正的英文 OCR", table_head), Paragraph("中文译文", table_head)]]
    for label in labels:
        data.append([
            labelled(label, ENGLISH[label], eng_style),
            labelled(label, chinese_sections[label], zh_style, True),
        ])
    table = LongTable(
        data,
        colWidths=[86 * mm, 98 * mm],
        repeatRows=1,
        hAlign="CENTER",
        splitByRow=1,
        splitInRow=1,
    )
    commands = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("BOX", (0, 0), (-1, -1), 0.7, MID),
        ("INNERGRID", (0, 0), (-1, -1), 0.35, MID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 1), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
    ]
    for idx in range(1, len(data)):
        commands.append(("BACKGROUND", (0, idx), (-1, idx), colors.white if idx % 2 else PALE))
    table.setStyle(TableStyle(commands))
    return table


def header_footer(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setStrokeColor(MID)
        canvas.setLineWidth(0.5)
        canvas.line(18 * mm, A4[1] - 14 * mm, A4[0] - 18 * mm, A4[1] - 14 * mm)
        canvas.setFillColor(MUTED)
        canvas.setFont("Deng", 8)
        canvas.drawString(18 * mm, A4[1] - 11 * mm, "《国际象棋中局计划》｜计划 - 具体构想｜校对稿")
    canvas.setFillColor(MUTED)
    canvas.setFont("Deng", 8)
    canvas.drawCentredString(A4[0] / 2, 10 * mm, str(doc.page))
    canvas.restoreState()


def scaled_image(path, max_width, max_height):
    from PIL import Image as PILImage

    with PILImage.open(path) as image:
        width, height = image.size
    scale = min(max_width / width, max_height / height)
    return Image(str(path), width=width * scale, height=height * scale)


chinese_sections = parse_chinese_sections()
missing = sorted(set(ENGLISH) ^ set(chinese_sections))
if missing:
    raise ValueError(f"Section mismatch: {missing}")

doc = SimpleDocTemplate(
    str(OUTPUT),
    pagesize=A4,
    rightMargin=13 * mm,
    leftMargin=13 * mm,
    topMargin=20 * mm,
    bottomMargin=17 * mm,
    title="Chess Middlegame Planning - Concrete Ideas - Chinese Proof",
    author="OCR and Chinese translation proof",
    subject="Corrected English OCR and Chinese translation for proofreading",
)

story = [
    Spacer(1, 27 * mm),
    Paragraph("《国际象棋中局计划》", cover_title),
    Paragraph("计划 - 一般原则 - 具体构想", cover_title),
    Spacer(1, 4 * mm),
    Paragraph("英文 OCR 校正稿 + 中文翻译校对稿", cover_subtitle),
    Spacer(1, 14 * mm),
]
cover_info = [
    [Paragraph("文档性质", label_style), Paragraph("初译校对稿，非最终出版版本", info_style)],
    [Paragraph("内容范围", label_style), Paragraph("原书印刷页 9 至第 17 页右栏；止于 3: Dynamics 之前", info_style)],
    [Paragraph("棋谱规范", label_style), Paragraph("中文译文统一采用现代 SAN：O-O、1-0、0-1，并规范回合号与黑方省略号", info_style)],
    [Paragraph("术语延续", label_style), Paragraph("development of pieces 译为“出子”；realisation of the advantage 译为“兑现优势”；concrete idea 暂译“具体构想”", info_style)],
    [Paragraph("版本日期", label_style), Paragraph("2026-09-23", info_style)],
]
info_table = Table(cover_info, colWidths=[30 * mm, 125 * mm], hAlign="CENTER")
info_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), PALE_BLUE),
    ("BOX", (0, 0), (-1, -1), 0.7, MID),
    ("INNERGRID", (0, 0), (-1, -1), 0.35, MID),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 9),
    ("RIGHTPADDING", (0, 0), (-1, -1), 9),
    ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
]))
story.append(info_table)
story.append(Spacer(1, 10 * mm))
story.append(Paragraph("建议重点核对：“具体构想”的标题译法；三盘例局中对计划、目标和构想的区分；棋手姓名译法；以及所有实战与分析变例的棋谱。", section_note))
story.append(PageBreak())

story.append(Paragraph("2 具体构想（Concrete Ideas）", section_title))
story.append(Paragraph("一般论述", section_note))
story.append(bilingual_table(["CI-1", "CI-2", "CI-3"], chinese_sections))

story.append(CondPageBreak(38 * mm))
story.append(Spacer(1, 7 * mm))
story.append(Paragraph("例局一：克拉曼 - 斯梅斯洛夫", section_title))
story.append(bilingual_table(["CI-4", "CI-5", "CI-6"], chinese_sections))

story.append(CondPageBreak(38 * mm))
story.append(Spacer(1, 7 * mm))
story.append(Paragraph("例局二：尤多维奇 - 克拉曼", section_title))
story.append(bilingual_table(["CI-7", "CI-8", "CI-9", "CI-10"], chinese_sections))

story.append(CondPageBreak(38 * mm))
story.append(Spacer(1, 7 * mm))
story.append(Paragraph("例局三：邦达列夫斯基 - 鲍特维尼克", section_title))
story.append(bilingual_table(["CI-11", "CI-12", "CI-13", "CI-14", "CI-15", "CI-16", "CI-17"], chinese_sections))
story.append(PageBreak())

story.append(Paragraph("附录：原扫描页", section_title))
story.append(Paragraph("以下图像保留原书棋盘图、版面和旧式记谱，用于核对 OCR、棋谱与译文。", section_note))
story.append(PageBreak())
for page in range(11, 20):
    printed = page - 2
    story.append(Paragraph(f"原书印刷页 {printed}", scan_caption))
    story.append(scaled_image(WORK / f"source-{page:03d}.png", 170 * mm, 238 * mm))
    if page != 19:
        story.append(PageBreak())

doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(OUTPUT)
