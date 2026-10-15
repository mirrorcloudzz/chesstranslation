import json,re,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; TMP=Path(__file__).parent
TRANS=ROOT/'translations/chess_middlegame_planning'
name='16_chapter_six_heavy_pieces'
archive=TRANS/'archive/20260928_before_ch6_illustrated';archive.mkdir(parents=True,exist_ok=True)
src=TRANS/(name+'_reviewed.json')
if not (archive/src.name).exists():
    for f in [src,TRANS/(name+'_zh.md'),TRANS/(name+'_en_ocr.md'),TMP/'reviewed_segments.json']:
        shutil.copy2(f,archive/f.name)
rows=json.loads((archive/src.name).read_text(encoding='utf-8'))
edits={}
def group(a,b,*parts): edits[a]=(b,list(parts))
group(20,21,'**25... Rd7 26. Qd1 Qe5 27. Qg4 Ke8**')
group(23,24,'王在g8或f8当然比在c7更安全，不过即使在c7，对手也很难接近它：棋盘上子力不多，而黑方后翼兵链相当稳固。')
group(30,32,'施莱希特显然想向这位强劲的对手证明，眼下仍是中局。但白方自己也须谨慎：a3兵薄弱，加上黑方可能以... c5冲兵突破，车残局对白方完全不能接受。此前走h3而非g3的弊端也开始显现。正因如此，看起来自然且最好的后续手段32. Qd3不能成立，因为32... Qa1+ 33. Kh2 Qa2! 34. c5 dxc5 35. bxc5 Rd7 36. Qc3 Qd2! 37. Qe5+ Kb7，黑方凭借后翼多兵和对d线的控制，获得切实的胜机。〔校勘注：原书写作“白方”，与所列变化及上下文矛盾；此处按“黑方”理解。〕')
group(40,42,'这是应对白方威胁的好办法。若36. a4，则可能出现36... bxa4 37. Qxa4 Kb7 38. Ra3 Qxe4+ 39. Kh2 Qd4! 40. Qa6+ Kc7 41. Qa7+ Qxa7 42. Rxa7+ Kb6。现在拉斯克这步的用意便清楚了：让f兵避开攻击。43. Rxg7 Re4之后，黑方应能赢下残局。')
group(50,50,'后深入得过于冒进。黑方无疑应走38... Ra8，彻底消除白方冲起a兵这一主要、甚至可能是唯一的机会。也许拉斯克看不出继续加强局面的明确办法，便反过来引诱施莱希特发动接下来的兵的攻击，指望白方为此弃掉子力。')
group(54,56,'39... Ra8也不差：40. axb5 Qxb5 41. Qb3 Ra1! 42. Rd3 Kb6，若43. Rxd6，则43... Qf1+ 44. Kg3 Qg1+，黑方胜。不过，拉斯克急于取得子力优势，尤其是因为当时看不出王会立即遭遇危险。')
group(68,69,'黑方主动进一步暴露自己的王，显然相信防守可靠，并希望尽快兑现子力优势。若46... Rb5，白方可用47. Ra4反击；若47... Rb1，则48. Qa5+ Kd7 49. Qf5+。')
group(70,72,'评注这盘复杂对局的棋手认为，最好的防守是46... Ra5，威胁... Ra3。不过，在47. Rb3 Qxb3 48. Qxa5+ Kb7 49. Qd8 Qe6 50. f3 d5 51. exd5 cxd5 52. Qa5 Qd7 53. Qb4+ Kc7 54. Qd4之后形成的后残局并不简单，黑方能否获胜也不明确。')
group(76,77,'**48. Qa1 Qxe4+ 49. Kh2 Rb5 50. Qa2**')
group(79,80,'**50... Qe5+ 51. Kg1 Qe1+ 52. Kh2**')
group(89,91,'中心总攻未能奏效，加上应付对手接连不断的威胁所带来的疲劳，看来共同促成了拉斯克的失误。不过，此时黑王已十分危险，和棋本来就是黑方能够争取的最好结果。为此，他应走54... Rb7或54... Rb8。','**55. Qa6 Rb8**','55... Rb7 56. Qe6同样救不了他。')
group(92,94,'**56. Ra7+ Kd8 57. Rxg7 Qb6 58. Qa3 Kc8**','若58... Qb4，则59. Qa7。拉斯克走完最后一步便认输了，没有等白方走出59. Qf8+ Qd8 60. Qc5+，形成杀棋。')
group(97,97,'1895年在黑斯廷斯国际锦标赛的拉斯克对皮尔斯伯里一局，形成了图中局面。')
group(102,102,'犹如伤虎奋起一扑！这让人想起上一局施莱希特的“拼命”下法。白方背水一战，勇敢地用中心兵换取对方的侧翼兵。其他棋手或许更愿意走23. Qf3，但黑方可应以23... Qd4+ 24. Kh1 Qg7，威胁在f线上兑子。')
group(104,108,'皮尔斯伯里低估了对手在a线获得通路兵后的反击机会。在重子斗争中，通路兵能显著增加己方的选择。例如，白方现在可以接受后残局；某些情况下，只要黑王不能及时封锁通路兵，白方甚至可以接受车残局。因此，皮尔斯伯里应当选择24... c4。此后无论25. Qxc4 Qxc4 26. bxc4 Rb2，还是25. bxc4 Qf2! 26. Rg1 Qb6 27. Qa4 Rf8 28. Qd7 e5，都对黑方有利。','他显然顾虑另一个后续手段：25. Qc6 Rf8! 26. Rxf8+ Kxf8 27. h3 cxb3 28. axb3 Qc5 29. Qd7 Qxc2 30. Qxe6 Qc1+ 31. Kh2 Qf4+ 32. Kh1 Qf7；若改走30. Qxh7，则30... Qxe4 31. Qxc7 Qe1+ 32. Kh2 Qe5+ 33. Kh1 a5。两种情况下，黑方固然都需要很好的技术，但应当能够获胜。')
group(113,113,'**28... e5 29. h3**','**29... Rb4?**')
group(115,117,'走出这步致命的错误之前，皮尔斯伯里仍有希望兑现子力优势。他应走29... Re8，从后方支援e兵。例如30. a5 d5 31. Qe2 e4 32. Ra1 Qg7! 33. Ra2 e3 34. a6 Qe5 35. a7 Ra8，黑方仍有较好的机会。即使已经走错，他也应立即退车b8加以纠正。但他执意贯彻原来的想法，从此每况愈下。从心理角度看，这一过程颇值得玩味。')
group(119,121,'白方威胁33. Qf2，若33... Qe7，则34. a7，黑方阵地已危机四伏。因此必须走32... Rb8，才能继续抵抗，而且只能争取和棋。以下变化可以说明：33. Qg3 Ra8 34. Ra1 Ra7! 35. Qb8+ Kg7。白方也没有比36. Qe5+ Kg8 37. Qb8+强制和棋更好的办法；若改走37. Rf1，则37... Qe7，白方并无收获。')
group(124,124,'**33... e3 34. Ra1**')
group(125,125,'白方的通路兵抢先一步：34... e2 35. a7，b4车只能置身事外。若34... Qa7，白方直接吃掉e3兵即可。')
group(127,129,'35. Ra2也足以获胜，但必须算清双方各有双后的变化。可能的结局如下：35... Qf1+ 36. Kh2 e2 37. a7 e1=Q 38. a8=Q Kg7 39. Ra7+ Kh6 40. Rxh7+ Kxh7 41. Qgc7+ Kh6 42. Qh8+ Kg5 43. Qcd8+ Kf4 44. Qh6+，黑方被将杀。值得注意的是，这是35. Ra2之后唯一的取胜途径。好运如此意外地降临，拉斯克不愿再冒险试探它。')
group(130,133,'**35... d4**','若35... Re4，则36. a7 Re8 37. Rxe3 Rc8 38. Qb8 Qf8 39. Qb7 Qf1+ 40. Kh2 Qf4+ 41. Rg3 Qf8 42. Rf3 Qe8 43. Re3!，白方获胜。','**36. a7 Qd8 37. Ra1 Qa8 38. Qd6 Rb7**','若38... e2，则39. Qe6+；若38... Rb5，则39. Ra6。')
group(140,142,'**27... Qf6 28. Rf1**','若28. Qc5，则28... e4 29. Rb1 Ra2，a兵已经难逃被吃的命运；28. Qf1 e4 29. a6 Rxf2同样无济于事。','**28... Qd8 29. a6**')
group(151,151,'图中局面出自1935年在莫斯科的罗曼诺夫斯基对斯塔尔贝里一局。')
group(161,163,'此时仍可走39... Kg8；若40. Qc4 Qxc4 41. Rxc4 Kf7，黑王仍来得及保护c5兵。而黑王在g6并不安全，白方接下来的行动将证明这一点。')
group(167,168,'现在走Rc4后，便有闪将的威胁；若41... Kh7，白方则有出人意料的应手42. Rxe5。','**41... Kf7 42. Qc3 Re6 43. h4**')
group(172,172)
group(174,175,'黑方上一步给了白方提出兑换的机会。也可以走强制性较弱的44. h5，把局势的骤变稍向后推，让对手继续承受一段时间的心理压力。')
group(178,184,'除实战的后续手段外，黑方还可以选择44... Rd6或44... Qxc4。前者可用45. Ke3!应对，此时45... Ke7不好，因为46. f4；45... Kf7也不好，因为46. Rxe5。','若44... Qxc4，则可能出现45. Rxc4 Rc6 46. Ke3 Ke7 47. Ke4 Ke6 48. h5 Rc8 49. Ra4。我们认为黑方最好的应手是49... Rd8，有很好的和棋机会：无论50. Ra6+ Rd6，还是50. Ra7 Rd4+ 51. Ke3 Rd7，接下来若转入兵残局，都应当能够弈和。')
group(189,191,'有力的应手。黑方组织起对白王的反击。也可以走46... Qxd3，随后47. Ra8+ Re8 48. Rxe8+ Kxe8 49. Qg8+ Kd7 50. Qxg7+ Kc8 51. Qh8+ Kd7 52. Qxe5 c4 53. Qe3 Qc2+ 54. Ke1 c3 55. Qe2，接着55... Qb2或55... Qg6，黑方应能守和。')
group(192,192,'**47. Ra8+**','**47... Rb8**')
group(193,197,'黑方过于相信一般经验，以为转入残局便能轻松守和。这正是拘泥成见所付出的代价！他本可以立即确保和棋，为此应走47... Ke7。若48. Qg8（这正是白方原来的打算），则48... Rb2+ 49. Ke1 Rb1+ 50. Kd2 Rd1+! 51. Kxd1 Qxd3+ 52. Kc1 Qc3+ 53. Kb1 Qd3+ 54. Kb2 Qd2+ 55. Kb3 Qd3+ 56. Ka4 Qd4+ 57. Ka5 Qd2+ 58. Ka6 Qd6+ 59. Kb5 Qd7+! 60. Kxc5 Qd4+ 61. Kb5 Qd7+（或61... Qb2+）。白王无处藏身。黑方只须选择白后不能挡住的将军，而这并不难做到。')
group(204,206,'致命的错误。黑方仍可用57... Qf2争取和棋；若58. Kxe5，则58... Qc5+，再次长将。黑方舍不得兵，结果却保不住王。')
group(207,207,'**58. Kg6 Qc1 59. Qd7 Qg1+ 60. Kf7 Kh7 61. Qf5+ g6 62. Qd7 1-0**')
group(214,215,'6... e5这一后续手段，在7. Ndb5 a6的变化中可以成立；但白方若走7. Nf3 d4 8. Nd5 Nc6 9. e4，黑方就不够满意。尤伟对阿廖欣世界冠军回敬赛的第二十九局表演对局就出现过这个变化。')
group(221,223,'9... Qxb2无异于自取灭亡。最简单的反驳是10. Ndb5；列文菲什指出的10. O-O也很好。若10... Qxc3?，则11. Rc1，黑方只得走11... Qxc1，因为11... Qa3会遭到12. Bb5+ Bd7 13. Rc8+，白方迅速获胜。')
group(224,225,'**10. O-O Nc6 11. Bb3 Be7 12. Rc1 Rd8**')
group(226,227,'12... O-O-O更差，因为13. Qh5。','**13. Nxc6 Bxc6 14. Qh5 Qc5**')
group(235,237,'黑方必须照顾王的安全。若24... Rxb2?，则25. Rc7+ Kf8 26. Qh4 Kg7 27. Qg4+ Kh8（27... Kf8 28. Qh5）28. Rxf7，白方获胜。')
group(239,240,'白方避开了... Rd1+之后沿长斜线的将军，并威胁29. Qa8 Rd8 30. R1c7+ Ke8 31. Rxd8+ Qxd8 32. Rc8。这迫使黑方兑掉一对车，转入本章常见的双方各有一后、一车的局面。他认为，减少子力应当能够缓解对手的攻势。')
group(245,245,'**32. Qc3 b5 33. Rc6 Qd4 34. Qc2 b4**')
group(257,261,'白王避开了黑后在d5将军的可能。不过，41. Qf6并威胁Rd4更强。例如41... Qd5+ 42. Kh3 Qxa2 43. Rd4+ Kc6 44. Qd8，白方获得决定性的进攻。不过，若41... Kc6立即退王，则42. Rd4，黑方最好以42... Qe7接受少一兵的残局。')
group(268,268,'**45... Ra7 46. Qb8+ Rb7 47. Qe5+ Ka6**','**48. Rc4**')
group(269,277,'白方还有另一项有力的后续手段。当时许多棋手的分析表明，48. a3可以带来无法抵挡的进攻。这步既清除黑王最后的兵屏障，又消除白方自身的弱点，而这个弱点恰恰会成为黑方后来在残局中争和的主要希望。','黑方最好的防守是48... Rb5（若48... bxa3，则49. Ra4+ Kb6 50. Qa5+ Kc6 51. Rc4+，黑方很快被将杀），但白方有强有力的49. Qe2，借助a4和axb4的威胁，迫使黑方走49... bxa3。','随后50. Ra4+ Kb6 51. Qe3+ Kc6 52. Ra6+ Kc7 53. Ra7+（53. Rxe6强制性较弱，但也足够）53... Rb7 54. Qe5+ Kc8 55. Ra8+ Kd7 56. Qd4+ Kc7 57. Qc4+ Kd7（若57... Kd6，则58. Ra6+ Ke5 59. Qc3+ Kd5 60. Ra5+ Kd6 61. Ra4）58. Qc8+ Kd6 59. Ra6+ Ke5 60. Qc3+ Kd5 61. Ra4 Qc5 62. Qf3，白方取得决定性进展。')
group(285,286,'a）50... Ka4? 51. Ra6+ Ra5 52. Qc8，白方获胜。')
group(287,288,'b）50... Rb7 51. Qd4 Qd7 52. Qc4 Rb5 53. Rc7 Qd6 54. Rxh7。','c）50... Rb6 51. Qa8+ Kb5 52. a4+ bxa3 53. Rc3 Ra6 54. Qb8+ Ka5（54... Ka4 55. Qb3+ Ka5 56. Rc4）55. Qe5+ Kb4（55... Kb6 56. Rb3+ Kc6 57. Qb5+）56. Qd4+ Ka5（若56... Kb5，则57. Rb3+ Kc6 58. Qc4+；或57... Ka5 58. Qe5+）57. Rc5+ Kb6 58. Rc1+ Ka5 59. Qe5+ Kb4（或59... Kb6）60. Rb1+，黑方必须认输。')
group(289,290,'d）50... Qb7 51. Rc8 Ka4 52. Ra8+ Ra5 53. Qe8+ Qb5 54. Rxa5+ Kxa5 55. Qxe6。这一变化中52. Qe8!更强，52... Ka3 53. Qxe6 Qd5 54. Qe3+，白方在子力和局面上都占据巨大优势。')
group(293,294,'**51... Rd5 52. Re2 Rd6 53. f4 Rh6+ 54. Kg2 Kb5 55. h3 Rg6 56. Kf3 h5 57. Re5+ Kc4 58. Rxf5 Ra6 59. Rxh5 Rxa2 60. Rh8 b3 61. Rc8+ Kd4 62. Rd8+ Kc3 63. Rc8+ Kd3 64. Rd8+ Kc3 65. Rc8+**')

edits[189][1].append('〔校勘注：此处经校正应为53... Qc2+，后续54. Ke1 c3 55. Qe2以及55... Qb2、55... Qg6两种应手均可成立。〕')
group(153,153,'白方应制定怎样的计划？第一阶段的主要任务，是把黑后赶离中心的d5据点，再让自己的后占据c4，使后更加活跃。同时，白方要准备兑后转入车残局，并为此尽可能创造有利条件。')
main_ids={16,18,20,25,27,29,33,35,37,39,43,45,47,49,51,53,57,59,61,63,65,67,74,76,79,82,84,86,88,101,103,109,111,113,118,122,124,126,134,138,140,144,148,156,160,164,166,170,173,176,186,188,192,199,201,203,207,213,216,220,224,229,231,234,238,241,243,245,248,250,252,254,256,262,264,266,268,279,281,291,293}
blocks=[];newrows=[];skip=set()
for r in rows:
    n=int(re.search(r'CH6-(\d+)',r['segment_id'])[1])
    if n in skip:continue
    if n in edits:
        end,parts=edits[n];members=[x for x in rows if n<=int(re.search(r'CH6-(\d+)',x['segment_id'])[1])<=end]
        skip.update(range(n+1,end+1));ids=[y for x in members for y in x.get('source_ids',[x['segment_id']])]
        out=dict(r,segment_id=f'CH6-{n}'+(f'–{end}' if end!=n else ''),source_ids=ids,text=' '.join(x['text'] for x in members),zh='\n\n'.join(parts),review_status='illustrated_review_2026-09-28')
        if len(members)>1:out['page_end']=members[-1].get('page_end',members[-1]['page'])
        out['kind']='moves' if len(parts)==1 and parts[0].startswith('**') else 'body'
        if not parts:
            out=dict(r,layout_omit=True)
    else:
        out=dict(r);parts=[r['zh']]
        if n in main_ids:parts=['**'+r['zh']+'**'];out['zh']=parts[0];out['kind']='moves'
    newrows.append(out)
    if n==1:continue
    for k,t in enumerate(parts):
        ismove=t.startswith('**') and t.endswith('**')
        kind='moves' if ismove else out.get('kind','body')
        if kind not in ('moves','heading','metadata'):kind='body'
        blocks.append(dict(key=f'{n}.{k}',last_key=f'{n}.{k}',ids=out.get('source_ids',[out['segment_id']]),page=r['page'],kind=kind,text=t[2:-2] if ismove else t))
assert len([x for r in newrows for x in r.get('source_ids',[r['segment_id']])])==296
(TMP/'ch6_illustrated_blocks.json').write_text(json.dumps(blocks,ensure_ascii=False,indent=2),encoding='utf-8')
src.write_text(json.dumps(newrows,ensure_ascii=False,indent=2),encoding='utf-8')
for field,suffix,title in [('zh','zh','中文修订稿'),('text','en_ocr','英文OCR核对稿')]:
    lines=[f'# 第六章：重子斗争（{title}）','修订日期：2026-09-28。异常断段已合并，保留原编号对应关系。']
    for r in newrows:lines.extend(['## '+r['segment_id'],r[field]])
    (TRANS/f'{name}_{suffix}.md').write_text('\n\n'.join(lines)+'\n',encoding='utf-8')
allrows=json.loads((TMP/'reviewed_segments.json').read_text(encoding='utf-8'))
allrows=[r for r in allrows if r['chapter']<6]+newrows+[r for r in allrows if r['chapter']>6]
(TMP/'reviewed_segments.json').write_text(json.dumps(allrows,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# 第六章：重子斗争']
for b in blocks:lines.extend(['<!-- '+', '.join(b['ids'])+' -->',('**'+b['text']+'**') if b['kind']=='moves' else b['text']])
(TRANS/f'{name}_illustrated_zh.md').write_text('\n\n'.join(lines)+'\n',encoding='utf-8')
print(len(blocks),'layout blocks;',len(newrows),'review units; 296 original IDs covered')
