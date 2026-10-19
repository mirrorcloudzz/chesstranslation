import json,re,hashlib
from pathlib import Path
base=Path('translations/art_of_attack/translation')
changes=json.loads(r'''[["CH7-49","这个例子说明，实行针对底线弱点的组合时，必须保持高度警惕，谨慎计算。","原译“必须多么警惕”不符合陈述句语法，按原文强调谨慎之意调整。"],["CH7-80","此局面出自尼姆佐维奇—卡帕布兰卡，纽约，1927年。黑车已经深入第七横线（白方第二横线），但f2兵挡在途中，其威力尚未完全显现。为了完全控制这条横线，黑方弃一兵，借此叠车。","原译添加“对方的第七横线”导致方位相反；此处按黑方视角计数，对应白方第二横线。"],["CH7-103","白方在这里通常应准备所谓的少数兵进攻，客观而言这也是最佳方案。例如短易位并走Rab1后，将兵推到b4、a4，再以b5和bxc6削弱黑方兵形。另一种办法是兑换黑格象之后，利用黑方c5、b6的弱点。约纳棋风锐利，对这些局面棋方案不感兴趣，选择了第三条道路：异向易位，攻击易位王。这个计划并不坏，但黑方也有均等机会。","修正“通常也客观上最好是”的中文语序，保留原文对常见方案与客观最佳方案的双重判断。"],["CH7-305","车更值钱，弃车比弃象更难；在牵制中，子力价值的高低就更加重要：象换掉被牵制的车是得交换，象换马则价值相当，而车通过牵制获利，只有吃到后才行。另一个区别更明显：通常推进己方兵，就比较容易打开或封闭斜线；但要在直线上达到同样目的，兵必须吃子，自然就要取决于对方子力的配置，所以开放直线可能相当困难。反过来，要封闭直线，通常须建立前哨；斜线上的前哨却是例外，因为兵很容易完成“开关”动作。斜线全部的“微妙与深谋远虑”，归根结底就在这里。我们以斜线上的牵制开始这一组实例。这里的牵制其实只是清理整条斜线过程中的暂时环节，最后吃掉被牵制棋子，彻底打通线路。","修正“子力价值的次序更为相关”的生硬表达，准确呈现价值高低在牵制中的重要性。"],["CH8-45","改走2. exf4也不会更好，因为黑方可2... Qh4，同时威胁3... Rxg2+和3... Qxh3。","明确no better的比较含义，修正“并不好些”的不自然表达。"],["CH8-64","这是伯恩施坦—科托夫，格罗宁根，1946年一局的结尾。黑方贪心地吃了一兵，其实根本没有必要；他刚走了...Re4xb4，而正确的是...Rc4，结果如下输棋：","将“贪心而多余地吃”改为通顺中文，保留greedily与needlessly两个判断。"],["CH8-161","1）进攻方的兵，无论是否弃掉，迫使对手削弱王城。\\n2）制造进攻中的组合因素，例如引离或引入敌子，或开放直线。\\n3）组成攻击配置的一部分，例如h1车、h4兵的配置，或支持焦点上的棋子。\\n4）这种攻击配置中，一个值得单列的例子是兵中心；它通常总体限制对手，或为攻击易位王提供基础。\\n5）兵在侧翼独立推进，驱赶敌子或控制某格。这通常称为刺刀进攻。\\n6）两三个侧翼进攻兵组成正面阵列，向敌王城推进，即兵的雪崩或滚压。\\n7）兵进入王城区域，直接作为攻击单位对付敌王。\\n8）兵进入王城区域，争取升变；这一过程可以伴随对王的攻击，也可以没有。升变后，兵便能以新的身份继续进攻。","第8点with or without修饰推进过程是否伴随攻王，不是升变的方式；原译表达含混，重新理顺修饰关系。"],["CH8-223","¹ 纳恩注：黑方可27... Qc3! 28. exf7+ Kh8意外扭转局势，但白方可以提前改进：27. Ne7+ Kf8 28. Qf6获胜。","turn the tables表示扭转局势，原译“反败为胜”把原文未明说的最终取胜写成确定结论。"],["CH8-266","两三个相邻兵处于同一横线的阵形，棋书常称为“兵方阵”；这种方阵展开攻击时，也很适合形容为“雪崩”或“滚压”。兵雪崩进攻通常比刺刀进攻受到更多局面上的约束，因为要推进的是两个兵，而非一个。但雪崩的威力也更大，它能把面前的敌子全部赶开，提供更多进攻可能。","positional commitments指冲兵后在局面上作出的承诺及所受约束，“承担责任”易误导为一般责任；按上下文改为约束。"],["CH8-310","对21... fxg6，克莫赫指出22. Rxg6?较弱（因为22... exf3，黑方弃后换得的子力太多）。他认为以下变化有利于白方：22. Nh4 g5 23. Ng6 Qf6 24. h7+ Kf7 25. h8=Q Rxh8 26. Nxh8+。但26... Ke7之后，局面有些可疑，因为白方设法把马从角落撤出时，黑方能组织反击，例如27. Qe2 c3! 28. Qh5（或28. bxc3 Ba3+再...Qf5）28... cxb2+；若29. Kb1，则29... Ba3；若29. Kxb2，则29... Qxf2+，等等。","原译把交换方向颠倒；in return for his queen是黑方交出自己的后，取得过多补偿子力。"],["CH8-337","【纳恩注1】实际上，26... Ke8 27. Qxf8+ Kd7等之后，白方最终在子力上吃亏，所以应改走23. hxg7 Bxg7 24. Rh7 Qc7 25. Rgh1，随后将杀。","material down泛指子力价值处于劣势，不一定少一个轻子；改掉可能被读成具体少子的表述。"],["CH8-374","关于兵的攻击，实战中常有两种值得一提的情形：一种要求在进攻中采用固定兵形，发挥兵的局面棋作用；另一种则完全不适合兵参与，最好只靠棋子进攻。下面各给出适当例子。","rigid, positional描述兵的固定形态及局面棋用法，不是“严格按照原则”；与下一例主动封闭兵形的说明一致。"],["CH7-101","本书写作时的理论对此着评价不高。白方在d5兑换，可获得稳健而有利的局面。","明确Modern theory的时间参照为作者写作时，避免让读者误解为本次校对时的理论判断。"],["CH8-403","对其他任何着法，白象都可到达f6，决定胜负，例如5... Nc6 6. Nf3 Nh7 7. Bh6 Qd7 8. Bg5，等等。","reaching f6表示象最终到达f6，原译“经由f6”容易读成途经该格。"],["CH8-411","黑方被牵制在王翼，白方最佳计划是在h线上叠加后双车。白方进行必要的重新部署，既阻止黑象渗透，又延缓黑车沿c线侵入；同时超额保护e5格，防备对手孤注一掷的弃子。","over-protect是有意增加保护的正面技术概念；统一为本书前文“超额保护”，避免“过度”暗示不必要或有害。"],["CH9-19","面对侧翼出象王城，自然没有h7弃象的机会；而且，许多在普通王城中很典型的弃子，也不适用于这种特殊结构。针对侧翼出象王城，一种有代表性的弃子是在f5弃马。下图就是一例。","原译“才是”增加排他性；原文只指出一种具有代表性的形式，不排除其他特色弃子。"],["CH9-127","【纳恩注2】卡斯帕罗夫当时的新近分析指出了第三种可能：21. Rb3 Qg5+ 22. Kb1 Nd2+ 23. Ka1 Nxb3+ 24. cxb3 Bd6 25. Qa7+ Kc8 26. Nxd6+ Rxd6（26... cxd6 27. f4! gxf3 28. Nxf3，车将进入c1）27. Qa8+ Kd7 28. Qxh8，白方多两兵。","Recent相对于纳恩撰注的时间，补明“当时”，避免被理解为本次校对日前的新分析。"]]''')
paths={n:base/f'ch{n:02}_v1.md' for n in (7,8,9)}
original={n:p.read_bytes() for n,p in paths.items()}
records=[]
for seg,after,reason in changes:
 n=int(re.match(r'CH(\d+)-',seg)[1]); raw=original[n].decode('utf-8')
 m=re.search(r'^## '+re.escape(seg)+r' \| ([^|]+) \| [^\r\n]+\r\nEN: [^\r\n]*\r\nZH: ([^\r\n]*)',raw,re.M)
 assert m,seg
 records.append(dict(id=seg,sourcepage=m[1].strip(),field='ZH',before=m[2],after=after,reason=reason))
for n,src,dst in [(8,'科列','科勒'),(9,'列舍夫斯基','雷舍夫斯基')]:
 raw=original[n].decode('utf-8')
 for block in re.split(r'(?=^## CH)',raw,flags=re.M):
  m=re.match(r'## (CH\d+-\d+) \| ([^|]+) \|',block)
  if not m: continue
  for line in block.splitlines():
   if src not in line: continue
   if line.startswith('ZH: '): field='ZH'; before=line[4:]
   elif line.startswith('FIG: '): field='caption_zh'; before=line.split(' | ',1)[1]
   else: raise AssertionError(line)
   records.append(dict(id=m[1],sourcepage=m[2].strip(),field=field,before=before,after=before.replace(src,dst),reason='按全书既有正文与棋手索引统一译名，经统稿确认。'))
for n,p in paths.items():
 text=original[n].decode('utf-8')
 for rec in records:
  if not rec['id'].startswith(f'CH{n}-'): continue
  pat=r'(^## '+re.escape(rec['id'])+r' \| [\s\S]*?)(?=^## |\Z)'
  m=re.search(pat,text,re.M); assert m
  block=m[0]
  if rec['field']=='ZH':
   before='ZH: '+rec['before']; after='ZH: '+rec['after']
  else:
   before=' | '+rec['before']; after=' | '+rec['after']
  assert block.count(before)==1,(rec['id'],rec['field'])
  block=block.replace(before,after,1)
  text=text[:m.start()]+block+text[m.end():]
 result=text.encode('utf-8')
 # Confirm original CRLF, all IDs/EN and all FIG identities are unchanged.
 for prefix in (b'## ',b'EN: '):
  assert [x for x in original[n].splitlines() if x.startswith(prefix)]==[x for x in result.splitlines() if x.startswith(prefix)]
 assert original[n].count(bytes([13,10]))==result.count(bytes([13,10]))
 assert bytes([10]) not in result.replace(bytes([13,10]),b'')
 assert [x.split(b' | ')[0] for x in original[n].splitlines() if x.startswith(b'FIG: ')]==[x.split(b' | ')[0] for x in result.splitlines() if x.startswith(b'FIG: ')]
 p.write_bytes(result)
summary={str(n):dict(units=len(re.findall(rb'^## CH',original[n],re.M)),figures=len(re.findall(rb'^FIG:',original[n],re.M)),sha256_before=hashlib.sha256(original[n]).hexdigest(),sha256_after=hashlib.sha256(paths[n].read_bytes()).hexdigest()) for n in paths}
report=dict(date='2026-10-18',scope=['ch07_v1.md','ch08_v1.md','ch09_v1.md'],reviewed=summary,changed_fields=len(records),changed_units=len(set(r['id'] for r in records)),changes=records)
(base/'language_review_ch07_09_20261018.json').write_bytes((json.dumps(report,ensure_ascii=False,indent=2)+chr(10)).encode('utf-8'))
print(json.dumps({k:v for k,v in report.items() if k!='changes'},ensure_ascii=False))

