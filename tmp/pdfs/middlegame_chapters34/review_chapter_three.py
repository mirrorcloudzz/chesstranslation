"""Source-page review of Chapter Three; preserves legacy proofreading IDs."""
import json
import re
from pathlib import Path

ROOT = Path(str(Path(__file__).resolve().parents[3]))
TRANS = ROOT / 'translations' / 'chess_middlegame_planning'
TMP = Path(__file__).parent

# Each combined range restores a sentence/paragraph split by the first OCR pass.
MERGES = {14: 15, 19: 20, 21: 23, 47: 48, 59: 60, 65: 66,
          70: 75, 86: 87, 92: 93, 96: 97, 100: 101, 109: 111,
          114: 115, 118: 119, 133: 134, 137: 138, 139: 140,
          147: 148, 149: 150, 178: 179}

ZH = {
1: 'a线上的战斗',
2: '我们选取双方均已短易位时围绕a线展开的计划性行棋作为基本主题。这类a线行动具有鲜明特点，值得单独研究。',
3: '双方均在王翼易位时，a线行动具有哪些特点？首先，a线与王翼相距甚远，所以主要战事暂时不会直接影响易位后的王城。更重要的是，掌握a线主动权的一方必须在该线及其附近集中大量兵力，尤其是双车。这意味着重要棋子会被调离王翼，从而可能促使对手转而进攻王翼。因此，必须以稳固兵链和少量轻子妥善守护王翼。\n\n译注：从残局的观点来看，由于a线距离王城非常远，而轻子对于通路兵，尤其是边线通路兵的防守能力较弱，如果在此处的战斗发生大量重子兑换，后翼一旦出现通路兵将是决定性的。在围绕a线斗争的过程中执行兑换或者兵的突破时，必须时刻考虑到这一点。',
4: '打开a线的基本方法，是以a兵交换对方的b兵。如果b兵仍在初始格，这种交换便难以实现。因此，打开a线之前，往往要先诱使对方的b兵冲起一格或两格。不言而喻，打开a线并随后沿线侵入的计划必须经过周密考虑：既要结合局面的具体条件，也要权衡对手能否有利地阻止开线，或在王翼发动有效反击。',
5: '规划a线行动时，当然必须确保开线后能够以双车占据该线。这意味着适当的子力重组必须在a线打开之前便已完成。',
6: '早在十九世纪末的伦敦国际象棋大会附属赛（1898年）中，马尔科对穆勒一局的收尾，便出色展示了沿a线侵入的技术。',
7: '白方已经为打开并占据a线做好准备。',
8: '此时立即在b6吃兵也不坏。白方若走33. axb6 axb6 34. Qa1! Rxa4 35. Rxa4，便可掌握a线；结合b6兵和e6兵的弱点，这最终应当为白方带来胜利。不过，黑方以35... Rd7回应后仍可顽强防守。',
9: '马尔科选择了最佳下法：',
10: '**33. Qa1!**\n\n这时才真正威胁axb6。为了不丢兵，黑方被迫将a8车移开，随后白方便能在保留全部重子的情况下占据a线。实战接着走：\n\n**33... Rab8 34. axb6 axb6 35. Ra7+ Kh8 36. Rc7 Ra8 37. Raa7 Rxa7 38. Qxa7**',
11: '白方在第七横线叠起重子，胜负很快便见分晓。',
13: '在这个例子中，王翼局面很平稳。封闭的兵链使白王免受任何威胁，白方便能把全部子力调往a线。',
14: '在拉斯克对肖瓦尔特一局（纽伦堡，1896年）中，整体形势则大不相同。黑方通过...a5-a4xb3的冲兵路线成功打开并占据a线，随后以重子侵入第一、第二横线。拉斯克则力求利用肖瓦尔特为整套行动耗费的时间，对黑王制造反击威胁。黑王仍在h8，由h7-g6-f5兵链和e6马掩护。白方走完第60步后，这盘战略上颇有意思的对局形成了图示局面，其优劣并不容易判断。',
16: '白王头顶乌云密布，但白方也有自己的机会。位置极佳的d5马转到f6后，便能为后打开h1-a8斜线。白后沿这条斜线侵入b7或c6，就能对黑王制造直接威胁。',
17: '接下来，局势的发展既尖锐又有趣：',
19: '威胁...Qf1。然而，黑方没有预见到对手危险的反击。他本可通过61... Rg1+ 62. Bxg1 Qxg1+ 63. Kh3 Nxf4+ 64. Qxf4 Qh1+ 65. Kg3 Qg1+ 66. Kh3 Qh1+等后续手段求和，但也仅此而已（67. Qh2 Qf1+）。当然，对61... Rg1+，白方也可走62. Kh2；不过，62... Rf1 63. Rd2 Qe1会形成复杂局面，黑方看来能够守住。实战中，胜负却立即揭晓：\n\n**62. Qb7 Ng7 63. Qf7 1-0**',
21: '黑方能否用更强的走法替代60... Rb1？60... Qc1可以争取胜机。若61. Nf6，则61... Qc2，白方只有把马退回d5，因为62. Bg1会遭到62... Qg2+。黑方接下来的计划是走62... Qe2兑后；若63. Qxe2，就把车撤回b2，再把王调到f7，马调到a5，以吃掉b3兵。在卡帕布兰卡的对局中，我们还可以找到几个富有启发性的a线作战范例。',
24: '在对特雷巴尔的一局中（卡尔斯巴德，1929年），执白的卡帕布兰卡经过长时间围攻，封闭了中心和王翼，成功打开a线，并以重子沿线侵入。',
25: '白方轻而易举地控制着a线。他的七个兵组成强大的黑格兵链，把黑方牢牢封锁住，迫使黑方只能等待。唯一的问题在于：白车侵入a7已不可阻止，但白方能否利用这一点取得成果？',
26: '实战接着走：',
28: '40... Qa8 41. Qb2也无济于事。',
30: '白方已经侵入，并将重子以理想的次序配置在a线上，后居于双车之后。然而，下一步该怎么办？接下来的运王表明，卡帕布兰卡尚未形成明确的行动计划。',
32: '王在h4的位置不佳；白马一旦离开f3，黑方便可能获得在g5弃子的战术机会。',
34: '现在，一切都清楚了。黑方的b7兵是弱兵，白马正准备转往a5。',
36: '白方的侵入范围扩展到了第七横线。',
38: '从这段收尾可以看出，a7车为轻子提供了防守上的支持。这便引出一个问题：如果棋盘上只有重子，白方还能利用自己在a线上的巨大空间优势吗？恐怕不能，因为他将没有合适的棋子去攻击b7兵。',
39: '1927年卡帕布兰卡对阿廖欣世界冠军赛第25局的收尾，可以很好地回答这个问题。',
41: '这是被迫的，否则白方会主动在a6交换，再沿b线侵入。',
43: '乍看之下，似乎反而是黑方会占据a线，但这只是表象。',
45: '阿廖欣预见到接下来的局势发展，强制交换双方最后的轻子，以便随后更容易地防守b7兵。',
47: '若29... Rcc8，白方以30. Rxa8 Rxa8 31. Qb6即可得兵。\n\n**30. b6 Rd7 31. Ra7 Kh7 32. Rca1 f5 33. Qc2 Re7 34. g3 Rce8**',
49: '黑方暂时无法在e线上制造威胁，但白方也无法进一步增加对b7兵的压力。',
51: '阿廖欣认为，白方应立即走26. Ra1，而不是26. b5，以避免兑象。这样，白方利用后翼优势的机会会更多；不过，保留双方的象也会增加黑方的防守资源。况且局面比较开放，黑方还可以在中心和王翼组织反击。',
52: '当一方沿a线展开行动，而对手以王翼的主动行动相抗衡时，斗争就会变得更加尖锐激烈。有时，a线行动会发展为真正的反击；只要同时做好对己方王的防守，就可能取得决定性成果，尤其是在对手过分专注于王翼进攻的时候。',
53: '下面继续看实战例局。',
54: '伯德开局',
55: '白方：P. 叶夫季费耶夫',
56: '黑方：D. 达努舍夫斯基',
57: '（圣彼得堡，1909年）',
59: '在这个开局中，白方的计划是牢牢控制e5格，从而在王翼取得主导地位，再让b2象、后及王翼车协调配合，对黑王发动直接进攻。王翼车的调动路线是短易位后经f1-f3转到g3或h3。从对抗这一计划的角度看，黑方的开局下法即使谈不上软弱，也至少缺乏针对性。黑方较好的选择之一是把象出到g7，因此第3步值得考虑3... g6，而不是3... Nf6。同样，黑方也不必急于出后翼马，以免白象上b5形成牵制；或者先走...a6，防止这种牵制。\n\n**6. Be2**',
61: '毫无疑问，6. Bb5更符合白方的计划；随后以象换马，可以进一步巩固对中心e5格的控制。这再次说明，开局与中局的计划必须相互衔接。',
63: '这次跃马至少为时过早。无论现在还是下一步，白方都应优先考虑d3，因为在e5交换只会正中黑方下怀。',
65: '双方都没有按计划行棋，而是在各走各的零散招法。白方应先走10. d3，而不是10. Qg3，以便用e4应对10... d4。黑方本来也可以利用有利条件，以...d4在中心发动进攻。他可能担心11. Bf3，但下面的变化说明，这种顾虑完全没有必要：11... Nd5 12. e4 Nxe5 13. fxe5 Nb4 14. Na3 a6，黑方有明确的后翼冲兵计划；或者12. Nxc6 Bxc6 13. exd4（13. e4? Bh4 14. Qg4? f5 15. exf5 exf5 16. Bxd5+ Qxd5!，黑方取得决定性优势）13... Bh4 14. Qh3 Bf6，黑方明显占优并掌握主动。实战中，黑方选择把马从f6调到d6、把象调到f6，这也不坏，但只解决了一个局部问题。\n\n**11. Qh3 Bf6 12. d3 Nd6 13. Nd2**',
67: '这步棋自然，甚至也是必要的，但从具体局面出发，白方应稍缓一步。对黑方下一步的分析将表明，此时先走g4，剥夺黑马利用f5格的可能，会非常有用。',
69: '与第21步一样，这是黑方本局最严重的局面错误之一。不可否认，黑方的行棋确有一定计划：他准备在后翼大举冲兵，围绕a线展开行动。然而，他对白方王翼进攻可能性的估计过于肤浅。这步棋主动消除了中心兵之间的紧张，使白方能够放手在王翼行动。这个错误本应带来致命后果。',
70: '其实，黑方有一个值得研究的选择：13... Bxe5。白方必须仔细考虑，究竟用什么吃回这只象。例如，14. Bxe5 Nxe5 15. fxe5 Nf5之后，16. g4可用16... Qh4应对；对白方的16. Bg4，16... Nh6也足够好。由于黑方有17... Bc8或17... Qe7，白方弃半子的效果值得怀疑。14. fxe5 Nf5这一变化也有类似情况，只是由于白方还保留着b2象，弃半子能够带来更多机会。不过，15. Rxf5 exf5 16. Qxf5 Bc8 17. Qh5 Ne7之后，黑方的局面仍相当稳固。',
76: '实战没有出现上述变化，黑方的局面开始恶化。',
78: '黑方的局面原本已经较差，这一步又让对手能够切断黑方全部子力与王翼的联系，进而对王发动难以抵挡的进攻。15... Be7更好。',
80: '这只象即将侵入第三横线，可惜它在这里的威风只能是昙花一现。',
82: '黑象无法在e3站稳脚跟。例如19... Nb5 20. Ng1，白方又能用后攻击这只象。',
84: '黑方开始实施后翼进攻计划。如果立即走20... a5，白方可以21. a4回应；现在黑方准备按...a5-a4xb3的路线冲兵。不过，白方的进攻本应更快奏效。',
86: '白方一味追求Ng6之类漂亮的临时威胁，对局面作出了错误判断。仅凭一只棋子进攻，无法突破黑方在王翼的兵防线。白方所选的计划不切实际，构想也不够具体。他应走21. g4；若21... Nf7，则22. Qg3。此后可能出现22... h6 23. h4 a5 24. Rf2 a4 25. Rg1 axb3 26. axb3 Ra2 27. g5! hxg5 28. hxg5 Rxc2 29. Rh2 fxg5 30. Qh3 Nh6 31. Rxg5，白方制造出多种威胁。\n\n**21... Be8**',
88: '只要黑方不接受弃子，Ng6就没有实际威胁，因此黑方本可直接走21... a5，节省时间。有时，棋手选择某步棋的原因可以从其风格中找到。达努舍夫斯基是一位极其谨慎的棋手，即使并无迫切需要，也从不错过加固防线的机会。',
90: '现在，就连达努舍夫斯基也不再理会白方的进攻了。白方的计划犹如沙上建塔，根本没有坚实基础。',
92: '白方仍寄希望于24... axb3 25. axb3 Ra2 26. Ng6 Rf7? 27. Rxh7，或者26... Bxg6 27. fxg6 h6 28. Qe6+ Kh8 29. b4!。然而，黑方接下来的应手连这点希望也打破了；此后，白方聚集在王翼的子力将完全无所作为。',
94: '叶夫季费耶夫认清进攻计划已经失败，开始全线撤退，急忙把子力从王翼调回。与此同时，黑方夺得主动，沿a线侵入白方阵地。',
96: '27. Ng6 Bxg6 28. fxg6 h6 29. Bg4 Qe7也不能给白方带来任何好处。\n\n**27... Qa7 28. Rf3 Bf7 29. Rf1 Ra8 30. Nf3**',
98: '白方的棋子竟又回到了十步前开始进攻时的位置！他虽然避免了子力损失，却在局面上蒙受了严重损失。黑方已经打开并占据a线，车侵入a2，接下来威胁...c4，并将侵入范围扩展到第二横线。',
100: '这种兑现优势的方法有条不紊，却稍嫌缓慢。更有力的是31... c4 32. bxc4 bxc4 33. Rb1 Qc3 34. Ne1 cxd3；或者33. g4 Rb8 34. Ra1 Rbb2。\n\n**32. g4**',
102: '白方终于投入进攻，但已经晚了11步，条件也比第21步时差得多。不过，这是他最后、也是唯一的自救机会。正所谓亡羊补牢，犹未为晚。',
104: '这是一幅生动而富有启发性的重子侵入图景！',
106: '白方打算用Bh5使局面变得尖锐。',
108: '这种令人惋惜的错误，往往是斗争过于紧张所致。如果走36. Bh5，黑方仍会遇到一些麻烦。',
109: '例如36... Bxb3 37. Qg4，白方威胁Rg1，能够获得攻势。不过，只要黑方简单地走36... c4 37. Bxf7 Nxf7 38. bxc4 bxc4 39. dxc4 Qe3，就能吃掉e4兵并获胜，因此36. Bh5这一尝试最终也不能成功。\n\n**36... Bxb3!**',
112: '白方漏算了这步应手。若37. cxb3，则37... Rxe2，威胁一步杀。',
114: '准备以38. Qg4应对37... Bxc2。\n\n**37... Nxe4!**',
116: '漂亮而决定性的一击，威胁...Nf2+。',
118: '白方还可以走38. Qf3，但38... Bd5! 39. dxe4 Qxf3+ 40. Bxf3 Bc6之后，尽管白方多一子，却仍无力抵挡黑方后翼兵群的汹涌攻势。例如41. Rg2 c4 42. Kg1 b4 43. Kf1 b3 44. cxb3 Rxg2 45. Bxg2 c3等。\n\n**38... Bxc2 39. Nxc2 Rxc2 40. Rxc2 Qxc2 41. Qxc2 Rxc2**',
120: '进入残局后，黑方三个相连的通路兵使白方毫无希望。白方只是惯性地又抵抗了几步。',
122: '这盘极其复杂而有趣的对局中，有一点值得注意。黑方最严重、原本可能导致输棋的错误是13... d4，但后来恰恰是这个d4兵，成为黑方后翼冲兵得以成功的基石！可见，随着棋盘上形势的变化，一步坏棋的作用也可能转向相反的一面。这正是国际象棋内在辩证性的一种体现。',
123: '再看一盘棋。它或许是a线作战最精彩的范例，也鲜明展示了让对手重子沿a线侵入会带来怎样危险的后果。',
124: '英格兰开局',
125: '白方：M. 尤多维奇',
126: '黑方：V. 阿拉托尔采夫',
127: '（第14届苏联锦标赛半决赛，1944年）',
129: '严格说来，双方此时都还没有真正经过深思熟虑的计划。他们谨慎调动子力，试图把棋子和兵的作用集中到中心格附近，行棋仍以概括性的考虑为依据。',
131: '白方专注于调动子力，却没有注意到自己可能丢兵。',
133: '黑方可以这样得兵：11... Bxf3 12. Bxf3（若想保住这兵，就必须走12. gxf3，但12... exd4 13. exd4 Nh5之后，黑方获得的优势比一兵更有价值）12... exd4 13. exd4 Rxe1+ 14. Qxe1 Nxd4 15. Bxb7 Nc2 16. Qd1 Nxa1 17. Bxa8 Nxb3。不过，18. Nd5! Nxd5 19. Bxd5 Nc5 20. Bd4之后，这点收获很难转化为胜势。黑方可能不愿满足于和棋，因而主动放弃这一变化，转而设法使d3成为潜在弱格，并限制b2象的活动。这还不算完整的计划，但已经是在为计划作准备。\n\n**12. Nh2 Bxe2 13. Qxe2 d5!**',
135: '白方的后翼象现在受到严重限制；黑方则在中心e4建立起坚强的兵据点，子力配置明显更好，并威胁通过...Nb4-d3把马安置到弱格上。不过，斗争的焦点仍应在中心。',
136: 'd5格才是双方必须紧盯的要点。d5兵支撑着e4兵；黑方若能先移开c6马，再走...c6，就能大大巩固中心兵群。巩固中心并侵入d3，是黑方计划第一阶段的内容。由此也就明确了白方眼前的任务：阻止对手的这一意图。白方可以14. Ng4加强对d5的控制。',
137: '由于...dxc4会违背黑方的整体计划，黑方只好走14... Nxg4。此时，白方至少有Qxg4、hxg4和cxd5三种后续手段，都能引出复杂变化，迫使对手解决一系列新的问题。例如15. Qxg4 Ne7 16. cxd5 f5 17. Qe2 Nxd5 18. Qc4 c6 19. Rac1等。',
139: '即使走14. a3，阻断黑马前往d3的路线，也比实战下法好。可能的后续手段是14... Na5 15. Qc2 dxc4 16. bxc4 Nxc4 17. Nxe4 Nxb2 18. Nxf6+ Qxf6 19. Qxb2 Qb6 20. Qc3。\n\n**14. Rad1**',
141: '这步棋没有计划，既不追求明确目标，也没有具体构想指导。更令人不满的是，它未能阻止黑马侵入d3弱格。',
142: '那么，白方为什么走这一步呢？看来，他只是想把车从无所作为的角落a1格，调到位置无疑更好的中央d1格。',
143: '在某些局面中，尤其是开局阶段，根据一般性考虑这样行棋完全合理。不过，即使在纯粹的局面性斗争中，通常也有足够的具体内容，可以据此计算变化、确定任务并付诸实施。眼前这盘棋正是如此。',
145: '白方局面已明显较差，更严重的是，黑马深入其子力配置的腹地，使他几乎无计可施。因此，勇敢的选择应是弃半子：18. Rxd3 exd3 19. Qd1。这样可以拔掉这根刺，争取顽强抵抗的机会。实战中，白方却宁愿继续困守苦境。',
147: '黑方打算换掉唯一能把马赶出d3的棋子，从而确保这匹马成为铁马。不过，20... b6或20... Qa5仍然更好。\n\n**21. Qc2?**',
149: '这步棋实在不能不打问号。白方再次无视对手的意图，毫无计划地行棋。应走21. Na4，威胁Nb2。若21... Ba3，则22. Nc5! Nxc5 23. dxc5 Bxc5 24. cxd5 cxd5 25. Kh1，白方制造出Qb2的危险威胁。若黑方以21... b6回应21. Na4，白方仍可22. Nb2，换掉侵入的黑马。这也解释了为什么黑方应在第20步就走...b6，不给白方Nc5的机会。\n\n**21... Bxc3**',
151: '这次交换之后，白方的局面已很难挽救。',
153: '打开c线只对黑方有利，因为黑方可以轻易用双车占据这条线。',
155: '固定住b3兵。这对实施a线进攻计划十分重要。',
157: '黑方开始实施计划的第二阶段：打开a线。白方无法阻止，唯一的抵抗机会是在王翼组织进攻。走g4等手段为此提供了一点可能，但显然还远远不够。',
160: '果然如此，白方开始尝试最后的机会。',
162: '黑方将在后翼积极行动，同时在王翼采取必要的预防措施。由于白方的威胁很有限，这并不困难。现在，黑方自己反而威胁吃掉g4兵。',
164: '黑方还有一个优势值得注意：第七、第八横线为双车在棋盘两翼之间调动提供了绝佳通道，使黑方能够充分发挥车强大的机动性。利用己方后方畅通的横线自由而迅速地调车，有时可以成为决定性因素。白方在这方面的处境差得多：第一横线上子力拥挤，第二横线也交通不畅，因为占据d3的黑马在这两条横线上各控制着两个格。接下来可以看到，黑方如何充分利用对方后方受制的弱点。',
166: '必须阻止白车侵入g5。',
168: '当然不能31. Rxg6，因为黑方有31... Nxe1，或31... Qxg6 32. Rxg6 Nxe1!。',
170: '典型的侵入过程开始了，随后便要把侵入转化为具体成果：从侧面进攻白王的位置。',
172: '白方似乎终于制造了一个实实在在的威胁：Rxg6。',
174: '这步棋有什么用呢？34. Qg4之后尚可继续斗争，实战却迅速走向终局。最后，白方全军被牢牢困住，景象鲜明而生动，充分体现了从侧面进攻的特点。',
176: '现在开始兑现优势！黑方双车协调配合，作战方向由a线转向第一横线。（见下图）',
178: '若42. Rh2，则42... Rf3+ 43. Kg2 Rb1，黑方得后。不过，此时黑方已经不止一种获胜方法。',
180: '本章着重讨论重子沿a线突破，但显然，这种突破在计划、实施方法和结果上，与沿其他线侵入敌方阵地并无太大差别。当然，沿边线突破与沿中央的e线或d线突破，仍存在一些区别，尤其是在将侵入转化为成果的过程中。沿中央线突破时，侵入的车需要兼顾两翼，有时反而会分散突破的力量。',
181: '沿边线侵入时，车的进攻则集中朝向一翼，因此目标更明确，力量也更集中。',
}

# OCR repairs verified against all twelve source scans (printed pp. 87–98).
EN_REPLACE = {
    'do ) not affecthe': 'do not affect the', 'thathe': 'that the',
    'could 1 prompthe': 'could prompt the', 'covering C detachment': 'covering detachment',
    'largescale': 'large-scale', 'preventhe': 'prevent the', 'regrouping g': 'regrouping',
    'yethe': 'yet the', 'Nirnberg': 'Nürnberg', 'againsthe': 'against the',
    'arrived athe': 'arrived at the', 'penetratin on': 'penetrating on',
    'buthen': 'but then', 'invadin on': 'invading on', 'exploithe': 'exploit the',
    'sevenpawn': 'seven-pawn', 'Capablanca- Alekhine': 'Capablanca-Alekhine',
    'development t': 'development', '3 3...': '3...', 'considering g': 'considering',
    'buthe': 'but the', 'there were no grounds at all for “"fright"': 'there were no grounds at all for "fright"',
    'thathere': 'that there', '16... ( Qh4': '16... Qh4',
    'route-march 1...': 'route-march ...', 'chooses san': 'chooses an',
    'mighthen': 'might then', 'accepthe': 'accept the',
    'possible, without losing it was time,': 'was possible, without losing time,',
    'justhe': 'just the', 'dangerous eensuing consequence from': 'dangerous consequence ensuing from',
    'Semi-fina1': 'Semi-final', 'rea1,': 'real,', 'manoeuvre e': 'manoeuvre',
    'Rxel+': 'Rxe1+', 'Racl': 'Rac1', 'limithe': 'limit the', 'plan.l': 'plan.',
    'at least 3. continuations': 'at least 3 continuations', 'Further- more': 'Furthermore',
    'dra on': 'drag on', 'Ousting': 'ousting',
    'thereby himself the securing': 'thereby securing himself the',
    '0n 21.': 'on 21.', 'Occupy': 'occupy',
    "an attack the king's flank. A small, on though": "an attack on the king's flank. A small, though",
    'presenthemselves': 'present themselves', 'Be1ow': 'Below',
    'tothefirst': 'to the first', 'queen.1': 'queen.',
    'not very r much': 'not very much', 'Of course, army there': 'Of course, there',
    'position of the enemy on other files': 'position of the enemy army on other files',
    'However, an invasion upon along': 'However, upon an invasion along',
    'central e or d lines': 'central e or d lines',
    'onepiece': 'one-piece', '... a5 a4xb3': '...a5-a4xb3',
    'therefore was possible': 'therefore it was possible',
}

EN_BY_ID = {
21: "Could Black, instead of 60... Rb1, have played stronger? 60... Qc1 offered chances of a win. If 61. Nf6 then 61... Qc2 and there is only one more for White - the return of the knight to d5, since on 62. Bg1 follows 62... Qg2+. Black's further plan is this: to exchange queens by playing 62... Qe2, return the rook to b2 (in the event of 63. Qxe2), transfer the king to f7 and dispatch the knight to a5 to win the b3 pawn. Several instructive examples of play on the a-file can be found in the creative work of Capablanca.",
46: '28. Bxg6 Qxg6 29. Ra1 Rac8',
70: "Meanwhile, Black had at his disposal an interesting possibility - 13... Bxe5, and White has to think carefully before deciding how to recapture the bishop. If, for example, 14. Bxe5, then 14... Nxe5 15. fxe5 Nf5 and on 16. g4 follows 16... Qh4, while on 16. Bg4 good enough is 16... Nh6. The sacrifice of the exchange is doubtful in view of 17... Bc8 or 17... Qe7. The same consideration applies also to the variation 14. fxe5 Nf5, only in this situation the exchange sacrifice promises White rather more chances, since the bishop on b2 is still present, though after 15. Rxf5 exf5 16. Qxf5 Bc8 17. Qh5 Ne7 Black has quite a solid position.",
}

# Mainline strings within mixed prose segments: preserve the original bolding.
MAINLINES = {
10: ['33. Qa1!', '33... Rab8 34. axb6 axb6 35. Ra7+ Kh8 36. Rc7 Ra8 37. Raa7 Rxa7 38. Qxa7'],
19: ['62. Qb7 Ng7 63. Qf7 1-0'],
47: ['30. b6 Rd7 31. Ra7 Kh7 32. Rca1 f5 33. Qc2 Re7 34. g3 Rce8'],
59: ['6. Be2'], 65: ['11. Qh3 Bf6 12. d3 Nd6 13. Nd2'],
86: ['21... Be8'], 96: ['27... Qa7 28. Rf3 Bf7 29. Rf1 Ra8 30. Nf3'],
100: ['32. g4'], 109: ['36... Bxb3!'], 114: ['37... Nxe4!'],
118: ['38... Bxc2 39. Nxc2 Rxc2 40. Rxc2 Qxc2 41. Qxc2 Rxc2'],
133: ['12. Nh2 Bxe2 13. Qxe2 d5!'], 139: ['14. Rad1'],
147: ['21. Qc2?'], 149: ['21... Bxc3'],
}


def main():
    source = json.loads((TMP / 'translated_segments_clean.json').read_text(encoding='utf-8'))
    old = [s for s in source if 89 <= s['page'] <= 100 and s['kind'] != 'chapter']
    if len(old) != 181:
        raise ValueError('Run only against the legacy 181-section Chapter Three draft.')
    reviewed = []
    coverage = []
    n = 1
    while n <= len(old):
        if n == 158:
            assert old[n - 1]['text'] == 'Y'
            n += 1
            continue
        end = MERGES.get(n, n)
        group = old[n - 1:end]
        item = dict(group[0])
        en = ' '.join(s['text'] for s in group)
        for before, after in EN_REPLACE.items():
            en = en.replace(before, after)
        en = EN_BY_ID.get(n, en)
        if n == 14:
            en = en.replace('march-route a5-a4xb3', 'march-route ...a5-a4xb3')
        if n == 19:
            en = en.replace('threat Qf1', 'threat ...Qf1')
        if n == 65:
            en = en.replace('11. Nd5', '11... Nd5')
        if n == 86:
            en = en.replace('21. Nf7', '21... Nf7')
        if n == 133:
            en = en.replace('11 . Bxf3', '11... Bxf3')
        if n == 149:
            en = en.replace('21. Ba3', '21... Ba3')
        if n == 180:
            en = en.replace('central e or d lines', 'central e or d lines')
        # Repair a move number stranded at an OCR segment boundary.
        en = re.sub(r'(?<![A-Za-z0-9.])(\d+) (?=(?:[KQRBN][a-h]|[a-h](?:x[a-h])?[1-8]))', r'\1. ', en)
        if n in ZH:
            zh = ZH[n]
        else:
            # Every unrewritten section must consist solely of checked moves.
            residue = re.sub(r'\d+\.{1,3}|[KQRBN]?[a-h]?[1-8]?x?[a-h][1-8][+#!?]*|O-O(?:-O)?|1/2-1/2|[01]-[01]|[\s.]', '', en)
            if residue:
                raise ValueError(f'Unreviewed prose CH3-{n}: {residue}')
            zh = en
            item['kind'] = 'moves'
        if n in MAINLINES:
            for moves in MAINLINES[n]:
                assert moves in en, (n, moves, en)
                en = en.replace(moves, '\n\n**' + moves + '**\n\n', 1)
            item['kind'] = 'body'
        if n in ZH and n not in {1, 54, 55, 56, 57, 124, 125, 126, 127}:
            item['kind'] = 'body'
        item['text'] = re.sub(r' *\n *', '\n', en).strip()
        item['zh'] = zh.strip()
        item['segment_id'] = f'CH3-{n}' if n == end else f'CH3-{n}–{end}'
        item['legacy_ids'] = [f'CH3-{i}' for i in range(n, end + 1)]
        item['page_end'] = max(s.get('page_end', s['page']) for s in group)
        item['review_status'] = 'source_scan_reviewed'
        reviewed.append(item)
        coverage.extend(range(n, end + 1))
        n = end + 1
    assert set(coverage) | {158} == set(range(1, 182))
    target = TRANS / '13_chapter_three_reviewed.json'
    target.write_text(json.dumps(reviewed, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Reviewed {len(reviewed)} sections; all 181 legacy IDs accounted for, including deleted OCR noise CH3-158.')


if __name__ == '__main__':
    main()
