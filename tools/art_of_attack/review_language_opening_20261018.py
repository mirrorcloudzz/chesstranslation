"""Apply the individually reviewed opening/chapter 1–3 language corrections."""
import json
from pathlib import Path
from build_opening_proofs import PROJECT, parse_file

# Stable IDs, exact phrase changes, and the reason established by EN/ZH reading.
EDITS = {
 'FM-5': [('会让每一位国际象棋爱好者的走法更有力量，也更富于精彩的构思', '能使国际象棋爱好者的棋艺更有力量，构思更加精彩', 'play指整体棋艺；理顺“富于精彩的构思”的搭配')],
 'FM-8': [('第三章　易位与攻击易位局面概论', '第三章　易位与攻击王城的一般问题', '目录与权威章节标题一致')],
 'FM-9': [('第十二章　杀王进攻：对局不可分割的一部分', '第十二章　杀王进攻作为对局整体的一部分', '目录与权威章节标题一致')],
 'IN-4': [('最初的局面思想', '最初的局面棋思想', '落实已确认的positional ideas译法')],
 'IN-5': [('因为对局面认识的加深，也为防守技术的完善奠定了基础', '因为人们对局面棋的理解不断加深，为防守技术的完善奠定了基础', '落实positional understanding的已确认译法并理顺因果句'), ('准确的局面走法', '准确的局面棋走法', 'positional play术语一致')],
 'IN-15': [('白方转而选择局面棋走法**2. Ne4**，也已经满意', '白方转而选择局面棋走法**2. Ne4**，便可得到满意的局面', '理顺be content with的中文表达')],
 'IN-43': [('建立在进攻方在局面棋方面的优势之上', '建立在进攻方的局面棋优势之上', '消除重复介词导致的拗口')],
 'IN-44': [('某个进攻组合', '某个进攻组合战术', 'combination为棋理中的组合战术，避免含混')],
 'CH1-24': [('10... e4之后的走法已经没有多少悬念', '10... e4之后的走法已无须在这里继续讨论', 'no longer of interest指偏离本节讨论重点，并非胜负毫无悬念')],
 'CH1-31': [('只能以**4. Kf2**为代价接受失后', '只能走**4. Kf2**，接受失后的代价', 'Kf2是被迫应对，失后才是代价；纠正修饰关系')],
 'CH1-70': [('一个精彩组合就此开始，这是19世纪国际象棋中最出色的组合之一', '一个精彩的组合战术就此开始，这是19世纪国际象棋中最出色的组合战术之一', '组合战术术语及搭配')],
 'CH1-94': [('纳伊道尔夫变例', '纳道尔夫变例', '修正此前漏统一的Najdorf译名')],
 'CH1-100': [('获得获胜的进攻', '获得制胜进攻', '消除同义重复，准确表达winning attack')],
 'CH1-111': [('实施了如下组合', '实施了如下组合战术', 'combination术语明确')],
 'CH2-24': [('白方的两匹马因此占据越来越危险的位置', '白方的两匹马因此占据了越来越有威胁的位置', 'dangerous指对白方进攻有利、对黑方危险，避免主客体歧义')],
 'CH2-41': [('进攻中的先手，以及逐步织成一道让王无路可逃的杀网', '进攻的节奏，以及逐步织成一道让王无路可逃的杀网', 'tempo of the attack在此指进攻节奏；后句tempi仍保留先手')],
 'CH2-42': [('用连续将军保持进攻的先手', '用连续将军保持进攻的节奏', '区分进攻节奏与具体所得先手')],
 'CH2-47': [('以保持进攻中的先手', '以保持进攻的节奏', 'keep up the tempo of the attack与本节论述一致')],
 'CH2-124': [('使优势变得明确', '从而确立明显优势', '理顺made his advantage clear的中文棋理表述')],
 'CH2-151': [('成功到让对手除了长将之外，再也无计可施', '使对手最多只能取得长将', 'to the extent that限定脱险的成果，不等于对手无计可施；消除生硬句法')],
 'CH2-167': [('形成强大的主动权', '取得强劲的主动权', '主动权搭配修正')],
 'CH2-185': [('它并不能带来更多，只能保持均势', '这步只能维持均势，并不能带来优势', '补足不明所指的“更多”，明确原意')],
 'CH2-189': [('在这个局面中，这步既好，也必需', '在这个局面中，这既是好棋，也是必要的一步', '修正句法及词语搭配')],
 'CH2-224': [('这位组合天才', '这位组合战术天才', '明确combinative genius的棋理含义')],
 'CH2-244': [('黑方在整盘棋中的表现，恰好展示了追赶游走的王时不应怎样进攻', '黑方在整盘棋中的表现，为如何进攻游走的王提供了一个反面教材', '消除“不应怎样”的生硬结构，保留反面示例含义')],
 'CH3-3': [('我们值得先考察易位的一般意义', '有必要先考察易位的一般意义', '纠正“我们值得考察”的主谓搭配')],
 'CH3-7': [('反映出欧洲社会自中世纪以来日益增强的活力', '反映出欧洲自中世纪以来社会运动日益活跃的趋势', '保留social movements的社会运动含义，不将其泛化为整个社会的活力')],
 'CH3-11': [('积极组合的一部分', '具体组合战术的一部分', 'active combination在动态/静态对照中指实际战术行动，避免生硬直译')],
 'CH3-13': [('易位后的王的位置相当明确地构成了持久的局面棋特征', '易位后的王位便构成了局面中的一个持久特征', '此处positional feature直译局面棋特征拗口，按既有软性规范顺译')],
 'CH3-33': [('但对白方已经形成的王城，进攻是决定性的', '但白方已经易位，黑方就能发动制胜进攻', '理顺对王城进攻的主谓关系')],
 'CH3-62': [('那么一个先手与两个先手的差别就很大了', '那么只需一步与需要两步的时间差别就十分关键了', '这里tempi是完成易位耗费的时间，并非赢得一个或两个先手')],
 'CH3-91': [('看起来作者主要关心得一兵', '看起来作者主要关心的是如何得一兵', '补足宾语结构')],
 'CH3-92': [('给出一些组合', '给出一些组合战术', 'combination术语明确')],
 'CH3-112': [('再加上一对活跃的双象', '再加上活跃的双象', '消除“一对双象”的数量重复')],
 'CH3-113': [('随后兴起的浪漫派反响，推动了多种特殊弃子进攻的发展', '随后浪漫派棋风再度兴起，推动了多种特定类型的弃子进攻的发展', 'romantic reaction指棋风上的回潮；“浪漫派反响”不通顺')],
}

def main():
    records=[]
    for stem in ['front_preface','introduction','ch01','ch02','ch03']:
        p=PROJECT/'translation'/f'{stem}_v1.md'
        raw=p.read_bytes(); text=raw.decode('utf-8')
        for s in parse_file(stem):
            if s['segment_id'] not in EDITS: continue
            old=s['zh']; new=old; reasons=[]
            for before,after,reason in EDITS[s['segment_id']]:
                assert new.count(before)==1,(s['segment_id'],before)
                new=new.replace(before,after); reasons.append(reason)
            oldline='ZH: '+old.replace('\n',r'\n')
            newline='ZH: '+new.replace('\n',r'\n')
            assert text.count(oldline)==1,s['segment_id']
            text=text.replace(oldline,newline)
            records.append(dict(id=s['segment_id'],sourcepage=s['page'],before=old,after=new,reason='；'.join(reasons)))
        p.write_bytes(text.encode('utf-8'))
    dest=PROJECT/'translation/language_review_opening_ch01_03_20261018.json'
    dest.write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'{len(records)} paired units corrected')

if __name__=='__main__':main()
