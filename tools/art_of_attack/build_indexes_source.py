"""Transcribed from scan pages 350-352; preserve source page numbers and bold."""
from pathlib import Path
import re

FOLDER=Path(__file__).resolve().parents[2]/'translations/art_of_attack/translation'
NAMES={
 'Abramavicius':'阿布拉马维丘斯','Richter':'里希特','Alekhine':'阿廖欣','Asgeirsson':'阿斯盖尔松',
 'Asztalos':'阿斯塔洛什','Botvinnik':'鲍特维尼克','E. Cohn':'E. 科恩','Drewitt':'德鲁伊特','Feldt':'费尔特',
 'Gilg':'吉尔格','Kmoch':'克莫赫','Lasker':'拉斯克','Potemkin':'波将金','Rubinstein':'鲁宾斯坦',
 'Ståhlberg':'斯塔尔贝里','Supico':'苏皮科','Tarrasch':'塔拉什','Vygodchikov':'维戈德奇科夫','Weenink':'韦宁克',
 'Alexander':'亚历山大','Pachman':'帕赫曼','Szabo':'萨博','Anderssen':'安德森','Max Lange':'马克斯·朗格',
 'Raud':'劳德','Averbakh':'阿韦尔巴赫','Kotov':'科托夫','von Bardeleben':'冯·巴德勒本','Steinitz':'斯坦尼茨',
 'Barnes':'巴恩斯','Morphy':'墨菲','Bauer':'鲍尔','Fox':'福克斯','Belavenets':'别拉韦涅茨','Chistiakov':'奇斯佳科夫',
 'Bernstein':'伯恩斯坦','Capablanca':'卡帕布兰卡','Bird':'伯德','Boden':'博登','Blackburne':'布莱克本','Schwarz':'施瓦茨',
 'Schulder':'舒尔德','Bogoljubow':'波戈留波夫','Przepiorka':'普热皮乌尔卡','Réti':'列蒂','Julio Bolbochan':'胡利奥·博尔博昌',
 'Najdorf':'纳道尔夫','Boleslavsky':'波列斯拉夫斯基','Ufimtsev':'乌菲姆采夫','Bondarevsky':'邦达列夫斯基',
 'Lilienthal':'利林塔尔','Chekhover':'切霍韦尔','Rabinovich':'拉宾诺维奇','Rauzer':'劳泽尔','Reshevsky':'雷舍夫斯基',
 'Burn':'伯恩','Marshall':'马歇尔','D. Byrne':'D. 拜恩','Fischer':'菲舍尔','Colle':'科勒','Coria':'科里亚',
 'R. Illa':'R. 伊利亚','Kan':'卡恩','Molina':'莫利纳','Nimzowitsch':'尼姆佐维奇','Ragozin':'拉戈津','Schroeder':'施罗德',
 'Winter':'温特','Caro':'卡罗','Chigorin':'齐果林','Castaldi':'卡斯塔尔迪',"O’Kelly":'奥凯利',"O'Kelly":'奥凯利',
 'Clemens':'克莱门斯','Eisenschmidt':'艾森施密特','Euwe':'尤伟',"O’Hanlon":'奥汉隆',"O'Hanlon":'奥汉隆',
 'Tartakower':'塔塔科维尔','Delmar':'德尔马','Loyd':'洛伊德','Endzelins':'恩泽林斯','Vuković':'武科维奇',
 'Flohr':'弗洛尔','Maroczy':'马洛契','Field':'菲尔德','Tenner':'滕纳','Fine':'法因','Keres':'凯列斯','NN':'无名氏',
 'Stoltz':'斯托尔茨','Florian':'弗洛里安','Smyslov':'斯梅斯洛夫','Geller':'盖勒','Gligorić':'格里戈里奇','Kostić':'科斯蒂奇',
 'Petrosian':'彼得罗相','Golmayo':'戈尔马约','Guimard':'吉马尔','Hamppe':'汉佩','Meitner':'迈特纳',
 'Hansen':'汉森','Lundin':'伦丁','Ivkov':'伊夫科夫','Jaenisch':'雅尼施','Shumov':'舒莫夫','Janowski':'雅诺夫斯基',
 'Taubenhaus':'陶本豪斯','P. Johner':'P. 约纳','Keller':'凯勒','Rohaczek':'罗哈切克','Petrov':'彼得罗夫',
 'Kieseritzky':'基塞里茨基','Michelet':'米舍莱','Koltanowski':'科尔塔诺夫斯基','Tylor':'泰勒','König':'克尼希',
 'H. Weiss':'H. 魏斯','Kottnauer':'科特瑙尔','Tolush':'托卢什','Krogius':'克罗吉乌斯','Niemelä':'涅梅拉',
 'Soldatenkov':'索尔达坚科夫','Legall':'莱加尔','St Brie':'圣布里','Lewitzky':'列维茨基','Luprecht':'卢普雷希特',
 'Schulz':'舒尔茨','Marco':'马尔科','Yates':'耶茨','Mikenas':'米凯纳斯','Pillsbury':'皮尔斯伯里',
 'Mieses':'米泽斯','Meesen':'梅森','H. Müller':'H. 米勒','Varein':'瓦赖因','Rossolimo':'罗索利莫','Panov':'帕诺夫',
 'Ravinsky':'拉文斯基','L. Paulsen':'L. 保尔森','H. Wolf':'H. 沃尔夫','Pilnik':'皮尔尼克','Romanovsky':'罗曼诺夫斯基',
 'Renter':'伦特尔','P. Schmidt':'P. 施密特','Rödl':'勒德尔','Sämisch':'泽米施','van Scheltinga':'范·谢尔廷加',
 'Schlechter':'施莱希特','Teichmann':'泰希曼','Szigeti':'西盖蒂','Szilagyi':'西拉吉','Takacs':'塔卡奇','Toth':'托特',
 'K. Treybal':'K. 特雷巴尔','Vajda':'瓦伊达','Vidmar':'维德马尔',
}
PLAYERS={350: '''Abramavicius – Richter 232
Alekhine – Asgeirsson **170**, Asztalos **337**, Botvinnik **284**, E. Cohn **144**, Drewitt **199**, Feldt **31**, Gilg **297**, Kmoch **344**, Lasker **86**, Potemkin 28, Rubinstein 187, Ståhlberg 321, Supico **185**, Tarrasch 202, Vygodchikov 84, Weenink **212**, **300**
Alexander – Pachman **233**, Szabo **177**
Anderssen – Max Lange **77**
Asgeirsson – Alekhine 170, Raud **24**
Asztalos – Alekhine 337
Averbakh – Kotov **32**
von Bardeleben – Steinitz 19
Barnes – Morphy 46
Bauer – Fox 184, Lasker 197
Belavenets – Chistiakov **36**
Bernstein – Capablanca **142**, Kotov **190**
Bird – Boden 165
Blackburne – Schwarz **253**
Boden – Bird **165**, Schulder 76
Bogoljubow – Przepiorka **330**, Réti **255**
Julio Bolbochan – Najdorf 143
Boleslavsky – Ufimtsev **83**
Bondarevsky – Kotov 31, Lilienthal 303
Botvinnik – Alekhine 284, Chekhover **295**, Rabinovich **331**, Rauzer 313, Reshevsky 255
Burn – Chigorin 16, E. Cohn **96**, Marshall 289
D. Byrne – Fischer **33**
Capablanca – Bernstein 142, Colle 346, Coria 83, R. Illa **98**, Kan **316**, Molina **135**, Nimzowitsch **151**, **190**, Ragozin **256**, Schroeder **341**, Winter 186
Caro – Chigorin 38
Castaldi – O'Kelly 305
Chekhover – Botvinnik 295
Chigorin – Burn **16**, Caro **38**
Chistiakov – Belavenets 36
Clemens – Eisenschmidt **29**
E. Cohn – Alekhine 144, Burn 96
Colle – Capablanca **346**, Euwe 242, O'Hanlon **139**, Tartakower **192**
Coria – Capablanca **83**
Delmar – Loyd 193
Drewitt – Alekhine 199
Eisenschmidt – Clemens 29
Endzelins – Vuković 105
Euwe – Colle **242**, Flohr **114**, Maroczy **309**, Rubinstein **26**, Tartakower 37
Feldt – Alekhine 31
Field – Tenner **83**
Fine – Keres 204
Fischer – D. Byrne 33
Flohr – Euwe 114, NN **147**, Stoltz **152**
Florian – Smyslov 34
Fox – Bauer **184**
Geller – Kotov **182**
Gilg – Alekhine 297
Gligorić – Kostić **298**, Petrosian **32**
Golmayo – Steinitz 167
Guimard – Stoltz 178
Hamppe – Meitner **43**
Hansen – Lundin **17**
R. Illa – Capablanca 98
Ivkov – Najdorf 99''',351: '''Jaenisch – Shumov 194
Janowski – Lasker and Taubenhaus **99**
P. Johner – Rubinstein **153**
Kan – Capablanca 316
Keller – Rohaczek **194**
Keres – Fine **204**, Kotov **22**, 287, Petrov **210**, Reshevsky **239**, Winter **23**
Kieseritzky – Michelet 49
Kmoch – Alekhine 344
Koltanowski – Tylor 96
König – H. Weiss **218**
Kostić – Gligorić 298
Kotov – Averbakh 32, Bernstein 190, Bondarevsky **31**, Geller 182, Keres 22, **287**, Kottnauer 131, Szabo 90, Tolush 220
Kottnauer – Kotov **131**
Krogius – Niemelä **162**
Lasker – Alekhine 86, Bauer **197**, Janowski and Soldatenkov 99, Marshall **243**, Steinitz 320
Legall – St Brie **77**
Lewitzky – Marshall **185**
Lilienthal – Bondarevsky **303**, Najdorf **195**
Loyd – Delmar **193**
Lundin – Hansen 17, Tartakower **180**
Luprecht – Schulz **195**
Marco – Steinitz 223, Yates 271
Maroczy – Euwe 309, Mikenas 143, Pillsbury 329, Rubinstein 150
Marshall – Burn **289**, Lasker 243, Lewitzky 185, Mieses **322**
Max Lange – Anderssen 77
Meesen – H. Müller **15**
Meitner – Hamppe 43
Michelet – Kieseritzky **49**
Mieses – Marshall 322
Mikenas – Maroczy **143**
Molina – Capablanca 135
Morphy – Barnes **46**
H. Müller – Meesen 15
Najdorf – Julio Bolbochan **143**, Ivkov **99**, Lilienthal 195, Pilnik 116
Niemelä – Krogius 162
Nimzowitsch – Capablanca 151, 190, Tarrasch **198**
NN – Flohr 147, Varein 23
O'Hanlon – Colle 139
O'Kelly – Castaldi **305**
Pachman – Alexander 233, Rossolimo 277
Panov – Ravinsky 18
L. Paulsen – Steinitz 191
Petrosian – Gligorić 32
Petrov – Keres 210
Pillsbury – Maroczy **329**, Tarrasch **258**, H. Wolf **311**
Pilnik – Najdorf **116**
Potemkin – Alekhine **28**
Przepiorka – Bogoljubow 330
Rabinovich – Botvinnik 331, Romanovsky **240**
Ragozin – Capablanca 256
Raud – Asgeirsson 24
Rauzer – Botvinnik **313**
Ravinsky – Panov **18**
Renter – Tolush 176
Reshevsky – Botvinnik **255**, Keres 239
Réti – Bogoljubow 255, Tartakower **78**, H. Wolf **25**
Richter – Abramavicius **232**, P. Schmidt 158
Rödl – Sämisch **158**
Rohaczek – Keller 194
Romanovsky – Rabinovich 240
Rossolimo – Pachman **277**
Rubinstein – Alekhine **187**, Euwe 26, P. Johner 153, Maroczy **150**, Teichmann **215**
Sämisch – Rödl 158
van Scheltinga – Szabo 104
Schlechter – Tarrasch **213**, Teichmann 319''',352: '''P. Schmidt – Richter **158**
Schroeder – Capablanca 341
Schulder – Boden **76**
Schulz – Luprecht 195
Schwarz – Blackburne 253
Shumov – Jaenisch **194**
Smyslov – Florian **34**
Soldatenkov – Lasker and Taubenhaus **99**
St Brie – Legall 77
Ståhlberg – Alekhine **321**
Steinitz – von Bardeleben **19**, Golmayo **167**, Lasker **320**, Marco **223**, L. Paulsen **191**
Stoltz – Flohr 152, Guimard **178**
Supico – Alekhine 185
Szabo – Alexander 177, Kotov **90**, van Scheltinga **104**, Szilagyi 232
Szigeti – Toth 159
Szilagyi – Szabo **232**
Takacs – Yates 307
Tarrasch – Alekhine **202**, Nimzowitsch 198, Pillsbury 258, Schlechter 213
Tartakower – Colle 192, Euwe **37**, Lundin 180, Réti 78
Taubenhaus – Janowski and Soldatenkov 99
Teichmann – Rubinstein 215, Schlechter **319**
Tenner – Field 83
Tolush – Kotov **220**, Renter **176**
Toth – Szigeti **159**
K. Treybal – H. Wolf **265**
Tylor – Koltanowski **96**
Ufimtsev – Boleslavsky 83
Vajda – Vuković 166
Varein – NN **23**
Vidmar – Yates **326**
Vuković – Endzelins **105**, Vajda **166**
Vygodchikov – Alekhine **84**
Weenink – Alekhine 212, 300
H. Weiss – König 218
Winter – Capablanca **186**, Keres 23
H. Wolf – Pillsbury 311, K. Treybal 265, Réti 25
Yates – Marco **271**, Takacs **307**, Vidmar 326'''}
OPENINGS=[
 ('Blumenfeld Counter-Gambit 202','布卢门菲尔德反弃兵　202'),
 ('Caro-Kann Defence 78, 116','卡罗—卡恩防御　78、116'),
 ('Colle System 139, 346','科勒体系　139、346'),
 ('Danish Gambit 99','丹麦弃兵　99'),('English Opening 15','英国式开局　15'),
 ('Evans Gambit 29','伊文斯弃兵　29'),('French Defence 36, 170','法兰西防御　36、170'),
 ('Giuoco Piano 19, 55, 63, 92','意大利开局　19、55、63、92'),('Grünfeld Defence 34','格林菲尔德防御　34'),
 ("King's Gambit Accepted 49",'王翼弃兵接受弃兵变例　49'),
 ("King's Gambit Declined 16",'王翼弃兵拒弃兵变例　16'),
 ('Nimzo-Indian Defence 256, 344','尼姆佐-印度防御　256、344'),
 ('Petroff Defence 46, 243','俄罗斯防御　46、243'),('Philidor Defence 77, 271','菲利道尔防御　77、271'),
 ("Queen's Gambit Declined 153, 289, 337",'后翼弃兵拒弃兵变例　153、289、337'),
 ('Orthodox Defence 25, 86, 135, 215, 258, 311, 316, 341','　正统防御　25、86、135、215、258、311、316、341'),
 ('Semi-Slav Defence 131','　半斯拉夫防御　131'),('Semi-Tarrasch Defence 204','　半塔拉什防御　204'),
 ('Tarrasch Defence 198','　塔拉什防御　198'),("Queen's Pawn Game 218",'后兵开局　218'),
 ('Ruy Lopez 77, 84','西班牙开局　77、84'),('Sicilian Defence','西西里防御'),
 ('2... Nf6 23, 26','　2... Nf6　23、26'),('Closed Variation 28','　封闭变例　28'),
 ('Dragon Variation 284, 313','　龙式变例　284、313'),('Scheveningen Variation 220','　舍维宁根变例　220'),
 ('Najdorf Variation 22','　纳道尔夫变例　22'),('Sokolsky Opening 199','索科尔斯基开局　199'),
 ('Vienna Game 38, 43','维也纳开局　38、43')]


def translate_names(value):
    pattern='|'.join(re.escape(k) for k in sorted(NAMES,key=len,reverse=True))
    return re.sub(pattern,lambda m:NAMES[m[0]],value).replace(' and ','与').replace(' – ','—').replace(', ','、')


def block(sid,page,kind,en,zh):
    return f'## {sid} | {page} | {kind}\nEN: {en}\nZH: {zh}\n\n'


def main():
    text='# 《国际象棋进攻的艺术》棋手索引\n\n'
    text+=block('PI-1',350,'title','Index of Players','棋手索引')
    text+=block('PI-2',350,'paragraph','Numbers refer to pages. A number in bold indicates that the first-named player had White, e.g. Alekhine was White against Asgeirsson but Black against Rubinstein.',
                '数字指原书页码；本对照校样保留原书定位，不改作中文校样页码。粗体页码表示该条目中列在前面的棋手执白，例如阿廖欣对阿斯盖尔松时执白，对鲁宾斯坦时执黑。条目沿用原书拉丁字母顺序。')
    index=3
    for page,entries in PLAYERS.items():
        for entry in entries.splitlines():
            text+=block(f'PI-{index}',page,'paragraph',entry,translate_names(entry));index+=1
    (FOLDER/'players_v1.md').write_text(text,encoding='utf-8')
    text='# 《国际象棋进攻的艺术》开局索引\n\n'+block('OI-1',352,'title','Index of Openings','开局索引')
    for index,(en,zh) in enumerate(OPENINGS,2):text+=block(f'OI-{index}',352,'paragraph',en,zh)
    (FOLDER/'openings_v1.md').write_text(text,encoding='utf-8')
    print('Player entries:',sum(len(v.splitlines()) for v in PLAYERS.values()),'Opening entries:',len(OPENINGS))


if __name__=='__main__':main()
